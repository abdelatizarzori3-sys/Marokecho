#!/bin/bash
clear
echo "=========================================="
echo "⚡ مروق AI الكمومي - باتش الإصلاح الشامل"
echo "=========================================="
echo ""

cd /storage/emulated/0/mrook_echo/backend

# 1. قتل العمليات القديمة
echo "🔴 إيقاف العمليات القديمة..."
pkill -9 -f "python3 app.py" 2>/dev/null
sleep 1

# 2. تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip install flask flask-cors requests python-dotenv -q 2>/dev/null

# 3. إنشاء app.py صحيح
echo "📝 إنشاء app.py المُحدّث..."
cat > app.py << 'PYEOF'
"""
⚡ مروق AI الكمومي - Quantum AI Backend
Flask API مع دعم Gemini AI المجاني 100%
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import random
import datetime
import requests

# المجلد الأمامي (frontend) هو مجلد الأب
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..')

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'

@app.route('/')
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/api/assistant/info')
def assistant_info():
    return jsonify({
        "status": "quantum-active",
        "name": "مروق AI الكمومي",
        "version": "2.0.0-Quantum",
        "languages": ["ar", "en", "fr", "es", "de", "zh", "ja", "ru", "tr", "ur"],
        "features": ["chat", "voice", "weather", "time", "touch", "gemini"],
        "server_time": datetime.datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    msg = data.get('message', '').strip()
    lang = data.get('lang', 'ar')
    if not msg:
        return jsonify({"error": "Empty message"}), 400

    gemini_response = ask_gemini_ai(msg, lang)
    if gemini_response:
        return jsonify({
            "status": "success",
            "source": "gemini-ai",
            "response": gemini_response,
            "lang": lang,
            "timestamp": datetime.datetime.now().isoformat()
        })

    return jsonify({
        "status": "success",
        "source": "quantum-brain",
        "response": f"⚡ فهمت: '{msg[:40]}...' جرب توصيل Gemini API!",
        "lang": lang,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/weather')
def get_weather():
    city = request.args.get('city', 'Riyadh')
    conditions = [
        {"icon": "☀️", "desc": "مشمس", "temp": 32, "humidity": 45, "wind": 12, "visibility": 10},
        {"icon": "⛅", "desc": "غائم جزئياً", "temp": 28, "humidity": 55, "wind": 15, "visibility": 9},
        {"icon": "☁️", "desc": "غائم", "temp": 25, "humidity": 65, "wind": 18, "visibility": 7},
    ]
    w = random.choice(conditions)
    return jsonify({
        "status": "success", "city": city, "weather": w,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/time')
def get_time():
    now = datetime.datetime.now()
    return jsonify({
        "status": "success",
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "day": now.strftime("%A"),
        "timestamp": int(now.timestamp())
    })

def ask_gemini_ai(question, lang):
    if not GEMINI_API_KEY:
        return None
    system_prompts = {
        'ar': 'أنت مروق، مساعد ذكاء اصطناعي كمومي متطور. تتحدث بأسلوب مستقبلي، ودي، وذكي. أجب باللغة العربية.',
        'en': 'You are Mrook, an advanced quantum AI assistant. Speak in a futuristic, friendly, and smart manner. Answer in English.',
        'fr': 'Vous êtes Mrook, un assistant IA quantique avancé. Répondez en français.',
        'es': 'Eres Mrook, un asistente de IA cuántico avanzado. Responde en español.',
        'de': 'Du bist Mrook, ein fortschrittlicher quanten KI-Assistent. Antworte auf Deutsch.',
        'zh': '你是Mrook，一个先进的量子AI助手。用中文回答。',
        'ja': 'あなたはMrook、高度な量子AIアシスタントです。日本語で答えてください。',
        'ru': 'Ты Mrook, продвинутый квантовый ИИ-ассистент. Отвечай на русском.',
        'tr': 'Sen Mrook, gelişmiş bir kuantum yapay zeka asistanısın. Türkçe cevap ver.',
        'ur': 'تم مروق ہو، ایک جدید کوانٹم AI اسسٹنٹ۔ اردو میں جواب دو۔'
    }
    try:
        url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
        prompt = system_prompts.get(lang, system_prompts['en'])
        r = requests.post(url, headers={'Content-Type': 'application/json'},
            json={"contents": [{"parts": [{"text": f"{prompt}\n\nالسؤال: {question}"}]}]},
            timeout=30)
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f'Gemini Error: {r.status_code}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None

if __name__ == '__main__':
    print("⚡ مروق AI الكمومي - Quantum Backend")
    print(f"🔮 Gemini API: {'متصل ✅' if GEMINI_API_KEY else 'غير متصل ❌'}")
    print("🚀 http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
PYEOF

# 4. التحقق من المفتاح
echo ""
echo "🔑 التحقق من Gemini API Key..."
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
k = os.getenv('GEMINI_API_KEY')
print('   الحالة:', '✅ موجود' if k else '❌ غير موجود في .env')
if k:
    print('   البداية:', k[:20] + '...')
"

# 5. تشغيل الخادم
echo ""
echo "=========================================="
echo "🚀 تشغيل الخادم على المنفذ 5001..."
echo "=========================================="
echo ""
python3 app.py
