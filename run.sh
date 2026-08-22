#!/bin/bash
# ⚡ مروق AI الكمومي v3.0 — سكريبت التشغيل

echo "=========================================="
echo "  ⚡ مروق AI الكمومي v3.0"
echo "  جاري التشغيل..."
echo "=========================================="

# التوجه إلى مجلد المشروع
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# تحميل متغيرات البيئة من .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✅ تم تحميل المفاتيح من .env"
else
    echo "⚠️  ملف .env غير موجود! انسخ .env.template إلى .env وأضف مفاتيحك."
fi

# التوجه إلى backend وتشغيل الخادم
cd backend
python3 app.py
