"""
اختبارات تطبيق مروق ايكو الخارق
Mrook Echo - Test Suite
"""
import unittest
import tkinter as tk
from tkinter import ttk
import json
import os
import sys

# إضافة المسار
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import MrookEcho
from components import ValidationEntry, StatusBar, ProgressCard


class TestValidationEntry(unittest.TestCase):
    """اختبارات حقل الإدخال مع التحقق"""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_integer_validation(self):
        """التحقق من إدخال الأعداد الصحيحة"""
        entry = ValidationEntry(self.root, validate_type="int")
        self.assertTrue(entry.validate("123"))
        self.assertTrue(entry.validate("0"))
        self.assertTrue(entry.validate(""))
        self.assertFalse(entry.validate("abc"))
        self.assertFalse(entry.validate("12.5"))

    def test_float_validation(self):
        """التحقق من إدخال الأعداد العشرية"""
        entry = ValidationEntry(self.root, validate_type="float")
        self.assertTrue(entry.validate("12.5"))
        self.assertTrue(entry.validate("3.14"))
        self.assertTrue(entry.validate("100"))
        self.assertFalse(entry.validate("abc"))

    def test_text_validation(self):
        """التحقق من إدخال النصوص"""
        entry = ValidationEntry(self.root, validate_type="text")
        self.assertTrue(entry.validate("مرحبا"))
        self.assertTrue(entry.validate("Hello"))
        self.assertFalse(entry.validate("@#$"))


class TestMrookEcho(unittest.TestCase):
    """اختبارات التطبيق الرئيسي"""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = MrookEcho(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initial_values(self):
        """التحقق من القيم الأولية"""
        self.assertEqual(self.app.time_var.get(), "0")
        self.assertEqual(self.app.energy_var.get(), "0")

    def test_validate_input_empty(self):
        """التحقق من رفض القيم الفارغة"""
        result = self.app.validate_input("", "اختبار")
        self.assertIsNone(result)

    def test_validate_input_negative(self):
        """التحقق من رفض القيم السالبة"""
        result = self.app.validate_input("-5", "اختبار")
        self.assertIsNone(result)

    def test_validate_input_valid(self):
        """التحقق من قبول القيم الصحيحة"""
        result = self.app.validate_input("42", "اختبار")
        self.assertEqual(result, 42)

    def test_validate_input_non_numeric(self):
        """التحقق من رفض القيم غير الرقمية"""
        result = self.app.validate_input("abc", "اختبار")
        self.assertIsNone(result)

    def test_reset_values(self):
        """التحقق من إعادة التعيين"""
        self.app.time_var.set("50")
        self.app.energy_var.set("75")
        self.app.reset_values()
        self.assertEqual(self.app.time_var.get(), "0")
        self.assertEqual(self.app.energy_var.get(), "0")

    def test_update_status(self):
        """التحقق من تحديث الحالة"""
        test_message = "اختبار الحالة"
        self.app.update_status(test_message)
        self.assertEqual(self.app.status_var.get(), test_message)


class TestDataFiles(unittest.TestCase):
    """اختبارات ملفات البيانات"""

    def test_data_json_exists(self):
        """التحقق من وجود ملف data.json"""
        self.assertTrue(os.path.exists("data.json"))

    def test_settings_json_exists(self):
        """التحقق من وجود ملف settings.json"""
        self.assertTrue(os.path.exists("settings.json"))

    def test_data_json_valid(self):
        """التحقق من صحة بيانات data.json"""
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("features", data)
        self.assertIn("settings", data)
        self.assertIsInstance(data["features"], list)

    def test_settings_json_valid(self):
        """التحقق من صحة بيانات settings.json"""
        with open("settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.assertIn("app_name", settings)
        self.assertIn("version", settings)
        self.assertIn("theme", settings)


class TestComponents(unittest.TestCase):
    """اختبارات المكونات"""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_progress_card(self):
        """التحقق من بطاقة التقدم"""
        card = ProgressCard(self.root, title="اختبار", maximum=100)
        card.set_value(50)
        self.assertEqual(card.progress["value"], 50)

    def test_status_bar(self):
        """التحقق من شريط الحالة"""
        status_var = tk.StringVar(value="جاهز")
        status = StatusBar(self.root, textvariable=status_var)
        self.assertEqual(status.activity_var.get(), "●")


def run_tests():
    """تشغيل جميع الاختبارات"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestValidationEntry))
    suite.addTests(loader.loadTestsFromTestCase(TestMrookEcho))
    suite.addTests(loader.loadTestsFromTestCase(TestDataFiles))
    suite.addTests(loader.loadTestsFromTestCase(TestComponents))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
