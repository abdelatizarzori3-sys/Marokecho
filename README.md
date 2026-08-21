# ⚡ مروق ايكو الخارق | Mrook Echo

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](https://github.com)

**نظام إدارة الوقت والطاقة الذكي**

[الواجهة الرئيسية](#-الواجهة-الرئيسية) • [التثبيت](#-التثبيت) • [الاستخدام](#-الاستخدام) • [الاختبارات](#-الاختبارات)

</div>

---

## 📋 نظرة عامة

**مروق ايكو الخارق** هو تطبيق متكامل لإدارة الوقت والطاقة بكفاءة عالية. يوفر واجهة مستخدم سهلة الاستخدام مع:

- ✅ **إدارة الوقت**: تتبع الوقت المستغرق في المهام
- ✅ **مراقبة الطاقة**: متابعة مستوى الطاقة والأداء
- ✅ **حفظ الإعدادات**: حفظ وتحميل الإعدادات تلقائياً
- ✅ **واجهة ويب**: تصميم HTML/CSS تفاعلي وعصري
- ✅ **دعم العربية**: واجهة كاملة باللغة العربية
- ✅ **وضع ليلي**: دعم الوضع الداكن والفاتح

---

## 🚀 الميزات

| الميزة | الوصف | الحالة |
|--------|-------|--------|
| ⏱️ إدارة الوقت | تتبع وتحديث الوقت المستغرق | ✅ مفعل |
| 🔋 مراقبة الطاقة | متابعة مستوى الطاقة | ✅ مفعل |
| 💾 حفظ الإعدادات | حفظ في ملف JSON | ✅ مفعل |
| 🎨 واجهة ويب | HTML/CSS تفاعلي | ✅ جاهز |
| 📊 رسوم بيانية | عرض البيانات بصرياً | 🔄 قيد التطوير |
| 🔔 إشعارات | تنبيهات ذكية | 🔄 قيد التطوير |

---

## 📦 التثبيت

### المتطلبات

```bash
Python >= 3.8
```

### الخطوات

```bash
# 1. استنساخ المستودع
git clone https://github.com/username/mrook-echo.git
cd mrook-echo

# 2. إنشاء بيئة افتراضية (اختياري)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# 3. تثبيت المتطلبات
pip install -r requirements.txt

# 4. تشغيل التطبيق
python app.py
```

---

## 🖥️ الاستخدام

### التطبيق الرئيسي (Tkinter)

```bash
python app.py
```

### الواجهة الرئيسية (HTML)

افتح `main.html` في المتصفح للوصول إلى الصفحة الرئيسية، ثم انقر على **"ابدأ الآن"** للانتقال إلى واجهة التطبيق.

### الاختبارات

```bash
python test.py
```

---

## 📁 هيكل المشروع

```
mrook-echo/
├── app.py              # التطبيق الرئيسي (Tkinter)
├── components.py       # مكونات واجهة المستخدم
├── data.json           # بيانات الميزات والملاحظات
├── settings.json       # إعدادات المستخدم
├── ui.html             # واجهة المستخدم (HTML)
├── ui.css              # تنسيقات واجهة المستخدم
├── ui.js               # سكربتات واجهة المستخدم
├── main.html           # الصفحة الرئيسية
├── main.css            # تنسيقات الصفحة الرئيسية
├── test.py             # اختبارات التطبيق
├── requirements.txt    # المتطلبات
└── README.md           # هذا الملف
```

---

## 🔧 التحسينات المطبقة

### ✅ التحقق من البيانات
- فحص القيم الفارغة
- رفض القيم السالبة
- التحقق من نوع البيانات (أعداد صحيحة)
- التحقق من الحد الأقصى للطاقة (100%)

### ✅ معالجة الأخطاء
- `try...except` في جميع العمليات الحرجة
- رسائل خطأ واضحة بالعربية
- سجل حالة التطبيق

### ✅ التنسيق
- `ttk.Style` لتخصيص المظهر
- ألوان متناسقة وخطوط احترافية
- دعم الوضع الليلي في الواجهة الويب

### ✅ قابلية القراءة
- تعليقات مفصلة بالعربية والإنجليزية
- docstrings لجميع الدوال
- تنظيم واضح للكود

---

## 🧪 الاختبارات

```bash
# تشغيل جميع الاختبارات
python test.py

# النتيجة المتوقعة:
# test_integer_validation (__main__.TestValidationEntry) ... ok
# test_float_validation (__main__.TestValidationEntry) ... ok
# test_initial_values (__main__.TestMrookEcho) ... ok
# test_validate_input_empty (__main__.TestMrookEcho) ... ok
# ...
# ----------------------------------------------------------------------
# Ran 12 tests in 0.XXXs
# OK
```

---

## 🤝 المساهمة

نرحب بمساهماتكم! يرجى اتباع الخطوات التالية:

1. Fork المستودع
2. إنشاء فرع جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push إلى الفرع (`git push origin feature/amazing-feature`)
5. فتح Pull Request

---

## 📄 الترخيص

هذا المشروع مرخص بموجب [MIT License](LICENSE).

---

<div align="center">

**صنع بـ ❤️ في 2026**

⚡ [مروق ايكو الخارق](https://github.com/username/mrook-echo) ⚡

</div>
