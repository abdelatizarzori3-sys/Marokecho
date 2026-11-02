# -*- coding: utf-8 -*-
"""خادم مروق المحلي / Marokecho local Flask server."""

import hashlib
import os
from typing import Any, Dict, Optional, Tuple

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge

from components import check_api_key, process_message
from pro_faq import (
    MAX_DOCUMENT_BYTES,
    EntitlementDecision,
    FaqStorageError,
    FaqValidationError,
    FileFaqStore,
    entitlement_error,
    resolve_pro_entitlement,
    validate_faq_document,
)

# Serve frontend files
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_BASE_DIR)
MAX_CHAT_MESSAGE_CHARS = 4_000

app = Flask(__name__, static_folder=_PARENT_DIR, static_url_path="")
# The FAQ JSON document is deliberately small; Flask rejects oversized requests first.
app.config["MAX_CONTENT_LENGTH"] = MAX_DOCUMENT_BYTES


def _faq_store() -> FileFaqStore:
    """إرجاع مخزن FAQ الخاص / Return the configured private FAQ store."""

    configured_store = app.config.get("FAQ_STORE")
    if configured_store is not None:
        return configured_store
    storage_directory = os.path.join(app.instance_path, "faq-content")
    store = FileFaqStore(storage_directory)
    app.config["FAQ_STORE"] = store
    return store


def _pro_chat_session_id(account_id: str) -> str:
    """عزل ذاكرة برو من دون كشف الهوية / Derive a non-disclosing in-memory Pro session ID."""

    digest = hashlib.sha256(account_id.encode("utf-8")).hexdigest()
    return f"pro-faq-{digest}"


def _pro_access() -> Tuple[Optional[EntitlementDecision], Optional[Tuple[Any, int]]]:
    """فرض قرار برو خادمي / Require a verified entitlement or return a safe denial."""

    decision = resolve_pro_entitlement(app, request)
    if decision.state == "active":
        return decision, None
    error = entitlement_error(decision)
    return None, (jsonify(error), error["error"]["status"])


def _json_document_from_request() -> Tuple[Optional[Dict[str, Any]], Optional[Tuple[Any, int]]]:
    """قراءة JSON المخصص بأمان / Read a JSON FAQ document without permissive coercion."""

    if not request.is_json:
        return None, (
            jsonify(
                {
                    "error": {
                        "code": "unsupported_media_type",
                        "message": "أرسل مستند FAQ بصيغة application/json.",
                    }
                }
            ),
            415,
        )
    try:
        payload = request.get_json(silent=False)
    except BadRequest:
        return None, (
            jsonify(
                {
                    "error": {
                        "code": "invalid_json",
                        "message": "تعذر قراءة JSON المرسل.",
                    }
                }
            ),
            400,
        )
    try:
        return validate_faq_document(payload), None
    except FaqValidationError as error:
        return None, (
            jsonify(
                {
                    "error": {
                        "code": "invalid_faq_document",
                        "message": str(error),
                    }
                }
            ),
            400,
        )


@app.errorhandler(RequestEntityTooLarge)
def request_too_large(_: RequestEntityTooLarge):
    """إرجاع خطأ JSON للحجم الزائد / Return a JSON error for oversized requests."""

    return (
        jsonify(
            {
                "error": {
                    "code": "request_too_large",
                    "message": f"الحد الأقصى للطلب هو {MAX_DOCUMENT_BYTES} بايت.",
                }
            }
        ),
        413,
    )


@app.route("/")
def index():
    """تقديم واجهة المحادثة / Serve the chat frontend."""

    return send_from_directory(_PARENT_DIR, "index.html")


@app.route("/api/status")
def status():
    """حالة المحرك المحلي / Return the legacy local engine status."""

    ok, msg = check_api_key()
    return jsonify(
        {
            "status": "online" if ok else "offline",
            "gemini": "connected" if ok else "disconnected",
            "message": msg,
            "version": "4.0",
        }
    )


@app.route("/api/pro/faq/status", methods=["GET"])
def pro_faq_status():
    """فحص استحقاق FAQ بلا كشف بيانات / Check FAQ access without exposing account data."""

    decision, denied_response = _pro_access()
    if denied_response is not None:
        return denied_response
    return jsonify(
        {
            "pro": True,
            "feature": "custom_faq",
            "limits": {"max_document_bytes": MAX_DOCUMENT_BYTES, "max_entries": 100},
        }
    )


@app.route("/api/pro/faq/import", methods=["POST"])
def import_pro_faq():
    """دمج JSON FAQ المراجع / Merge a reviewed, validated FAQ JSON document."""

    decision, denied_response = _pro_access()
    if denied_response is not None:
        return denied_response
    assert decision is not None and decision.account_id is not None
    document, invalid_response = _json_document_from_request()
    if invalid_response is not None:
        return invalid_response
    try:
        result = _faq_store().merge(decision.account_id, document)
    except FaqStorageError:
        return (
            jsonify(
                {
                    "error": {
                        "code": "faq_storage_unavailable",
                        "message": "تعذر حفظ قاعدة الأسئلة الشائعة بأمان. حاول لاحقاً.",
                    }
                }
            ),
            503,
        )
    return jsonify({"ok": True, "result": result})


@app.route("/api/pro/faq/export", methods=["GET"])
def export_pro_faq():
    """تصدير FAQ المملوك للحساب / Export only the verified account's FAQ JSON."""

    decision, denied_response = _pro_access()
    if denied_response is not None:
        return denied_response
    assert decision is not None and decision.account_id is not None
    try:
        document = _faq_store().load(decision.account_id)
    except FaqStorageError:
        return (
            jsonify(
                {
                    "error": {
                        "code": "faq_storage_unavailable",
                        "message": "تعذر قراءة قاعدة الأسئلة الشائعة بأمان. حاول لاحقاً.",
                    }
                }
            ),
            503,
        )
    return jsonify(document)


@app.route("/api/chat", methods=["POST"])
def chat():
    """معالجة محادثة محلية / Process a free local chat with optional verified FAQ data."""

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"reply": "Invalid JSON message"}), 400

    message = data.get("message")
    if not isinstance(message, str) or not message.strip():
        return jsonify({"reply": "Empty message"}), 400
    if len(message) > MAX_CHAT_MESSAGE_CHARS:
        return jsonify({"reply": "Message is too long"}), 400

    language = data.get("lang")
    language = language if language in {"ar", "en"} else None
    custom_faq_document = None
    session_id = "default"
    decision = resolve_pro_entitlement(app, request)
    if decision.state == "active":
        try:
            assert decision.account_id is not None
            custom_faq_document = _faq_store().load(decision.account_id)
            session_id = _pro_chat_session_id(decision.account_id)
        except FaqStorageError:
            # A storage failure never grants or reveals Pro data; free chat remains usable.
            custom_faq_document = None

    reply = process_message(
        message,
        session_id=session_id,
        lang=language,
        custom_faq_document=custom_faq_document,
    )
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
