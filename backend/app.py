"""
⚡ مروق AI الكمومي - Quantum AI Backend
Flask API مع دعم Kimi AI + Weather + Time
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
import random
import datetime
from datetime import timedelta
import requests

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# ===== إعدادات API =====
KIMI_API_KEY = os.getenv('KIMI_API_KEY', '')
KIMI_API_URL = 'https://api.moonshot.cn/v1/chat/completions'
WEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')

# ===== المسارات =====

@app.route('/')
def serve_frontend():
    """خدمة الواجهة الأمامية"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """الملفات الثابتة"""
    return send_from_directory('../frontend', path)

@app.route('/api/assistant/info')
def assistant_info():
    """معلومات المساعد"""
    return jsonify({
        "status": "quantum-active",
        "name": "مروق AI الكمومي",
        "version": "2.0.0-Quantum",
        "languages": ["ar", "en", "fr", "es", "de", "zh", "ja", "ru", "tr", "ur"],
        "features": ["chat", "voice", "weather", "time", "touch", "kimi"],
        "server_time": datetime.datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """محادثة مع Kimi AI"""
    data = request.json or {}
    message = data.get('message', '').strip()
    lang = data.get('lang', 'ar')

    if not message:
        return jsonify({"error": "Empty message"}), 400

    # محاولة الاتصال بـ Kimi API
    kimi_response = ask_kimi_ai(message, lang)

    if kimi_response:
        return jsonify({
            "status": "success",
            "source": "kimi-ai",
            "response": kimi_response,
            "lang": lang,
            "timestamp": datetime.datetime.now().isoformat()
        })

    # رد احتياطي من الدماغ الكمومي
    return jsonify({
        "status": "success",
        "source": "quantum-brain",
        "response": quantum_brain_response(message, lang),
        "lang": lang,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/weather')
def get_weather():
    """الطقس"""
    city = request.args.get('city', 'Riyadh')

    # محاكاة بيانات الطقس
    conditions = [
        {"icon": "☀️", "desc": "مشمس", "temp": 32, "humidity": 45, "wind": 12, "visibility": 10},
        {"icon": "⛅", "desc": "غائم جزئياً", "temp": 28, "humidity": 55, "wind": 15, "visibility": 9},
        {"icon": "☁️", "desc": "غائم", "temp": 25, "humidity": 65, "wind": 18, "visibility": 7},
    ]
    w = random.choice(conditions)

    return jsonify({
        "status": "success",
        "city": city,
        "weather": w,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/time')
def get_time():
    """الوقت"""
    now = datetime.datetime.now()
    return jsonify({
        "status": "success",
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "day": now.strftime("%A"),
        "timestamp": int(now.timestamp())
    })

# ===== Kimi AI Integration =====

def ask_kimi_ai(question, lang):
    """السؤال Kimi AI عبر API"""
    if not KIMI_API_KEY or KIMI_API_KEY == 'YOUR_KIMI_API_KEY':
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
        response = requests.post(
            KIMI_API_URL,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {KIMI_API_KEY}'
            },
            json={
                'model': 'moonshot-v1-8k',
                'messages': [
                    {'role': 'system', 'content': system_prompts.get(lang, system_prompts['en'])},
                    {'role': 'user', 'content': question}
                ],
                'temperature': 0.7,
                'max_tokens': 1000
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            print(f'Kimi API Error: {response.status_code} - {response.text}')
            return None

    except Exception as e:
        print(f'Kimi Connection Error: {e}')
        return None

def quantum_brain_response(message, lang):
    """رد الدماغ الكمومي الاحتياطي"""
    responses = {
        'ar': f'⚡ فهمت سؤالك: "{message[:40]}..." أنا أتعلم باستمرار! جرب الاتصال بـ Kimi API للردود الأذكى.',
        'en': f'⚡ Got your question: "{message[:40]}..." I'm constantly learning! Try connecting Kimi API for smarter responses.',
        'fr': f'⚡ J'ai compris: "{message[:40]}..." J'apprends constamment!',
        'es': f'⚡ Entendí: "{message[:40]}..." ¡Aprendo constantemente!',
        'de': f'⚡ Verstanden: "{message[:40]}..." Ich lerne ständig!',
        'zh': f'⚡ 明白了："{message[:40]}..." 我在不断学习！',
        'ja': f'⚡ 了解："{message[:40]}..." 絶えず学んでいます！',
        'ru': f'⚡ Понял: "{message[:40]}..." Я постоянно учусь!',
        'tr': f'⚡ Anladım: "{message[:40]}..." Sürekli öğreniyorum!',
        'ur': f'⚡ سمجھا: "{message[:40]}..." میں مسلسل سیکھ رہا ہوں!'
    }
    return responses.get(lang, responses['en'])

# ===== تشغيل =====
if __name__ == '__main__':
    print("⚡ مروق AI الكمومي - Quantum Backend")
    print(f"🔮 Kimi API: {'متصل' if KIMI_API_KEY else 'غير متصل (أضف KIMI_API_KEY)'}")
    print("🚀 http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
