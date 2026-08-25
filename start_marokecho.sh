#!/bin/bash
clear
echo "╔══════════════════════════════════════════╗"
echo "║  ⚡ مروق AI الكمومي v3.0 — التشغيل الشامل  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

cd /storage/emulated/0/mrook_echo

# 1. قتل العمليات القديمة
echo "🔴 إيقاف العمليات القديمة..."
pkill -9 -f "python3 app.py" 2>/dev/null
pkill -9 -f "python" 2>/dev/null
sleep 2

# 2. التأكد من .env
echo "🔑 التحقق من المفاتيح..."
if [ ! -f .env ]; then
    echo "   ❌ .env غير موجود!"
    echo "   ➡️  انسخ .env.template إلى .env وأضف مفتاح Gemini"
    exit 1
fi

# 3. تحميل المفاتيح
export $(grep -v '^#' .env | xargs 2>/dev/null)
if [ -z "$GEMINI_API_KEY" ]; then
    echo "   ❌ GEMINI_API_KEY فارغ!"
    exit 1
fi
echo "   ✅ Gemini: ${GEMINI_API_KEY:0:20}..."

# 4. تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip install flask flask-cors requests python-dotenv -q 2>/dev/null

# 5. التحقق من الملفات
if [ ! -f backend/app.py ]; then
    echo "   ❌ backend/app.py غير موجود!"
    exit 1
fi

if [ ! -f index.html ]; then
    echo "   ❌ index.html غير موجود!"
    exit 1
fi

# 6. تشغيل الخادم
echo ""
echo "=========================================="
echo "🚀 تشغيل الخادم على المنفذ 5002..."
echo "=========================================="
echo ""
echo "📱 افتح المتصفح على:"
echo "   http://localhost:5002"
echo "   http://127.0.0.1:5002"
echo ""
cd backend
python3 app.py
