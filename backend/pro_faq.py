# -*- coding: utf-8 -*-
"""ميزة قاعدة الأسئلة الشائعة المخصصة (Pro) / Custom FAQ Pro feature.

This module only accepts a small reviewed JSON document.  It never evaluates,
imports, or executes user supplied content.  A caller must supply a verified
server-side entitlement before it may read or change a customer's document.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

FAQ_SCHEMA_VERSION = 1
MAX_DOCUMENT_BYTES = 64 * 1024
MAX_ENTRIES = 100
MAX_QUESTION_CHARS = 240
MAX_ANSWER_CHARS = 2_000
MAX_KEYWORDS_PER_ENTRY = 8
MAX_KEYWORD_CHARS = 64

_ACTIVE = "active"
_CONFIGURATION_REQUIRED = "purchase_configuration_required"
_UNAUTHENTICATED = "unauthenticated"
_NOT_ENTITLED = "not_entitled"
_EXPIRED = "expired"
_CANCELLED = "cancelled"
_UNAVAILABLE = "entitlement_unavailable"

_ALLOWED_ENTITLEMENT_STATES = {
    _ACTIVE,
    _CONFIGURATION_REQUIRED,
    _UNAUTHENTICATED,
    _NOT_ENTITLED,
    _EXPIRED,
    _CANCELLED,
    _UNAVAILABLE,
}
_ENTRY_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}")
_ARABIC_DIACRITICS = re.compile(r"[\u064B-\u065F\u0670\u0640]")
_ARABIC_NORMALIZE_MAP = str.maketrans("أإآءىؤئ", "اااايوي")


class FaqValidationError(ValueError):
    """خطأ صيغة FAQ / Raised when a submitted FAQ document is invalid."""


class FaqStorageError(RuntimeError):
    """خطأ التخزين / Raised when the private FAQ store cannot be used safely."""


@dataclass(frozen=True)
class EntitlementDecision:
    """قرار استحقاق صادر من خادم موثوق / Trusted server-side entitlement result."""

    state: str
    account_id: Optional[str] = None
    subscription_id: Optional[str] = None
    expires_at: Optional[datetime] = None


def default_faq_document() -> Dict[str, Any]:
    """إرجاع مستند FAQ فارغ / Return a fresh empty FAQ document."""

    return {"version": FAQ_SCHEMA_VERSION, "entries": []}


def normalize_for_match(value: str) -> str:
    """تطبيع محدود للبحث النصي / Normalize text for deterministic FAQ matching."""

    normalized = value.casefold().strip()
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = _ARABIC_DIACRITICS.sub("", normalized)
    normalized = normalized.translate(_ARABIC_NORMALIZE_MAP)
    normalized = re.sub(r"[^\w\s]", " ", normalized, flags=re.UNICODE)
    normalized = re.sub(r"[\s_]+", " ", normalized, flags=re.UNICODE)
    return normalized.strip()


def _clean_text(value: Any, field_name: str, max_chars: int) -> str:
    """التحقق من نص صريح / Validate and normalize one plain-text FAQ field."""

    if not isinstance(value, str):
        raise FaqValidationError(f"{field_name} يجب أن يكون نصاً.")

    normalized = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        raise FaqValidationError(f"{field_name} لا يجوز أن يكون فارغاً.")
    if len(normalized) > max_chars:
        raise FaqValidationError(f"{field_name} يتجاوز الحد الأقصى ({max_chars} حرفاً).")
    if any(ord(char) < 32 and char not in "\n\t" for char in normalized):
        raise FaqValidationError(f"{field_name} يحتوي محارف تحكم غير مسموحة.")
    return normalized


def _serialized_size(payload: Any) -> int:
    """حساب حجم JSON بأمان / Return the UTF-8 JSON size without executing input."""

    try:
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise FaqValidationError("مستند FAQ يجب أن يكون JSON صالحاً فقط.") from error
    return len(encoded)


def validate_faq_document(payload: Any) -> Dict[str, Any]:
    """التحقق الصارم من مخطط FAQ / Strictly validate and normalize FAQ JSON."""

    if _serialized_size(payload) > MAX_DOCUMENT_BYTES:
        raise FaqValidationError(
            f"مستند FAQ يتجاوز الحد الأقصى ({MAX_DOCUMENT_BYTES} بايت)."
        )
    if not isinstance(payload, dict):
        raise FaqValidationError("الجذر يجب أن يكون كائناً JSON.")

    expected_document_keys = {"version", "entries"}
    if set(payload) != expected_document_keys:
        raise FaqValidationError("يتطلب المستند الحقول version و entries فقط.")
    if payload["version"] != FAQ_SCHEMA_VERSION:
        raise FaqValidationError(f"الإصدار المدعوم هو {FAQ_SCHEMA_VERSION}.")
    if not isinstance(payload["entries"], list):
        raise FaqValidationError("entries يجب أن يكون قائمة.")
    if len(payload["entries"]) > MAX_ENTRIES:
        raise FaqValidationError(f"الحد الأقصى هو {MAX_ENTRIES} سؤالاً.")

    normalized_entries: List[Dict[str, Any]] = []
    entry_ids = set()
    normalized_questions = set()
    for position, entry in enumerate(payload["entries"], start=1):
        if not isinstance(entry, dict):
            raise FaqValidationError(f"السجل {position} يجب أن يكون كائناً JSON.")
        expected_entry_keys = {"id", "question", "answer", "keywords"}
        if set(entry) != expected_entry_keys:
            raise FaqValidationError(
                f"السجل {position} يتطلب id و question و answer و keywords فقط."
            )

        entry_id = entry["id"]
        if not isinstance(entry_id, str) or not _ENTRY_ID_PATTERN.fullmatch(entry_id):
            raise FaqValidationError(
                f"معرّف السجل {position} يجب أن يكون أحرفاً أو أرقاماً أو - أو _."
            )
        if entry_id in entry_ids:
            raise FaqValidationError(f"معرّف السجل مكرر: {entry_id}.")

        question = _clean_text(entry["question"], "question", MAX_QUESTION_CHARS)
        answer = _clean_text(entry["answer"], "answer", MAX_ANSWER_CHARS)
        normalized_question = normalize_for_match(question)
        if len(normalized_question) < 2:
            raise FaqValidationError(f"question في السجل {position} قصير جداً للمطابقة.")
        if normalized_question in normalized_questions:
            raise FaqValidationError(f"question مكرر في السجل {position}.")

        keywords_value = entry["keywords"]
        if not isinstance(keywords_value, list):
            raise FaqValidationError(f"keywords في السجل {position} يجب أن تكون قائمة.")
        if len(keywords_value) > MAX_KEYWORDS_PER_ENTRY:
            raise FaqValidationError(
                f"keywords في السجل {position} تتجاوز الحد ({MAX_KEYWORDS_PER_ENTRY})."
            )

        keywords: List[str] = []
        normalized_keywords = set()
        for keyword in keywords_value:
            clean_keyword = _clean_text(keyword, "keyword", MAX_KEYWORD_CHARS)
            match_keyword = normalize_for_match(clean_keyword)
            if len(match_keyword) < 2:
                raise FaqValidationError("كل keyword يجب أن يصلح للمطابقة النصية.")
            if match_keyword in normalized_keywords:
                raise FaqValidationError(f"keywords مكررة في السجل {position}.")
            normalized_keywords.add(match_keyword)
            keywords.append(clean_keyword)

        entry_ids.add(entry_id)
        normalized_questions.add(normalized_question)
        normalized_entries.append(
            {
                "id": entry_id,
                "question": question,
                "answer": answer,
                "keywords": keywords,
            }
        )

    normalized_document = {"version": FAQ_SCHEMA_VERSION, "entries": normalized_entries}
    if _serialized_size(normalized_document) > MAX_DOCUMENT_BYTES:
        raise FaqValidationError(
            f"مستند FAQ بعد التطبيع يتجاوز الحد ({MAX_DOCUMENT_BYTES} بايت)."
        )
    return normalized_document


def find_faq_answer(message: str, document: Dict[str, Any]) -> Optional[str]:
    """مطابقة سؤال محلياً / Return the best local FAQ answer without code execution."""

    if not isinstance(message, str):
        return None
    normalized_message = normalize_for_match(message)
    if not normalized_message:
        return None

    message_terms = set(normalized_message.split())
    best_score = -1
    best_answer: Optional[str] = None
    for entry in document.get("entries", []):
        candidates = [entry.get("question", "")] + entry.get("keywords", [])
        for candidate in candidates:
            if not isinstance(candidate, str):
                continue
            normalized_candidate = normalize_for_match(candidate)
            if not normalized_candidate:
                continue
            candidate_terms = set(normalized_candidate.split())
            if normalized_candidate == normalized_message:
                score = 10_000 + len(candidate_terms)
            elif len(candidate_terms) >= 2 and normalized_candidate in normalized_message:
                score = 5_000 + len(candidate_terms)
            elif len(message_terms) >= 2 and message_terms.issubset(candidate_terms):
                score = 2_000 + len(message_terms)
            else:
                continue
            if score > best_score:
                best_score = score
                answer = entry.get("answer")
                best_answer = answer if isinstance(answer, str) else None
    return best_answer


def resolve_pro_entitlement(app: Any, http_request: Any) -> EntitlementDecision:
    """التحقق الخادمي المغلق / Resolve a server-side entitlement and fail closed."""

    verifier = app.config.get("ENTITLEMENT_VERIFIER")
    if verifier is None or not callable(getattr(verifier, "verify", None)):
        return EntitlementDecision(state=_CONFIGURATION_REQUIRED)

    try:
        decision = verifier.verify(http_request)
    except Exception:
        return EntitlementDecision(state=_UNAVAILABLE)

    if not isinstance(decision, EntitlementDecision):
        return EntitlementDecision(state=_UNAVAILABLE)
    if decision.state not in _ALLOWED_ENTITLEMENT_STATES:
        return EntitlementDecision(state=_UNAVAILABLE)
    if decision.state != _ACTIVE:
        return EntitlementDecision(state=decision.state)

    if not isinstance(decision.account_id, str) or not decision.account_id.strip():
        return EntitlementDecision(state=_UNAVAILABLE)
    if len(decision.account_id) > 256:
        return EntitlementDecision(state=_UNAVAILABLE)
    if not isinstance(decision.subscription_id, str) or not decision.subscription_id.strip():
        return EntitlementDecision(state=_UNAVAILABLE)
    if not isinstance(decision.expires_at, datetime) or decision.expires_at.tzinfo is None:
        return EntitlementDecision(state=_UNAVAILABLE)
    if decision.expires_at.astimezone(timezone.utc) <= datetime.now(timezone.utc):
        return EntitlementDecision(state=_EXPIRED)
    return decision


def entitlement_error(decision: EntitlementDecision) -> Dict[str, Any]:
    """رسالة عامة آمنة / Produce a safe public error for a denied entitlement."""

    messages = {
        _CONFIGURATION_REQUIRED: "شراء برو والتحقق الخادمي غير مُعَدّين بعد.",
        _UNAUTHENTICATED: "سجّل الدخول بحسابك للوصول إلى قاعدة الأسئلة الشائعة المخصصة.",
        _NOT_ENTITLED: "تتطلب قاعدة الأسئلة الشائعة المخصصة اشتراك برو نشطاً.",
        _EXPIRED: "انتهى اشتراك برو؛ لا يمكن الوصول إلى قاعدة الأسئلة الشائعة المخصصة.",
        _CANCELLED: "أُلغي اشتراك برو؛ لا يمكن الوصول إلى قاعدة الأسئلة الشائعة المخصصة.",
        _UNAVAILABLE: "تعذر التحقق من استحقاق برو بأمان. حاول لاحقاً.",
    }
    status_codes = {
        _CONFIGURATION_REQUIRED: 503,
        _UNAUTHENTICATED: 401,
        _NOT_ENTITLED: 403,
        _EXPIRED: 403,
        _CANCELLED: 403,
        _UNAVAILABLE: 503,
    }
    return {
        "error": {
            "code": decision.state,
            "message": messages.get(decision.state, messages[_UNAVAILABLE]),
            "status": status_codes.get(decision.state, 503),
        }
    }


class FileFaqStore:
    """مخزن FAQ خاص بالحساب / Atomic account-owned JSON FAQ storage."""

    def __init__(self, storage_directory: str):
        """تهيئة مسار خاص / Initialize the private storage directory."""

        self.storage_directory = os.path.abspath(storage_directory)
        self._thread_lock = threading.RLock()

    def _document_path(self, account_id: str) -> str:
        """اشتقاق اسم ملف غير كاشف / Derive a non-disclosing filename for one account."""

        if not isinstance(account_id, str) or not account_id.strip():
            raise FaqStorageError("هوية الحساب غير صالحة.")
        digest = hashlib.sha256(account_id.encode("utf-8")).hexdigest()
        return os.path.join(self.storage_directory, f"{digest}.json")

    def _read_document(self, account_id: str) -> Dict[str, Any]:
        """قراءة وثيقة حساب والتحقق منها / Read and validate one account document."""

        document_path = self._document_path(account_id)
        if not os.path.exists(document_path):
            return default_faq_document()
        try:
            with open(document_path, "r", encoding="utf-8") as file_handle:
                payload = json.load(file_handle)
            return validate_faq_document(payload)
        except (OSError, json.JSONDecodeError, FaqValidationError) as error:
            raise FaqStorageError("تعذر قراءة قاعدة الأسئلة الشائعة بأمان.") from error

    def _write_document(self, account_id: str, document: Dict[str, Any]) -> None:
        """كتابة ذرية محلية / Atomically write a validated document with private permissions."""

        os.makedirs(self.storage_directory, mode=0o700, exist_ok=True)
        document_path = self._document_path(account_id)
        descriptor = -1
        temporary_path = ""
        try:
            descriptor, temporary_path = tempfile.mkstemp(
                prefix=".faq-", suffix=".tmp", dir=self.storage_directory
            )
            with os.fdopen(descriptor, "w", encoding="utf-8") as file_handle:
                descriptor = -1
                os.fchmod(file_handle.fileno(), 0o600)
                json.dump(document, file_handle, ensure_ascii=False, indent=2)
                file_handle.write("\n")
                file_handle.flush()
                os.fsync(file_handle.fileno())
            os.replace(temporary_path, document_path)
        except OSError as error:
            raise FaqStorageError("تعذر حفظ قاعدة الأسئلة الشائعة بأمان.") from error
        finally:
            if descriptor != -1:
                os.close(descriptor)
            if temporary_path and os.path.exists(temporary_path):
                os.unlink(temporary_path)

    def load(self, account_id: str) -> Dict[str, Any]:
        """تحميل FAQ للحساب / Load the FAQ document belonging to one verified account."""

        with self._thread_lock:
            return self._read_document(account_id)

    def merge(self, account_id: str, incoming_document: Any) -> Dict[str, int]:
        """دمج سجلات FAQ حسب id / Merge validated incoming entries by their stable IDs."""

        incoming = validate_faq_document(incoming_document)
        with self._thread_lock:
            current = self._read_document(account_id)
            entries = list(current["entries"])
            positions = {entry["id"]: index for index, entry in enumerate(entries)}
            added = 0
            updated = 0
            for incoming_entry in incoming["entries"]:
                entry_id = incoming_entry["id"]
                if entry_id in positions:
                    entries[positions[entry_id]] = incoming_entry
                    updated += 1
                else:
                    positions[entry_id] = len(entries)
                    entries.append(incoming_entry)
                    added += 1

            merged_document = validate_faq_document(
                {"version": FAQ_SCHEMA_VERSION, "entries": entries}
            )
            self._write_document(account_id, merged_document)
            return {"added": added, "updated": updated, "total": len(entries)}
