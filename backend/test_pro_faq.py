# -*- coding: utf-8 -*-
"""اختبارات FAQ برو / Tests for the entitlement-gated custom FAQ feature."""

import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

BACKEND_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIRECTORY not in sys.path:
    sys.path.insert(0, BACKEND_DIRECTORY)

import app as marokecho_app
from components import MathEngine
from pro_faq import MAX_DOCUMENT_BYTES, EntitlementDecision, FileFaqStore


class TestEntitlementVerifier:
    """موفر قرار اختباري فقط / Test-only verifier injected through Flask configuration."""

    def __init__(self, decision):
        """حفظ القرار المراد إرجاعه / Store the explicit test decision."""

        self.decision = decision

    def verify(self, _request):
        """إرجاع قرار ثابت للاختبار / Return a fixed decision for one test."""

        return self.decision


def active_decision(account_id="account-one"):
    """إنشاء استحقاق صالح للاختبار / Build a future-dated verified test entitlement."""

    return EntitlementDecision(
        state="active",
        account_id=account_id,
        subscription_id=f"subscription-{account_id}",
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )


def example_document(answer="الدوام من التاسعة إلى الخامسة."):
    """إرجاع مستند FAQ نموذجي / Return a valid custom FAQ JSON document."""

    return {
        "version": 1,
        "entries": [
            {
                "id": "working-hours",
                "question": "ما هي ساعات العمل؟",
                "answer": answer,
                "keywords": ["ساعات العمل", "الدوام"],
            }
        ],
    }


class CustomFaqApiTests(unittest.TestCase):
    """اختبارات حدود API / Test the custom FAQ HTTP and ownership boundaries."""

    def setUp(self):
        """تهيئة مخزن مؤقت وعزل الإعداد / Set up an isolated temporary Flask FAQ store."""

        self.storage_directory = tempfile.mkdtemp(prefix="marokecho-faq-test-")
        self.app = marokecho_app.app
        self.previous_verifier = self.app.config.pop("ENTITLEMENT_VERIFIER", None)
        self.previous_store = self.app.config.get("FAQ_STORE")
        self.app.config.update(
            TESTING=True,
            FAQ_STORE=FileFaqStore(self.storage_directory),
        )
        self.client = self.app.test_client()

    def tearDown(self):
        """استعادة إعداد Flask / Restore Flask configuration and remove test data."""

        if self.previous_verifier is not None:
            self.app.config["ENTITLEMENT_VERIFIER"] = self.previous_verifier
        else:
            self.app.config.pop("ENTITLEMENT_VERIFIER", None)
        if self.previous_store is not None:
            self.app.config["FAQ_STORE"] = self.previous_store
        else:
            self.app.config.pop("FAQ_STORE", None)
        self.app.config.pop("TESTING", None)
        shutil.rmtree(self.storage_directory)

    def activate(self, account_id="account-one"):
        """حقن استحقاق للاختبار فقط / Inject a test-only verified entitlement."""

        self.app.config["ENTITLEMENT_VERIFIER"] = TestEntitlementVerifier(
            active_decision(account_id)
        )

    def test_feature_fails_closed_without_server_verifier(self):
        """لا تقبل الواجهة ترويسة أو زر كاستحقاق / No client header can grant Pro access."""

        response = self.client.get("/api/pro/faq/status", headers={"X-Pro": "true"})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.get_json()["error"]["code"], "purchase_configuration_required"
        )

        response = self.client.post(
            "/api/pro/faq/import", json=example_document(), headers={"X-Pro": "true"}
        )
        self.assertEqual(response.status_code, 503)

    def test_invalid_schema_and_oversized_answer_are_rejected(self):
        """رفض الحقول غير المراجعة والحدود / Reject unknown fields and oversized answers."""

        self.activate()
        invalid_document = example_document()
        invalid_document["entries"][0]["script"] = "alert(1)"
        response = self.client.post("/api/pro/faq/import", json=invalid_document)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"]["code"], "invalid_faq_document")

        oversized_document = example_document(answer="أ" * 2_001)
        response = self.client.post("/api/pro/faq/import", json=oversized_document)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"]["code"], "invalid_faq_document")

        request_too_large = example_document(answer="أ" * MAX_DOCUMENT_BYTES)
        response = self.client.post("/api/pro/faq/import", json=request_too_large)
        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.get_json()["error"]["code"], "request_too_large")

    def test_import_export_is_account_owned_and_merges_reply(self):
        """يُصدّر الحساب وثيقته فقط وتسبق الإجابة المحلية الرد العام / Enforce ownership and FAQ reply merge."""

        secret_answer = "<b>الدوام الخاص من التاسعة إلى الخامسة.</b>"
        self.activate("account-one")
        response = self.client.post(
            "/api/pro/faq/import", json=example_document(answer=secret_answer)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["result"], {"added": 1, "updated": 0, "total": 1})

        revised_answer = "الدوام المحدّث من العاشرة إلى السادسة."
        response = self.client.post(
            "/api/pro/faq/import", json=example_document(answer=revised_answer)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["result"], {"added": 0, "updated": 1, "total": 1})

        export_response = self.client.get("/api/pro/faq/export")
        self.assertEqual(export_response.status_code, 200)
        exported = export_response.get_json()
        self.assertEqual(exported["entries"][0]["answer"], revised_answer)
        self.assertNotIn("account-one", exported)
        self.assertNotIn("path", exported)

        chat_response = self.client.post(
            "/api/chat", json={"message": "ساعات العمل", "lang": "ar"}
        )
        self.assertEqual(chat_response.status_code, 200)
        self.assertEqual(chat_response.get_json()["reply"], revised_answer)

        self.activate("account-two")
        second_export = self.client.get("/api/pro/faq/export")
        self.assertEqual(second_export.status_code, 200)
        self.assertEqual(second_export.get_json(), {"version": 1, "entries": []})
        second_chat = self.client.post(
            "/api/chat", json={"message": "ساعات العمل", "lang": "ar"}
        )
        self.assertNotEqual(second_chat.get_json()["reply"], revised_answer)

    def test_expired_entitlement_cannot_read_or_write(self):
        """رفض الاستحقاق المنتهي / Deny read and write access for expired subscriptions."""

        expired = EntitlementDecision(
            state="active",
            account_id="expired-account",
            subscription_id="expired-subscription",
            expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
        )
        self.app.config["ENTITLEMENT_VERIFIER"] = TestEntitlementVerifier(expired)
        response = self.client.get("/api/pro/faq/export")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()["error"]["code"], "expired")


class ArithmeticSafetyTests(unittest.TestCase):
    """اختبارات إزالة التنفيذ / Test that arithmetic no longer evaluates arbitrary Python."""

    def test_limited_arithmetic_works_without_python_eval(self):
        """قبول الحساب المقيد ورفض استدعاء بايثون / Allow math but reject Python execution syntax."""

        self.assertEqual(MathEngine.safe_eval("2 + 2 * 5"), 12)
        self.assertIsNone(MathEngine.safe_eval("__import__('os').system('id')"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
