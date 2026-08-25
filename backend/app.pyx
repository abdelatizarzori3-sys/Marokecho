#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ مروق AI الكمومي v3.0 — Multi-Engine Quantum Backend
"""
import os
import sys
import json
import time
import requests
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# تحميل .env من المجلد الأب (الجذر)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

from components import QuantumMemory, QuantumEngine

app = Flask(__name__, static_folder="..")
CORS(app)

memory = QuantumMemory()
engine = QuantumEngine()

PORT = int(os.environ.get("PORT", "5002"))
HOST = os.environ.get("HOST", "0.0.0.0")

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")


def call_gemini(message, lang="ar"):
    """استدعاء Gemini API"""
    if not GEMINI_KEY:
        return None, "مفتاح Gemini غير مُعدّ"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [{"parts": [{"text": message}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
        }
        r = requests.post(url, json=payload, timeout=30)
        data = r.json()
        if "candidates" in data and data["candidates"]:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text, None
        return None, "رد فارغ من Gemini"
    except Exception as e:
        return None, str(e)


def call_groq(message, lang="ar"):
    """استدعاء Groq API"""
    if not GROQ_KEY:
        return None, "مفتاح Groq غير مُعدّ"
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7
        }
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        data = r.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"], None
        return None, "رد فارغ من Groq"
    except Exception as e:
        return None, str(e)


def call_openrouter(message, lang="ar"):
    """استدعاء OpenRouter API"""
    if not OPENROUTER_KEY:
        return None, "مفتاح OpenRouter غير مُعدّ"
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5002",
            "X-Title": "Mrook Echo AI"
        }
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": message}]
        }
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        data = r.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"], None
        return None, "رد فارغ من OpenRouter"
    except Exception as e:
        return None, str(e)


# ─── المسارات ───────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("..", "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("..", filename)


@app.route("/api/status")
def status():
    return jsonify({
        "name": "مروق AI الكمومي v3.0",
        "status": "online",
        "time": datetime.now().isoformat(),
        "engines": {
            "gemini": {"active": bool(GEMINI_KEY), "status": "✅" if GEMINI_KEY else "❌"},
            "groq": {"active": bool(GROQ_KEY), "status": "✅" if GROQ_KEY else "❌"},
            "openrouter": {"active": bool(OPENROUTER_KEY), "status": "✅" if OPENROUTER_KEY else "❌"}
        },
        "memory": memory.get_stats()
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    lang = data.get("lang", "ar")
    preferred_engine = data.get("engine", "gemini")

    if not message:
        return jsonify({"error": "الرسالة فارغة"}), 400

    # حفظ رسالة المستخدم
    memory.add_message("user", message, preferred_engine)

    # اختيار المحرك
    selected = engine.select_engine(message, preferred_engine)

    # استدعاء المحرك
    reply = None
    error = None

    engines_order = [selected]
    for e in ["gemini", "groq", "openrouter"]:
        if e not in engines_order:
            engines_order.append(e)

    for eng in engines_order:
        if eng == "gemini" and GEMINI_KEY:
            reply, error = call_gemini(message, lang)
        elif eng == "groq" and GROQ_KEY:
            reply, error = call_groq(message, lang)
        elif eng == "openrouter" and OPENROUTER_KEY:
            reply, error = call_openrouter(message, lang)

        if reply:
            selected = eng
            break

    if not reply:
        reply = f"عذراً، لا يمكنني الرد الآن. ({error or 'جميع المحركات غير متصلة'})"
        selected = "fallback"

    # حفظ الرد
    memory.add_message("assistant", reply, selected)

    return jsonify({
        "reply": reply,
        "engine": selected,
        "lang": lang,
        "quantum": engine.process(message, lang, selected),
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/history")
def history():
    return jsonify({
        "conversations": memory.get_context(50),
        "stats": memory.get_stats()
    })


@app.route("/api/clear", methods=["POST"])
def clear():
    memory.conversations = []
    memory.save()
    return jsonify({"status": "cleared"})


# ─── التشغيل ───────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("⚡ مروق AI الكمومي v3.0 — Multi-Engine Quantum Backend")
    print(f"🔮 Gemini: {'✅' if GEMINI_KEY else '❌'} | Groq: {'✅' if GROQ_KEY else '❌'} | OpenRouter: {'✅' if OPENROUTER_KEY else '❌'}")
    print(f"🧠 محادثات سابقة: {len(memory.conversations)}")
    print(f"🚀 http://localhost:{PORT}")
    print("=" * 50)
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)
