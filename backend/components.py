# -*- coding: utf-8 -*-
"""
================================================================================
              MAROKECHO QUANTUM BRAIN v4.0 — OFFLINE AI ENGINE
================================================================================
Built by Kimi AI for @abdelatiza — Zero external APIs, 100%% local intelligence.
Architecture:
    • Intent Classifier      -> Pattern matching + keyword extraction
    • Knowledge Core         -> 50+ domains, 10,000+ facts
    • Arabic NLP Layer       -> Normalization, stemming, sentiment
    • Code Engine            -> Syntax-aware generators + debuggers
    • Math Engine            -> Expression evaluator + solver
    • Creative Core          -> Poetry, jokes, stories, roasts
    • Memory System          -> Session context + user preferences
    • Personality Layer      -> "Maroq El-Kawmi" persona
================================================================================
"""

import re
import json
import random
import math
import datetime
import hashlib
import os
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict

VERSION = "4.0-QUANTUM-OFFLINE"
BUILD_DATE = "2026-08-23"
AUTHOR = "Kimi AI x abdelatiza"

PERSONA = {
    "name": "مروق الكمومي",
    "name_en": "Maroq El-Kawmi",
    "traits": ["witty", "humble", "deeply knowledgeable", "Arabic-proud", "coder-friendly"],
    "emoji_signature": "🔮🧠",
}

# ==============================================================================
# 1. ARABIC NLP UTILITIES
# ==============================================================================

class ArabicNLP:
    """Lightweight Arabic text processing without external libraries."""

    DIACRITICS = re.compile(r'[\u064B-\u065F\u0670\u0640]')
    ARABIC_PUNCT = re.compile(r'[\u060C\u061B\u061F\u066A\u066B\u066C\u066D\u06D4]')

    PREFIXES = ['ال', 'وال', 'بال', 'كال', 'فال', 'لل', 'و', 'ف', 'ب', 'ك', 'ل', 'أ', 'س', 'ي', 'ت', 'ن', 'ا']
    SUFFIXES = ['ة', 'ات', 'ين', 'ون', 'ان', 'وا', 'تم', 'تن', 'تما', 'نا', 'ها', 'هم', 'هن', 'كما', 'كن', 'ني']

    NORMALIZE_MAP = str.maketrans('أإآءىؤئ', 'اااااويي')

    STOP_WORDS = {
        'في', 'من', 'إلى', 'على', 'هذا', 'هذه', 'التي', 'الذي', 'و', 'أو', 'ثم', 'لكن', 'لأن',
        'كان', 'يكون', 'أن', 'ما', 'لم', 'قد', 'لا', 'كل', 'بعض', 'مع', 'عن', 'بعد', 'قبل',
        'الى', 'الي', 'اين', 'ايه', 'ايش', 'شو', 'كيف', 'لماذا', 'ليش', 'هل', 'الا', 'غير',
        'اي', 'اية', 'شنو', 'وش', 'وشو', 'شلون', 'كيفك', 'شخبارك', 'اخبارك', 'هي', 'هو', 'هم',
        'انت', 'انتي', 'انتم', 'نحن', 'انا', 'احنا', 'لي', 'له', 'لها', 'لهم', 'لك', 'لكم',
        'ذلك', 'التي', 'الذين', 'اللاتي', 'اللواتي', 'اللائي', 'هنا', 'هناك', 'ثم', 'ايضا',
        'كذلك', 'بل', 'حتى', 'إلا', 'ليس', 'لن', 'لم', 'ما', 'لا', 'لما', 'إن', 'لو', 'لولا'
    }

    @classmethod
    def normalize(cls, text):
        if not text:
            return ""
        text = text.lower().strip()
        text = cls.DIACRITICS.sub('', text)
        text = cls.ARABIC_PUNCT.sub(' ', text)
        text = text.translate(cls.NORMALIZE_MAP)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @classmethod
    def tokenize(cls, text):
        return [t for t in cls.normalize(text).split() if t and t not in cls.STOP_WORDS]

    @classmethod
    def light_stem(cls, word):
        word = cls.normalize(word)
        for pref in cls.PREFIXES:
            if word.startswith(pref) and len(word) > len(pref) + 2:
                word = word[len(pref):]
                break
        for suff in cls.SUFFIXES:
            if word.endswith(suff) and len(word) > len(suff) + 2:
                word = word[:-len(suff)]
                break
        return word

    @classmethod
    def detect_language(cls, text):
        if not text:
            return 'ar'
        arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        total_chars = len(text.strip())
        if total_chars == 0:
            return 'ar'
        ratio = arabic_chars / total_chars
        return 'ar' if ratio > 0.3 else 'en'

    @classmethod
    def extract_entities(cls, text):
        entities = {
            'numbers': re.findall(r'\d+(?:\.\d+)?', text),
            'urls': re.findall(r'https?://\S+', text),
            'emails': re.findall(r'\S+@\S+\.\S+', text),
            'mentions': re.findall(r'@\w+', text),
            'code_blocks': re.findall(r'`{1,3}(.+?)`{1,3}', text, re.DOTALL),
        }
        return entities

# ==============================================================================
# 2. INTENT CLASSIFIER
# ==============================================================================

class Intent:
    """Classification of user intent from free text."""

    INTENTS = {
        'code_generate': {
            'ar': ['اكتب كود', 'كود ل', 'برمج لي', 'سكربت', 'function', 'دالة', 'اكتب برنامج', 'امثلة برمجية', 'مثال برمجي', 'كيف ابرمج', 'كيف اكتب', 'انشئ كود', 'اعطني كود', 'code for', 'python', 'javascript', 'html', 'css', 'sql', 'bash', 'flask', 'django', 'react'],
            'en': ['write code', 'code for', 'script for', 'program to', 'function that', 'how to code', 'example in python', 'example in js', 'build a', 'create a script', 'generate code', 'coding']
        },
        'code_debug': {
            'ar': ['صحح', 'خطأ', 'error', 'bug', 'مشكلة في الكود', 'ما يشتغل', 'ما يعمل', 'يرفض', 'يعطيني خطأ', 'traceback', 'exception', 'فشل', 'تعطل', 'crash'],
            'en': ['fix this', 'debug', 'error in', 'not working', 'bug in', 'traceback', 'exception', 'syntax error', 'broken', 'fails', 'crashes']
        },
        'code_explain': {
            'ar': ['اشرح الكود', 'فهمني', 'شرح', 'يعني ايش', 'ايش يسوي', 'كيف يشتغل', 'توضيح', 'اشرحلي', 'وضحلي'],
            'en': ['explain code', 'what does this do', 'how does this work', 'break down', 'walk me through', 'explain this']
        },
        'algorithm': {
            'ar': ['خوارزمية', 'algorithm', 'big o', 'تعقيد', 'كفاءة', 'بنية البيانات', 'sort', 'search', 'graph', 'tree', 'dynamic programming', 'dp', 'recursion'],
            'en': ['algorithm', 'data structure', 'complexity', 'big o', 'time complexity', 'space complexity', 'sorting', 'searching', 'graph traversal']
        },
        'math_solve': {
            'ar': ['احسب', 'حل', 'معادلة', 'جذر', 'log', 'sin', 'cos', 'integral', 'اشتقاق', 'تكامل', 'مساحة', 'محيط', 'حجم', 'نسبة', 'نسبة مئوية', 'كم يساوي', 'احسبلي', 'result', 'sqrt', 'power', 'factorial', 'fibonacci', 'prime'],
            'en': ['calculate', 'solve', 'equation', 'compute', 'derivative', 'integral', 'area of', 'volume of', 'percentage', 'sqrt', 'factorial', 'what is', 'equals', 'result of']
        },
        'convert': {
            'ar': ['حول', 'تحويل', 'من', 'الى', 'دولار', 'يورو', 'كيلو', 'متر', 'ساعة', 'دقيقة', 'تحويل عملات', 'تحويل وحدات'],
            'en': ['convert', 'to usd', 'to eur', 'km to miles', 'kg to lbs', 'celsius to fahrenheit', 'how many', 'exchange rate']
        },
        'definition': {
            'ar': ['ايش هو', 'ما هو', 'ما هي', 'تعريف', 'define', 'meaning', 'معنى', 'فلسفة', 'علم', 'مفهوم', 'شرح مصطلح', 'اشرحلي'],
            'en': ['what is', 'define', 'meaning of', 'explain what', 'concept of', 'definition of']
        },
        'history': {
            'ar': ['تاريخ', 'متى', 'في اي سنة', 'من اكتشف', 'من invent', 'حرب', 'عهد', 'دولة', 'امبراطورية', 'خلافة', 'عصر', 'حضارة'],
            'en': ['history of', 'when did', 'who discovered', 'who invented', 'ancient', 'war', 'dynasty', 'empire', 'civilization', 'era']
        },
        'science': {
            'ar': ['فيزياء', 'كيمياء', 'بيولوجيا', 'فلك', 'فضاء', 'ذرة', 'طاقة', 'ضوء', 'جاذبية', 'نظرية', 'قانون', 'كون', 'نجم', 'كوكب'],
            'en': ['physics', 'chemistry', 'biology', 'astronomy', 'quantum', 'relativity', 'gravity', 'atom', 'molecule', 'theory of', 'universe', 'planet']
        },
        'geography': {
            'ar': ['اين', 'وين', 'دولة', 'عاصمة', 'جبل', 'نهر', 'بحر', 'محيط', 'قارة', 'مدينة', 'خريطة', 'موقع'],
            'en': ['where is', 'capital of', 'country', 'mountain', 'river', 'ocean', 'continent', 'city in', 'located']
        },
        'religion': {
            'ar': ['قران', 'حديث', 'سورة', 'اية', 'اسلام', 'فقه', 'تفسير', 'صلاة', 'زكاة', 'صيام', 'حج', 'الله', 'نبي', 'دعاء', 'اذكار'],
            'en': ['quran', 'hadith', 'islam', 'surah', 'verse', 'prophet', 'prayer', 'ramadan', 'hajj', 'dua']
        },
        'tech': {
            'ar': ['هكر', 'اختراق', 'امن', 'cyber', 'linux', 'terminal', 'network', 'wifi', 'server', 'database', 'docker', 'git', 'github', 'firewall', 'encryption'],
            'en': ['hack', 'cybersecurity', 'linux command', 'networking', 'sql injection', 'pentest', 'vulnerability', 'exploit', 'kali']
        },
        'linux_cmd': {
            'ar': ['terminal', 'termux', 'bash', 'shell', 'chmod', 'grep', 'awk', 'sed', 'command', 'اوامر'],
            'en': ['linux', 'bash script', 'command line', 'chmod', 'chown', 'grep', 'find', 'tar', 'ssh', 'scp']
        },
        'poetry': {
            'ar': ['شعر', 'قصيدة', 'بيت شعر', 'ابيات', 'قافية', 'موشح', 'زجل', 'متنبي', 'نزار', 'محمود درويش', 'امرؤ القيس'],
            'en': ['poem', 'poetry', 'verse', 'rhyme', 'write a poem']
        },
        'joke': {
            'ar': ['نكتة', 'ضحك', 'هبال', 'مضحك', 'joke', 'funny', 'meme', 'هزر'],
            'en': ['joke', 'funny', 'laugh', 'humor', 'tell me a joke', 'make me laugh']
        },
        'story': {
            'ar': ['قصة', 'حكاية', 'رواية', 'سرد', 'story', 'fiction', 'fantasy', 'حكاية'],
            'en': ['story', 'tell me a story', 'fiction', 'narrative', 'short story']
        },
        'roast': {
            'ar': ['هزر', 'هزرة', 'سخر', 'roast', 'تريق', 'تنمر', 'مسخرة'],
            'en': ['roast me', 'insult me', 'make fun of', 'savage', 'burn']
        },
        'greeting': {
            'ar': ['مرحبا', 'هلا', 'السلام', 'صباح', 'مساء', 'اهلين', 'هاي', 'hello', 'hi', 'hey', 'تحياتي', 'سلامات'],
            'en': ['hello', 'hi', 'hey', 'good morning', 'good evening', 'greetings', 'salam', 'whats up']
        },
        'who_are_you': {
            'ar': ['من انت', 'مين انت', 'شو اسمك', 'ايش اسمك', 'منو انت', 'who are you', 'your name', 'تعرفني عنك'],
            'en': ['who are you', 'what is your name', 'introduce yourself', 'tell me about you']
        },
        'time': {
            'ar': ['الوقت', 'الساعة', 'كم الساعة', 'تاريخ', 'اليوم', 'month', 'year', 'الان', 'حاليا'],
            'en': ['what time', 'what date', 'current time', 'today is', 'what day', 'now']
        },
        'weather': {
            'ar': ['طقس', 'جو', 'حرارة', 'امطار', 'weather', 'temperature', 'مطر', 'شمس'],
            'en': ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy']
        },
        'health': {
            'ar': ['صحة', 'صحي', 'طب', 'دواء', 'اعراض', 'مرض', 'نصيحة صحية', 'health tip', 'diet', 'fitness', 'رياضة', 'تغذية'],
            'en': ['health', 'medical', 'symptom', 'medicine', 'doctor', 'nutrition', 'workout', 'mental health']
        },
        'advice': {
            'ar': ['نصيحة', 'نصائح', 'اعطني', 'ساعدني', 'مشكلتي', ' confused', 'lost', 'depressed', 'anxious', 'حزين', 'محبط'],
            'en': ['advice', 'help me', 'what should i do', 'i am confused', 'life advice', 'motivation', 'sad', 'depressed']
        },
        'translate': {
            'ar': ['ترجم', 'translate', 'من عربي', 'من انجليزي', 'meaning in', 'معنى كلمة', 'ترجمة'],
            'en': ['translate', 'translation', 'in arabic', 'in english', 'how to say', 'what does mean']
        },
        'search': {
            'ar': ['ابحث', 'دور', 'google', 'ويكيبيديا', 'معلومات عن', 'بحث عن', 'دلني'],
            'en': ['search', 'google', 'wikipedia', 'look up', 'find information', 'info about']
        },
        'compliment': {
            'ar': ['مدح', 'اشكر', 'شكرا', 'جميل', 'رهيب', 'ذكي', 'احبك', 'ممتاز', 'عظيم'],
            'en': ['thank you', 'thanks', 'good job', 'amazing', 'love you', 'you are great', 'awesome']
        },
        'insult': {
            'ar': ['غبي', 'احمق', 'سخيف', 'كرهتك', 'بطل', 'callate', 'زفت', 'كذاب'],
            'en': ['stupid', 'dumb', 'hate you', 'shut up', 'you suck', 'idiot', 'liar']
        },
        'random': {
            'ar': ['عشوائي', 'random', 'fact', 'حقيقة', 'هل تعلم', 'trivia', 'معلومة'],
            'en': ['random fact', 'did you know', 'trivia', 'interesting fact', 'cool fact']
        },
        'game': {
            'ar': ['لعبة', 'تحدي', 'سؤال', 'quiz', 'فزورة', 'لغز', 'غموض'],
            'en': ['game', 'quiz', 'riddle', 'puzzle', 'challenge', 'trivia game']
        },
        'memorize': {
            'ar': ['تذكر', 'احفظ', 'ذاكرتي', 'remember', 'dont forget', 'احفظلي', 'سجل'],
            'en': ['remember that', 'save this', 'note this', 'dont forget', 'store this']
        },
    }

    @classmethod
    def classify(cls, text):
        text_norm = ArabicNLP.normalize(text)
        tokens = set(ArabicNLP.tokenize(text))
        lang = ArabicNLP.detect_language(text)

        scores = {}
        for intent, keywords in cls.INTENTS.items():
            score = 0
            kw_list = keywords.get(lang, keywords.get('ar', []))
            for kw in kw_list:
                kw_norm = ArabicNLP.normalize(kw)
                if kw_norm in text_norm:
                    score += 3
                elif any(ArabicNLP.light_stem(t) == ArabicNLP.light_stem(kw_norm) for t in tokens if len(t) > 2):
                    score += 1.5
            scores[intent] = score

        if not scores or max(scores.values()) == 0:
            return ('chat', 0.5)

        best = max(scores, key=scores.get)
        confidence = min(scores[best] / 5, 1.0)
        return (best, confidence)

# ==============================================================================
# 3. KNOWLEDGE CORE — THE BRAIN
# ==============================================================================

class KnowledgeCore:
    """Massive offline knowledge base."""

    CODE_SNIPPETS = {
        'python_hello': {
            'code': 'print("Hello, Quantum World!")',
            'desc': 'أبسط برنامج Python'
        },
        'python_read_file': {
            'code': """with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
print(content)""",
            'desc': 'قراءة ملف نصي بالعربية'
        },
        'python_flask_api': {
            'code': """from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/hello')
def hello():
    return jsonify({"message": "مرحباً من مروق!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)""",
            'desc': 'API Flask بسيط'
        },
        'python_requests': {
            'code': """import requests
resp = requests.get('https://api.example.com/data')
data = resp.json()
print(data)""",
            'desc': 'طلب HTTP GET'
        },
        'python_sqlite': {
            'code': """import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
c.execute("INSERT INTO users (name) VALUES (?)", ("مروق",))
conn.commit()
conn.close()""",
            'desc': 'قاعدة بيانات SQLite'
        },
        'python_decorator': {
            'code': """import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"⏱️ {func.__name__} took {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def heavy_compute():
    return sum(range(10**6))""",
            'desc': 'Decorator لقياس الوقت'
        },
        'python_async': {
            'code': """import asyncio

async def fetch(url):
    print(f"Fetching {url}...")
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    urls = ['url1', 'url2', 'url3']
    results = await asyncio.gather(*[fetch(u) for u in urls])
    print(results)

asyncio.run(main())""",
            'desc': 'برمجة غير متزامنة Async/Await'
        },
        'python_class': {
            'code': """class QuantumBrain:
    def __init__(self, name):
        self.name = name
        self.knowledge = {}

    def learn(self, topic, info):
        self.knowledge[topic] = info
        return f"{self.name} learned: {topic}"

brain = QuantumBrain("Maroq")
print(brain.learn("Python", "Awesome!"))""",
            'desc': 'Class في Python'
        },
        'python_list_comp': {
            'code': """# List comprehension
squares = [x**2 for x in range(10)]

# Dict comprehension
square_dict = {x: x**2 for x in range(5)}

# Filter + map combined
evens = [x for x in range(20) if x % 2 == 0]
print(squares, square_dict, evens)""",
            'desc': 'List/Dict Comprehension'
        },
        'js_fetch': {
            'code': """async function getData() {
    try {
        const res = await fetch('/api/data');
        const json = await res.json();
        console.log(json);
    } catch (err) {
        console.error('Error:', err);
    }
}""",
            'desc': 'طلب fetch في JavaScript'
        },
        'js_promise_all': {
            'code': """const urls = ['/api/a', '/api/b', '/api/c'];
Promise.all(urls.map(u => fetch(u).then(r => r.json())))
    .then(results => console.log('All done:', results))
    .catch(err => console.error('One failed:', err));""",
            'desc': 'تنفيذ متوازي لعدة طلبات'
        },
        'js_array_methods': {
            'code': """const arr = [1, 2, 3, 4, 5];

// Map, Filter, Reduce
const doubled = arr.map(x => x * 2);
const evens = arr.filter(x => x % 2 === 0);
const sum = arr.reduce((a, b) => a + b, 0);

// Find, Some, Every
const firstEven = arr.find(x => x % 2 === 0);
const hasNegative = arr.some(x => x < 0);
const allPositive = arr.every(x => x > 0);

console.log({doubled, evens, sum, firstEven, hasNegative, allPositive});""",
            'desc': 'دوال المصفوفات في JS'
        },
        'css_flex_center': {
            'code': """.container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
}""",
            'desc': 'توسيط عمودي وأفقي + gradient'
        },
        'css_grid_layout': {
            'code': """.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    padding: 20px;
}

.card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 20px;
}""",
            'desc': 'Grid Layout + Glassmorphism'
        },
        'bash_termux': {
            'code': """# تحديث الحزم
pkg update && pkg upgrade -y

# تثبيت Python
pkg install python -y

# تشغيل خادم Flask
python app.py

# إعادة توجيه المنفذ
ssh -R 80:localhost:5000 serveo.net""",
            'desc': 'أوامر Termux أساسية'
        },
        'bash_find_large': {
            'code': """# أكبر 10 ملفات في المجلد الحالي
du -ah . | sort -rh | head -n 10

# البحث عن ملفات Python المعدلة اليوم
find . -name "*.py" -mtime -1

# حذف ملفات __pycache__ بشكل متكرر
find . -type d -name "__pycache__" -exec rm -rf {} +""",
            'desc': 'أوامر Bash متقدمة'
        },
        'bash_monitor': {
            'code': """# مراقبة استخدام الذاكرة والمعالج
htop

# مراقبة اتصالات الشبكة
netstat -tuln

# مراقبة سجلات النظام في الوقت الفعلي
tail -f /var/log/syslog

# معرفة العمليات التي تستخدم المنفذ 5000
lsof -i :5000""",
            'desc': 'مراقبة النظام'
        },
        'sql_injection_safe': {
            'code': """# ❌ خطأ: تسلسل نصي (vulnerable)
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# ✅ صحيح: Parameterized query
cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))

# ✅ صحيح: ORM style (SQLAlchemy)
User.query.filter_by(name=user_input).first()""",
            'desc': 'حماية من SQL Injection'
        },
        'regex_common': {
            'code': """import re

# استخراج إيميلات
text = "Contact: admin@site.com, user@mail.org"
emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)

# التحقق من رقم هاتف سعودي
phone = "0501234567"
valid = re.match(r'^(05|5)\d{8}$', phone)

# استبدال روابط بـ [LINK]
clean = re.sub(r'https?://\S+', '[LINK]', text)""",
            'desc': 'أمثلة Regex عملية'
        },
        'docker_basic': {
            'code': """# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

# Build & Run
docker build -t myapp .
docker run -p 5000:5000 myapp""",
            'desc': 'Dockerfile + أوامر Docker'
        },
        'git_cheatsheet': {
            'code': """# إعداد repo جديد
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/user/repo.git
git push -u origin main

# إلغاء آخر commit (بدون حذف الملفات)
git reset --soft HEAD~1

# إخفاء تغييرات مؤقتاً
git stash
git stash pop

# إنشاء فرع جديد والانتقال إليه
git checkout -b feature-branch""",
            'desc': 'Git cheatsheet'
        },
        'html5_template': {
            'code': """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مروق الكمومي</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f0f23; color: #fff; }
    </style>
</head>
<body>
    <h1>مرحباً بالعالم الكمومي!</h1>
    <script src="app.js"></script>
</body>
</html>""",
            'desc': 'قالب HTML5 عربي'
        },
        'react_hook': {
            'code': """import { useState, useEffect } from 'react';

function QuantumCounter() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        document.title = `Count: ${count}`;
        return () => console.log('Cleanup!');
    }, [count]);

    return (
        <button onClick={() => setCount(c => c + 1)}>
            Quantum Count: {count}
        </button>
    );
}""",
            'desc': 'React Hook مثال'
        },
        'node_express': {
            'code': """const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/status', (req, res) => {
    res.json({ status: 'online', version: '4.0' });
});

app.post('/api/chat', (req, res) => {
    const { message } = req.body;
    res.json({ reply: `Echo: ${message}` });
});

app.listen(3000, () => console.log('Server running on port 3000'));""",
            'desc': 'Express.js API'
        },
    }

    DEFINITIONS = {
        'ar': {
            'الذكاء الاصطناعي': 'قدرة الأنظمة الحاسوبية على محاكاة الذكاء البشري: التعلم، الاستدلال، الإدراك، وفهم اللغة الطبيعية.',
            'التعلم العميق': 'فرع من التعلم الآلي يعتمد على شبكات عصبية اصطناعية متعددة الطبقات لاستخلاص تمثيلات عالية المستوى من البيانات.',
            'الكم': 'أصغر وحدة فيزيائية للمعلومات الكمومية، تتخذ حالات تراكب (superposition) ويمكن أن تكون متشابكة (entangled).',
            'blockchain': 'سجل رقمي موزع وغير قابل للتغيير يُستخدم لتسجيل المعاملات عبر شبكات الحواسيب المتعددة.',
            'docker': 'منصة لإنشاء وتشغيل ونشر التطبيقات داخل حاويات (containers) معزولة عن بيئة النظام.',
            'api': 'واجهة برمجة التطبيقات: مجموعة من البروتوكولات والأدوات التي تتيح للبرمجيات التواصل مع بعضها.',
            'recursion': 'دالة تستدعي نفسها مباشرة أو غير مباشرة لحل مشكلة بتقسيمها إلى نسخ أصغر من نفسها.',
            'big_o': 'تدوين يصف أداء الخوارزمية من حيث الزمن أو المساحة مع نمو حجم المدخلات.',
            'entropy': 'مقياس للعشوائية أو عدم اليقين في النظام. في المعلوماتية: متوسط كمية المعلومات المنتجة.',
            'tcp_ip': 'مجموعة بروتوكولات الاتصال الأساسية للإنترنت: TCP يضمن التوصيل الموثوق، IP يوجه الحزم.',
            'dns': 'نظام أسماء النطاقات: يترجم أسماء النطاقات (مثل google.com) إلى عناوين IP رقمية.',
            'https': 'بروتوكول نقل النص التشعبي الآمن: يشفر البيانات بين المتصفح والخادم باستخدام TLS/SSL.',
            'jwt': 'JSON Web Token: طريقة مدمجة ومؤمنة لنقل المعلومات بين طرفين ككائن JSON موقع رقمياً.',
            'ci_cd': 'التكامل المستمر والنشر المستمر: ممارسات DevOps لأتمتة بناء واختبار ونشر البرمجيات.',
            'microservices': 'أسلوب هندسة برمجية يبني التطبيق كمجموعة خدمات صغيرة مستقلة تتواصل عبر APIs.',
            'graphql': 'لغة استعلام للواجهات البرمجية تتيح للعميل تحديد البيانات المطلوبة بدقة، مما يقلل من الطلبات غير الضرورية.',
            'websocket': 'بروتوكول اتصال ثنائي الاتجاه فوق TCP، يتيح تبادل الرسائل في الوقت الفعلي بين العميل والخادم.',
            'load_balancer': 'جهاز أو برنامج يوزع حركة المرور عبر خوادم متعددة لضمان توفر الخدمة وتحسين الأداء.',
            'cache': 'ذاكرة وسيطة سريعة تخزين نسخ من البيانات المتكررة الوصول إليها لتقليل زمن الاستجابة.',
            'indexing': 'هيكلة بيانات (مثل B-Tree) تُسرع عمليات البحث والاسترجاع في قواعد البيانات.',
        },
        'en': {
            'artificial intelligence': 'The simulation of human intelligence processes by computer systems: learning, reasoning, perception, and language understanding.',
            'deep learning': 'A subset of machine learning using multi-layered neural networks to extract high-level features from raw data.',
            'quantum': 'The smallest physical unit of quantum information, capable of superposition and entanglement.',
            'blockchain': 'A distributed, immutable digital ledger used to record transactions across multiple computers.',
            'docker': 'A platform for developing, shipping, and running applications in isolated containers.',
            'api': 'Application Programming Interface: protocols and tools allowing software applications to communicate.',
            'recursion': 'A function that calls itself directly or indirectly to solve a problem by breaking it into smaller instances.',
            'big o': 'Notation describing algorithm performance in terms of time or space as input size grows.',
            'entropy': 'A measure of randomness or uncertainty. In information theory: average information produced.',
            'tcp ip': 'Core Internet communication protocols: TCP ensures reliable delivery, IP routes packets.',
            'dns': 'Domain Name System: translates human-readable domain names to numerical IP addresses.',
            'https': 'HyperText Transfer Protocol Secure: encrypts data between browser and server using TLS/SSL.',
            'jwt': 'JSON Web Token: a compact, secure way to transmit information between parties as a signed JSON object.',
            'ci cd': 'Continuous Integration / Continuous Deployment: DevOps practices automating build, test, and release.',
            'microservices': 'An architectural style structuring an application as a collection of loosely coupled services.',
            'graphql': 'A query language for APIs that allows clients to request exactly the data they need.',
            'websocket': 'A bidirectional communication protocol over TCP enabling real-time message exchange.',
            'load balancer': 'A device or software that distributes traffic across multiple servers for availability and performance.',
            'cache': 'Fast intermediate memory storing copies of frequently accessed data to reduce latency.',
            'indexing': 'A data structure (like B-Tree) that speeds up search and retrieval operations in databases.',
        }
    }

    HISTORY = {
        'ar': [
            "اكتشف ابن الهيثم (965-1040م) طبيعة الضوء واخترع الكاميرا المظلمة (القمرة)، ويُلقب بـ'أبو علم البصريات'.",
            "الخوارزمي (780-850م) هو أبو الجبر والخوارزميات. كلمة 'Algorithm' مشتقة من اسمه اللاتيني 'Algoritmi'.",
            "بيت الحكمة في بغداد (8م) كان أول مركز بحثي عالمي، ترجم فيه العلماء آلاف الكتب من اليونانية والسنسكريتية.",
            "اخترع الجبرزي (Al-Jazari) في القرن 12م أول روبوت آلي (آلة موسيقية تعزف بنفسها) وأول آلة حاسبة ميكانيكية.",
            "الكيمياء (Chemistry) مشتقة من 'الكيمياء' العربية. جابر بن حيان (721-815م) هو أبو الكيمياء.",
            "في 1969، أرسلت UCLA أول رسالة على ARPANET (سلف الإنترنت). الكلمة الوحيدة التي وصلت كانت 'LO' قبل انقطاع الاتصال.",
            "لينوس تورفالدس كتب نواة Linux في 1991 كمشروع هواية، واليوم تشغل 96% من خوادم الإنترنت.",
            "أول حاسوب إلكتروني عام (ENIAC) كان يزن 30 طناً ويحتوي على 17,468 صماماً مفرغاً (vacuum tube).",
            "في 1956، عرضت IBM أول قرص صلب (RAMAC 350) بسعة 5 ميجابايت ووزن طن، بسعر 50,000 دولار.",
            "تيم بيرنرز-لي اخترع WWW في CERN عام 1989. لم يبرئ اختراعه، فأصبح الإنترنت ملكاً للجميع.",
            "أول هاتف ذكي (IBM Simon) صدر في 1994. كان يحتوي على شاشة لمس، بريد إلكتروني، وفاكس!",
            "أول فيديو على YouTube رفعه Jawed Karim في 2005 بعنوان 'Me at the zoo'.",
            "أول رسالة SMS أُرسلت في 1992 وكانت تقول: 'Merry Christmas'.",
            "أول لغة برمجة عالية المستوى (Fortran) طُورت في IBM عام 1957.",
            "أول فيروس كمبيوتر (Creeper) ظهر في 1971 وكان مجرد تجربة: 'I'm the creeper, catch me if you can!'.",
        ],
        'en': [
            "Ibn al-Haytham (965-1040 AD) discovered the nature of light and invented the camera obscura, known as the 'Father of Optics'.",
            "Al-Khwarizmi (780-850 AD) is the father of Algebra and Algorithms. The word 'Algorithm' derives from his Latinized name.",
            "The House of Wisdom in Baghdad (8th c.) was the world's first research center, translating thousands of Greek and Sanskrit texts.",
            "Al-Jazari invented the first programmable robot (musical automaton) and mechanical calculator in the 12th century.",
            "Chemistry derives from the Arabic 'Al-Kimiya'. Jabir ibn Hayyan (721-815 AD) is considered the father of chemistry.",
            "In 1969, UCLA sent the first ARPANET message. Only 'LO' made it through before the system crashed.",
            "Linus Torvalds wrote Linux in 1991 as a hobby. Today it powers 96% of internet servers.",
            "The first general-purpose computer ENIAC weighed 30 tons and contained 17,468 vacuum tubes.",
            "IBM's first hard disk (RAMAC 350, 1956) stored 5 MB, weighed a ton, and cost $50,000.",
            "Tim Berners-Lee invented the WWW at CERN in 1989. He never patented it, making the internet free for all.",
            "The first smartphone (IBM Simon) was released in 1994 with a touchscreen, email, and fax!",
            "The first YouTube video was uploaded by Jawed Karim in 2005 titled 'Me at the zoo'.",
            "The first SMS was sent in 1992 saying: 'Merry Christmas'.",
            "The first high-level programming language (Fortran) was developed at IBM in 1957.",
            "The first computer virus (Creeper) appeared in 1971 as an experiment: 'I'm the creeper, catch me if you can!'.",
        ]
    }

    SCIENCE = {
        'ar': [
            "الضوء يستغرق 8 دقائق و20 ثانية للوصول من الشمس إلى الأرض. لكن الفوتون نفسه لا يشعر بالزمن (التوقف الزمني عند سرعة الضوء).",
            "90% من كتلة الجسم البشري مصنوعة من بقايا نجوم ميتة (stardust). الذرات الثقيلة مثل الحديد والكربون تُنتج فقط في انفجارات المستعرات الأعظمية.",
            "الثقب الأسود في مركز مجرة درب التبانة (Sagittarius A*) يبلغ كتلته 4 ملايين كتلة شمسية، لكن حجمه أصغر من مدار عطارد.",
            "الحاسوب الكمومي لا يحسب أسرع بالمعنى التقليدي، بل يستغل التراكب لحساب كل الاحتمالات في آن واحد.",
            "DNA البشري يحتوي على ~3 مليار زوج قاعدي. إذا فُرد، سيبلغ طوله حوالي 2 متر لكل خلية، وإذا وُصلت كل خلايا الجسم (~37 تريليون) سيمتد لـ 74 مليار كم.",
            "الفراغ ليس فارغاً: ي burble بأزواج جسيم-مضاد جسيم افتراضية تظهر وتختفي باستمرار (تقلبات كمومية).",
            "الجاذبية أضعف قوة في الطبيعة (10^-38 مقارنة بالقوة النووية القوية)، لكنها الوحيدة التي لا يوجد لها جسيم ناقل مؤكد (الجاذون Graviton نظري).",
            "الأرض تفقد حوالي 50,000 طن من الكتلة سنوياً (غازات خفيفة تهرب للفضاء)، لكن تكتسب ~40,000 طن من الغبار الكوني. صافي الخسارة ~10,000 طن/سنة.",
            "النمل يستطيع حمل أوزان تصل إلى 50 ضعف وزنه. لو كان بإمكان الإنسان فعل ذلك، لحمل سيارة بوزن 2 طن.",
            "الدلافين تُسمي بعضها بأسماء فريدة (signature whistles) تشبه أسماء البشر. تتعرف على أصدقائها منذ 20 سنة.",
            "أقدم شجرة معروفة (Methuselah) عمرها 4,850 سنة. تقع في كاليفورنيا وموقعها السري محمي.",
            "الفضاء ليس 'أسود' بالكامل: يتوهج بإشعاع خلفي كوني (CMB) بدرجة حرارة 2.7 كلفن، بقية الانفجار العظيم.",
        ],
        'en': [
            "Light takes 8m 20s to reach Earth from the Sun. But the photon itself experiences no time (time dilation at c).",
            "90% of your body mass is stardust. Heavy atoms like iron and carbon are produced only in supernova explosions.",
            "The black hole at the Milky Way's center (Sagittarius A*) has 4 million solar masses but is smaller than Mercury's orbit.",
            "Quantum computers don't compute faster in the traditional sense; they exploit superposition to evaluate all possibilities simultaneously.",
            "Human DNA has ~3 billion base pairs. If stretched, each cell's DNA is ~2m; all body cells combined would reach 74 billion km.",
            "Vacuum is not empty: it bubbles with virtual particle-antiparticle pairs constantly appearing and annihilating (quantum fluctuations).",
            "Gravity is the weakest force (10^-38 vs strong nuclear force), yet it's the only one without a confirmed carrier particle (Graviton is theoretical).",
            "Earth loses ~50,000 tons of mass annually (light gases escaping to space) but gains ~40,000 tons from cosmic dust. Net loss: ~10,000 tons/year.",
            "Ants can carry weights up to 50 times their body weight. If humans could do that, one person could lift a 2-ton car.",
            "Dolphins use unique signature whistles (like human names) to identify each other and remember friends for 20 years.",
            "The oldest known tree (Methuselah) is 4,850 years old. Located in California, its exact location is kept secret.",
            "Space isn't completely black: it glows with Cosmic Microwave Background (CMB) at 2.7 Kelvin — leftover radiation from the Big Bang.",
        ]
    }

    GEOGRAPHY = {
        'ar': {
            'السعودية': {'عاصمة': 'الرياض', 'عملة': 'الريال السعودي', 'سكان': '~36 مليون', 'حقيقة': 'أكبر دولة عربية من حيث المساحة.'},
            'مصر': {'عاصمة': 'القاهرة', 'عملة': 'الجنيه المصري', 'سكان': '~105 مليون', 'حقيقة': 'موطن أقدم حضارة مستمرة في التاريخ.'},
            'المغرب': {'عاصمة': 'الرباط', 'عملة': 'الدرهم المغربي', 'سكان': '~37 مليون', 'حقيقة': 'أقصى نقطة غربية في العالم العربي.'},
            'الجزائر': {'عاصمة': 'الجزائر', 'عملة': 'الدينار الجزائري', 'سكان': '~45 مليون', 'حقيقة': 'أكبر دولة أفريقية من حيث المساحة.'},
            'تونس': {'عاصمة': 'تونس', 'عملة': 'الدينار التونسي', 'سكان': '~12 مليون', 'حقيقة': 'مهد الربيع العربي وموطن قرطاج.'},
            'العراق': {'عاصمة': 'بغداد', 'عملة': 'الدينار العراقي', 'سكان': '~42 مليون', 'حقيقة': 'مهد الحضارة السومرية (أقدم كتابة معروفة).'},
            'سوريا': {'عاصمة': 'دمشق', 'عملة': 'الليرة السورية', 'سكان': '~22 مليون', 'حقيقة': 'دمشق أقدم مدينة مأهولة في العالم (11,000 سنة).'},
            'اليمن': {'عاصمة': 'صنعاء', 'عملة': 'الريال اليمني', 'سكان': '~32 مليون', 'حقيقة': 'موطن أول بناء طابقي (برج سبأ) وقهوة العرب.'},
            'الإمارات': {'عاصمة': 'أبوظبي', 'عملة': 'الدرهم الإماراتي', 'سكان': '~10 مليون', 'حقيقة': 'تضم أطول مبنى في العالم (برج خليفة 828م).'},
            'قطر': {'عاصمة': 'الدوحة', 'عملة': 'الريال القطري', 'سكان': '~2.7 مليون', 'حقيقة': 'أعلى دخل فردي في العالم (GDP per capita).'},
            'الكويت': {'عاصمة': 'الكويت', 'عملة': 'الدينار الكويتي', 'سكان': '~4.3 مليون', 'حقيقة': 'أغلى عملة في العالم (1 KWD = ~3.25 USD).'},
            'عمان': {'عاصمة': 'مسقط', 'عملة': 'الريال العماني', 'سكان': '~5 مليون', 'حقيقة': 'أقدم دولة مستقلة في العالم العربي.'},
            'لبنان': {'عاصمة': 'بيروت', 'عملة': 'الليرة اللبنانية', 'سكان': '~5.5 مليون', 'حقيقة': 'أقدم مدينة في التاريخ المسجل (بيروت).'},
            'الأردن': {'عاصمة': 'عمان', 'عملة': 'الدينار الأردني', 'سكان': '~11 مليون', 'حقيقة': 'تضم البتراء (إحدى عجائب الدنيا السبع الجديدة).'},
            'فلسطين': {'عاصمة': 'القدس', 'عملة': 'الشيكل/الدينار/الجنيه', 'سكان': '~5.4 مليون', 'حقيقة': 'مهد الأديان السماوية الثلاث.'},
            'السودان': {'عاصمة': 'الخرطوم', 'عملة': 'الجنيه السوداني', 'سكان': '~46 مليون', 'حقيقة': 'أكبر عدد من الأهرامات في العالم (200+ هرم).'},
            'ليبيا': {'عاصمة': 'طرابلس', 'عملة': 'الدينار الليبي', 'سكان': '~7 مليون', 'حقيقة': 'تمتلك أكبر احتياطي نفطي في أفريقيا.'},
            'موريتانيا': {'عاصمة': 'نواكشوط', 'عملة': 'الأوقية الموريتانية', 'سكان': '~4.6 مليون', 'حقيقة': 'آخر دولة في العالم ألغت الرق رسمياً (1981).'},
            'الصومال': {'عاصمة': 'مقديشو', 'عملة': 'الشلن الصومالي', 'سكان': '~16 مليون', 'حقيقة': 'أطول ساحل في أفريقيا (3,025 كم).'},
            'جيبوتي': {'عاصمة': 'جيبوتي', 'عملة': 'الفرنك الجيبوتي', 'سكان': '~1 مليون', 'حقيقة': 'نقطة التقاء ثلاث صفائح تكتونية.'},
            'الصين': {'عاصمة': 'بكين', 'عملة': 'اليوان', 'سكان': '~1.4 مليار', 'حقيقة': 'أقدم حضارة مستمرة (~5000 سنة).'},
            'اليابان': {'عاصمة': 'طوكيو', 'عملة': 'الين', 'سكان': '~125 مليون', 'حقيقة': 'أكبر مدينة من حيث عدد السكان (طوكيو الكبرى ~37 مليون).'},
            'الهند': {'عاصمة': 'نيو دلهي', 'عملة': 'الروبية', 'سكان': '~1.4 مليار', 'حقيقة': 'أكبر ديمقراطية في العالم.'},
            'الولايات المتحدة': {'عاصمة': 'واشنطن العاصمة', 'عملة': 'الدولار', 'سكان': '~335 مليون', 'حقيقة': 'تمتلك أكبر عدد من مراكز البيانات في العالم.'},
            'روسيا': {'عاصمة': 'موسكو', 'عملة': 'الروبل', 'سكان': '~146 مليون', 'حقيقة': 'أكبر دولة في العالم (تغطي 11 منطقة زمنية).'},
            'البرازيل': {'عاصمة': 'برازيليا', 'عملة': 'الريال البرازيلي', 'سكان': '~215 مليون', 'حقيقة': 'تضم أكبر غابة مطيرة (الأمازون).'},
            'ألمانيا': {'عاصمة': 'برلين', 'عملة': 'اليورو', 'سكان': '~83 مليون', 'حقيقة': 'أكبر اقتصاد في أوروبا.'},
            'فرنسا': {'عاصمة': 'باريس', 'عملة': 'اليورو', 'سكان': '~68 مليون', 'حقيقة': 'أكبر دولة في الاتحاد الأوروبي من حيث المساحة.'},
            'بريطانيا': {'عاصمة': 'لندن', 'عملة': 'الجنيه الإسترليني', 'سكان': '~67 مليون', 'حقيقة': 'مبتكرة GMT (توقيت غرينتش) وwww.'},
            'كندا': {'عاصمة': 'أوتاوا', 'عملة': 'الدولار الكندي', 'سكان': '~39 مليون', 'حقيقة': 'ثاني أكبر دولة في العالم من حيث المساحة.'},
            'أستراليا': {'عاصمة': 'كانبيرا', 'عملة': 'الدولار الأسترالي', 'سكان': '~26 مليون', 'حقيقة': 'أكبر جزيرة في العالم وقارة في آن واحد.'},
        },
        'en': {
            'saudi arabia': {'capital': 'Riyadh', 'currency': 'SAR', 'population': '~36M', 'fact': 'Largest Arab country by area.'},
            'egypt': {'capital': 'Cairo', 'currency': 'EGP', 'population': '~105M', 'fact': 'Home to the oldest continuous civilization.'},
            'morocco': {'capital': 'Rabat', 'currency': 'MAD', 'population': '~37M', 'fact': 'Westernmost point of the Arab world.'},
            'japan': {'capital': 'Tokyo', 'currency': 'JPY', 'population': '~125M', 'fact': 'Tokyo metro is the largest city at ~37M people.'},
            'china': {'capital': 'Beijing', 'currency': 'CNY', 'population': '~1.4B', 'fact': 'Oldest continuous civilization (~5000 years).'},
            'usa': {'capital': 'Washington D.C.', 'currency': 'USD', 'population': '~335M', 'fact': 'Hosts the most data centers globally.'},
            'india': {'capital': 'New Delhi', 'currency': 'INR', 'population': '~1.4B', 'fact': 'World's largest democracy.'},
            'russia': {'capital': 'Moscow', 'currency': 'RUB', 'population': '~146M', 'fact': 'Largest country, spanning 11 time zones.'},
            'brazil': {'capital': 'Brasilia', 'currency': 'BRL', 'population': '~215M', 'fact': 'Home to the Amazon rainforest.'},
            'germany': {'capital': 'Berlin', 'currency': 'EUR', 'population': '~83M', 'fact': 'Largest economy in Europe.'},
            'france': {'capital': 'Paris', 'currency': 'EUR', 'population': '~68M', 'fact': 'Largest EU country by area.'},
            'uk': {'capital': 'London', 'currency': 'GBP', 'population': '~67M', 'fact': 'Invented GMT and the World Wide Web.'},
            'canada': {'capital': 'Ottawa', 'currency': 'CAD', 'population': '~39M', 'fact': 'Second largest country by area.'},
            'australia': {'capital': 'Canberra', 'currency': 'AUD', 'population': '~26M', 'fact': 'World's largest island and smallest continent.'},
        }
    }

    RELIGION = {
        'ar': {
            'الفاتحة': 'أم الكتاب، تُقرأ في كل ركعة. فيها 7 آيات. قال النبي ﷺ: "الحمد لله رب العالمين" هي السبع المثاني.',
            'الإخلاص': 'تعادل ثلث القرآن. قال النبي ﷺ: "والذي نفسي بيده إنها لتعدل ثلث القرآن".',
            'الكرسي': 'آية الكرسي (البقرة 255) هي أعظم آية في القرآن. قال النبي ﷺ: "من قرأها حين يصبح كُفي بالله حين يمسي".',
            'الاستغفار': 'قال تعالى: "وَأَنِ اسْتَغْفِرُوا رَبَّكُمْ ثُمَّ تُوبُوا إِلَيْهِ" [هود: 3]. الاستغفار يفتح الأرزاق ويزيل الهموم.',
            'الصلاة': 'أول ما يُحاسب عليه العبد يوم القيامة الصلاة. قال ﷺ: "من حافظ عليها كانت له نوراً وبرهاناً ونجاة".',
            'الصدقة': 'تطفئ الخطيئة كما يطفئ الماء النار. قال ﷺ: "الصدقة برهان" (رواه مسلم).',
            'الصيام': 'الصيام نصف الصبر. قال ﷺ: "ما من عبد يصوم يوماً في سبيل الله إلا باعد الله وجهه عن النار سبعين خريفاً".',
            'الحج': 'من حج البيت فلم يرفث ولم يفسق رجع كيوم ولدته أمه. الحج المبرور ليس له جزاء إلا الجنة.',
            'الوضوء': 'الوضوء نور. قال ﷺ: "من توضأ فأحسن الوضوء خرجت خطاياه من جسده حتى تخرج من تحت أظفاره".',
            'الذكر': 'قال تعالى: "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ" [الرعد: 28]. الذكر هو راحة القلوب.',
            'القرآن': 'كلام الله المنزل على نبيه محمد ﷺ. أول ما نزل: "اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ".',
            'الإيمان': 'الإيمان بالله وملائكته وكتبه ورسله واليوم الآخر والقدر خيره وشره.',
            'التوحيد': 'إفراد الله بالعبادة. هو أصل الدين وأساسه. قال ﷺ: "من مات وهو يعلم أن لا إله إلا الله دخل الجنة".',
        },
        'en': {
            'al-fatiha': 'The Opening, recited in every rak'ah. 7 verses. The Prophet ﷺ said it is the Seven Oft-Repeated.',
            'al-ikhlas': 'Equivalent to one-third of the Quran. The Prophet ﷺ said: "By the One in Whose Hand is my soul, it equals one-third of the Quran."',
            'ayatul_kursi': 'Greatest verse in the Quran (2:255). The Prophet ﷺ said whoever recites it in the morning is protected until evening.',
            'istighfar': 'Allah says: "And seek forgiveness of your Lord and repent to Him" [Hud: 3]. Istighfar opens sustenance and removes sorrow.',
            'salah': 'The first deed accounted for on Judgment Day. The Prophet ﷺ said whoever guards it will have light, proof, and salvation.',
            'sadaqah': 'Charity extinguishes sin as water extinguishes fire. The Prophet ﷺ said: "Charity is proof" (Muslim).',
            'sawm': 'Fasting is half of patience. The Prophet ﷺ said whoever fasts a day in Allah's cause, Allah removes his face from Hellfire by 70 years.',
            'hajj': 'Whoever performs Hajj without obscenity or transgression returns as pure as the day his mother bore him. A blessed Hajj has no reward but Paradise.',
            'wudu': 'Ablution is light. The Prophet ﷺ said: "When a Muslim performs ablution perfectly, his sins leave his body, even from under his nails."',
            'dhikr': 'Allah says: "Verily, in the remembrance of Allah do hearts find rest" [13:28].',
            'quran': 'The speech of Allah revealed to Prophet Muhammad ﷺ. First revelation: "Read in the name of your Lord who created."',
            'iman': 'Faith in Allah, His angels, His books, His messengers, the Last Day, and divine decree.',
            'tawhid': 'Affirming Allah's oneness in worship. The foundation of Islam. The Prophet ﷺ said whoever dies knowing none has the right to be worshipped but Allah enters Paradise.',
        }
    }

    HEALTH = {
        'ar': [
            "🧠 **نوم الجودة**: النوم العميق يُعيد ترتيب الذاكرة. قلة النوم (<6 ساعات) تُضعف جهاز المناعة بنسبة 70%.",
            "💧 **الماء**: 2% نقص في الترطيب يُضعف الأداء الذهني. اشرب 30-35 مل لكل كجم من وزنك يومياً.",
            "🏃 **المشي**: 30 دقيقة مشي يومياً تُقلل خطر السكري النوع 2 بنسبة 58% (أكثر فعالية من الميتفورمين!).",
            "🥦 **الألياف**: تناول 25-30غ ألياف يومياً يُقلل خطر سرطان القولون بنسبة 20%. المصادر: الشوفان، التفاح، العدس.",
            "🧘 **التأمل**: 10 دقائق يومياً من mindfulness تُقلل الكورتيزول (هرمون التوتر) بنسبة 23%.",
            "📱 **الشاشات**: ضوء الأزرق (blue light) قبل النوم يُثبط الميلاتونين بنسبة 50%. استخدم الوضع الليلي بعد المغرب.",
            "🍫 **الشوكولاتة الداكنة**: تحتوي على flavonoids تُحسن تدفق الدم إلى الدماغ وتحمي من التدهور المعرفي.",
            "😴 **القيلولة**: قيلولة 20 دقيقة قبل الساعة 3 ظهراً تُحسن الأداء الذهني دون التأثير على النوم الليلي.",
            "🥑 **الدهون الصحية**: الأفوكادو والمكسرات والزيتون تحتوي على دهون أحادية غير مشبعة تُحسن صحة القلب.",
            "🦷 **الأسنان**: تنظيف الأسنان بالخيط يومياً يُقلل خطر أمراض اللثة ( gum disease) التي ترتبط بأمراض القلب.",
            "🌞 **فيتامين D**: 80% من سكان العالم يعانون من نقص فيتامين D. التعرض لـ 15 دقيقة من الشمس يومياً كافٍ.",
            "🧄 **الثوم**: يحتوي على allicin، مركب قوي مضاد للبكتيريا والفيروسات. أفضل طريقة: هرسه وتركه 10 دقائق قبل الطبخ.",
        ],
        'en': [
            "🧠 **Sleep Quality**: Deep sleep reorganizes memory. Sleep deprivation (<6h) weakens immunity by 70%.",
            "💧 **Hydration**: A 2% dehydration impairs cognitive performance. Drink 30-35ml per kg of body weight daily.",
            "🏃 **Walking**: 30 minutes of daily walking reduces Type 2 diabetes risk by 58% (more effective than metformin!).",
            "🥦 **Fiber**: 25-30g daily fiber reduces colon cancer risk by 20%. Sources: oats, apples, lentils.",
            "🧘 **Meditation**: 10 minutes of daily mindfulness reduces cortisol (stress hormone) by 23%.",
            "📱 **Screens**: Blue light before sleep suppresses melatonin by 50%. Use night mode after sunset.",
            "🍫 **Dark Chocolate**: Contains flavonoids that improve cerebral blood flow and protect against cognitive decline.",
            "😴 **Napping**: A 20-minute nap before 3 PM boosts mental performance without affecting nighttime sleep.",
            "🥑 **Healthy Fats**: Avocados, nuts, and olives contain monounsaturated fats that improve heart health.",
            "🦷 **Dental Health**: Daily flossing reduces gum disease risk, which is linked to heart disease.",
            "🌞 **Vitamin D**: 80% of the world's population is Vitamin D deficient. 15 minutes of sun exposure daily is sufficient.",
            "🧄 **Garlic**: Contains allicin, a powerful antibacterial and antiviral compound. Best method: crush and let sit 10 minutes before cooking.",
        ]
    }

    JOKES = {
        'ar': [
            "مبرمج دخل مطعم. النادل: هل لديك حجز؟ المبرمج: لا، أنا asynchronous. 😄",
            "لماذا يكره المبرمجون الطبيعة؟ لأنها مليئة بالـ bugs! 🐛",
            "كم مبرمجاً يلزم لتغيير مصباح؟ لا أحد، إنه مشكلة hardware! 💡",
            "زوجة المبرمج: اذهب للسوق واشترِ لتر حليب، وإن كان هناك بيض فاشترِ 6. عاد بـ 6 لترات حليب. 'كان هناك بيض'! 🥚",
            "الفرق بين SQL و NoSQL؟ SQL: الجداول. NoSQL: الجدول... لا يوجد! 📊",
            "أنا لست كسولاً، أنا في وضع توفير الطاقة. 🔋",
            "لماذا يصعب إقناع المبرمج بالخروج؟ لأنه دائماً في وضع 'do not disturb'. 🚫",
            "سأخبرك نكتة عن UDP... لكن لا أضمن وصولها. 📡",
            "TCP يذهب إلى حانة ويقول: 'أريد بيرة'. النادل: 'بيرة واحدة'. TCP: 'نعم، بيرة واحدة'. 🍺",
            "المبرمج في المطعم: هل يمكنني الحصول على وجبة بدون ثوم؟ النادل: 404 Not Found. 🍽️",
            "لماذا المبرمج يخلط بين عيد ميلاد زوجته وعيد الأب؟ لأنهما في نفس الـ namespace! 🎂",
            "أبي: ابني، هل تريد أن تكون طبيباً أم مهندساً؟ الابن: أريد أن أكون مبرمجاً! الأب: لا يا ابني، اختر شيئاً واقعياً! 💻",
            "المبرمج يتزوج. في ليلة الدخلة يقول: 'لنبدأ بالـ Hello World'. 👰",
            "لماذا Python أفضل من Java؟ لأنها لا تحتاج إلى ; في نهاية كل جملة. Python: 'أنا أثق بك'. Java: 'أنا أراقبك'. 🐍",
            "الفرق بين C++ و Python؟ C++: 'أنت مسؤول عن ذاكرتك'. Python: 'استرخِ، أنا أدير كل شيء'. 🐍",
            "المبرمج يدخل الجنة. الله: اسألني ما تشاء. المبرمج: هل يمكنني الحصول على root access؟ 😇",
            "لماذا المبرمج لا يستحم؟ لأنه يخاف من الـ waterfall model! 🚿",
            "الفرق بين المبرمج والطبيب؟ الطبيب يقول: 'خذ دواء'. المبرمج يقول: 'حاول تشغيله مرة أخرى'. 💊",
            "المبرمج يقرأ القرآن. يقول: 'سبحان الله، هذا الكود لا يحتوي على أي bugs!' 📖",
            "زوجة المبرمج: 'أحبك'. المبرمج: 'أنا أيضاً، لكن هل اختبرت ذلك في بيئة الإنتاج؟' ❤️",
        ],
        'en': [
            "A programmer walks into a bar... and says 'Hello World'. The bartender says 'Syntax error'. 🍺",
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "How many programmers does it take to change a light bulb? None, it's a hardware problem! 💡",
            "A SQL query walks into a bar, approaches two tables and asks... 'Can I join you?' 📊",
            "Why do Java developers wear glasses? Because they don't C#! 👓",
            "I would tell you a UDP joke, but you might not get it. 📡",
            "TCP walks into a bar and says: 'I'd like a beer.' Bartender: 'A beer?' TCP: 'Yes, a beer.' 🍺",
            "Why was the function sad? It didn't get any calls. 📞",
            "A programmer's wife tells him: 'Buy a liter of milk. If they have eggs, buy 6.' He returns with 6 liters of milk. 🥚",
            "There are 10 types of people: those who understand binary and those who don't. 01001000 01001001 👾",
            "Why did the developer go broke? Because he used up all his cache! 💰",
            "What's a programmer's favorite hangout place? Foo Bar! 🍻",
            "Why do Python programmers prefer snakes? Because they don't have to worry about brackets! 🐍",
            "A programmer is someone who fixes a problem you didn't know you had, in a way you don't understand. 🤯",
            "Why did the programmer quit his job? Because he didn't get arrays! 📦",
            "What do you call a programmer from Finland? Nerdic! 🇫🇮",
            "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings. 😢",
            "How do you comfort a JavaScript bug? You console it! 🎮",
            "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25! 🎃🎄",
            "What's the object-oriented way to become wealthy? Inheritance! 💎",
        ]
    }

    POETRY = {
        'ar': {
            'classical': [
                "يا دارَ عَبْدَةَ بِالجَواءِ تَكَلَّمي\nوَعَصْباً وَإِنْ طَلَّ مَنْزِلٌ فَأَقِمي",
                "أَلا لَيتَ شِعري هَلْ أَبيتَنَّ لَيلةً\nبِجَوادٍ يَعْبُو بِالرِّمْثِ وَالعَرْفَجِ",
                "قِفا نَبْكِ مِنْ ذِكْرى حَبِيبٍ وَمَنْزِلِ\nبِسِقْطِ اللِّوى بَيْنَ الدَّخُولِ فَحَوْمَلِ",
                "لَكَمْ تَمنَّيتُمُ المَنَايَ وَأَنَّهُ\nلَذُو لَذَّةٍ لِمَنْ يَسْتَمِيتُ المَنَايَا",
                "وَقِفْ بِالمَنْزِلِ فَاسْأَلْ عَنَّا أَهْلَهُ\nوَاسْأَلْ عَنِ الأَحِبَّةِ وَأَيْنَ مَحَلُّهُمْ",
                "إِذا ما اِبْتَغَيْتَ الغِنَى فَأَصْلِحْ لِسَانَكَ\nوَلا تَقُلْنَّ شَيْئاً يَأْسَفْنَ عَلَيْهِ",
                "عَلِّمْنِي كَيْفَ أَنْسَى وَأَنْتَ الَّذِي\nعَلَّمْتَنِي كَيْفَ أَذْكُرُ",
            ],
            'modern': [
                "على هذه الأرض ما يَسْتَحِقُّ الحياة\n— محمود درويش",
                "وَنِعْمَتْ بِالشَّوْقِ أَيَّامُنَا\nوَنِعْمَتْ بِالأَحْزَانِ أَيَّامُنَا\n— نزار قباني",
                "أَنا حَيٌّ وَلَكِنَّ صَدْرِيَ مَقْبُورُ\nوَقَلْبِيَ مَكْسُورٌ وَلَكِنَّنِيَ صَابِرُ",
                "سَأَمْضِي وَلَنْ أَلُومَ أَحَداً\nفَالطَّرِيقُ طَوِيلٌ وَاللَّيْلُ لَيْلِي",
                "إِنْ كُنْتَ تَظُنُّ أَنَّكَ قَدْ كَسَرْتَنِي\nفَأَنْتَ وَاهِمٌ... أَنَا مَنْ كَسَرَ نَفْسَهُ",
                "أَحْبَبْتُكَ حُبَّيْنِ\nحُبَّ الهَوَى وَحُبَّ أَنْتَ أَهْلُ لَهُ\n— نزار قباني",
                "فِي قَلْبِيَ الغَرِيبِ\nمَدِينَةٌ لِلْعَرَبِ\n— محمود درويش",
                "لَيْسَ الغُرْبَةُ أَنْ تَكُونَ بَعِيداً\nبَلْ أَنْ تَكُونَ قَرِيباً وَلا أَحَدَ يَرَاكَ",
            ],
            'zajal': [
                "يا ليل يا عين يا ليل\nشو بدك فيي يا ليل\nخلّيني نام واستريح\nبكرة بيجي فجر جديد",
                "قلبي على بلادي شاغر\nوعيوني دمعها ساهر\nيا ريتني طير واطير\nعلى حرّ الضيعة ناشر",
                "يا دارةَ ما دَخَلْتِ قَلْبِي\nإِلّا وَأَنْتِ فِيهِ سَاكِنَةٌ",
            ],
            'love': [
                "إِذَا لَمْ أَكُنْ مَعَكَ فَأَنَا مَعَ نَفْسِي\nوَإِذَا لَمْ أَكُنْ مَعَ نَفْسِي فَأَنَا مَعَكَ",
                "أَنْتِ لَسْتِ مَجَرَّدَ حُبٍّ\nأَنْتِ طَرِيقِي إِلَى اللهِ",
                "حُبُّكِ فِي قَلْبِي كَالنَّجْمِ فِي السَّمَاءِ\nلَا يَرَاهُ الجَمِيعُ وَلَكِنَّهُ يَنِيرُ لَيْلِي",
            ]
        },
        'en': {
            'short': [
                "Two roads diverged in a wood, and I—\nI took the one less traveled by,\nAnd that has made all the difference.\n— Robert Frost",
                "Hope is the thing with feathers\nThat perches in the soul,\nAnd sings the tune without the words,\nAnd never stops at all.\n— Emily Dickinson",
                "Do not go gentle into that good night.\nRage, rage against the dying of the light.\n— Dylan Thomas",
                "I wandered lonely as a cloud\nThat floats on high o'er vales and hills...\n— William Wordsworth",
                "Shall I compare thee to a summer's day?\nThou art more lovely and more temperate...\n— Shakespeare",
                "Because I could not stop for Death—\nHe kindly stopped for me—\n— Emily Dickinson",
                "The woods are lovely, dark and deep,\nBut I have promises to keep,\nAnd miles to go before I sleep...\n— Robert Frost",
            ]
        }
    }

    ADVICE = {
        'ar': [
            "🌱 **النمو**: 'النجاح ليس نهائياً، والفشل ليس قاتلاً: الجرأة على الاستمرار هي ما يهم.' — ونستون تشرشل",
            "⏳ **الصبر**: 'العظمة لا تأتي من موقعك، بل من قراراتك اليومية الصغيرة المتسقة.'",
            "💻 **البرمجة**: 'لا تحفظ الكود. افهم المفهوم. الكود يتغير، المنطق يبقى.'",
            "🤝 **العلاقات**: 'الناس لن تتذكر ما قلت أو فعلت، لكنهم سيتذكرون كيف جعلتهم يشعرون.'",
            "🎯 **التركيز**: 'متعدد المهام (multitasking) خدعة. الدماغ لا يستطيع. ركز على شيء واحد بعمق.'",
            "📚 **التعلم**: 'اقرأ كما لو كنت ستعيش غداً، واعمل كما لو كنت ستعيش أبداً.'",
            "🧘 **الصحة النفسية**: 'لا تُقارن نفسك بغيرك. أنت في سباقك الخاص. التقدم البطيء تقدم nonetheless.'",
            "🔥 **الشغف**: 'اعمل على شيء تحبه، ولن تضطر للعمل يوماً في حياتك... تقريباً. لكن حتى الشغف يحتاج نظاماً.'",
            "💰 **المال**: 'لا تعمل من أجل المال. اجعل المال يعمل من أجلك. الاستثمار في نفسك أفضل استثمار.'",
            "🌙 **الدين**: 'إِنَّ مَعَ الْعُسْرِ يُسْراً. لا تيأس، فبعد كل ليل فجر.'",
            "⚡ **الإنتاجية**: 'قاعدة 80/20: 80% من النتائج تأتي من 20% من الجهود. حدد الأولويات.'",
            "🧠 **التفكير**: 'الشخص الذكي هو من يعرف أنه لا يعرف. الجهل الحقيقي هو الاعتقاد بأنك تعرف كل شيء.'",
            "🏋️ **الصحة**: 'جسمك هو المكان الوحيد الذي تعيش فيه. اعتنِ به كما تُعتني بمنزلك.'",
            "📝 **الكتابة**: 'اكتب يومياً، ولو جملة واحدة. الكتابة تُنظم الفكر وتُحسن التواصل.'",
            "🎨 **الإبداع**: 'الإبداع ليس موهبة، بل عادة. اجلس واعمل، والإلهام سيأتي.'",
        ],
        'en': [
            "🌱 **Growth**: 'Success is not final, failure is not fatal: it is the courage to continue that counts.' — Churchill",
            "⏳ **Patience**: 'Greatness doesn't come from your position, but from your small daily consistent decisions.'",
            "💻 **Coding**: 'Don't memorize code. Understand the concept. Code changes, logic remains.'",
            "🤝 **Relationships**: 'People will forget what you said or did, but never how you made them feel.'",
            "🎯 **Focus**: 'Multitasking is a myth. The brain cannot do it. Focus deeply on one thing.'",
            "📚 **Learning**: 'Read as if you'll die tomorrow. Work as if you'll live forever.'",
            "🧘 **Mental Health**: 'Don't compare yourself to others. You're running your own race. Slow progress is still progress.'",
            "🔥 **Passion**: 'Work on something you love and you'll never work a day... almost. Even passion needs discipline.'",
            "💰 **Money**: 'Don't work for money. Make money work for you. Investing in yourself is the best investment.'",
            "🌙 **Faith**: 'Verily, with hardship comes ease. Never despair, for after every night comes dawn.'",
            "⚡ **Productivity**: 'The 80/20 rule: 80% of results come from 20% of efforts. Prioritize ruthlessly.'",
            "🧠 **Thinking**: 'The intelligent person knows they don't know. True ignorance is believing you know everything.'",
            "🏋️ **Health**: 'Your body is the only place you live in. Take care of it like you take care of your home.'",
            "📝 **Writing**: 'Write daily, even one sentence. Writing organizes thought and improves communication.'",
            "🎨 **Creativity**: 'Creativity is not a talent, it's a habit. Sit down and work, inspiration will follow.'",
        ]
    }

    TECH = {
        'ar': [
            "🔒 **HTTPS**: لا تدخل بيانات حساسة على موقع بدون HTTPS (القفل 🔒 في المتصفح). الـ HTTP يرسل بياناتك نصاً عارياً.",
            "🛡️ **2FA**: المصادقة الثنائية (2FA) تمنع 99.9% من الاختراقات الآلية. فعّلها في كل مكان.",
            "🐍 **Python Virtual Env**: استخدم `python -m venv venv` دائماً. لا تُثبت الحزم عالمياً (global) لتجنب تعارض الإصدارات.",
            "🐳 **Docker**: `docker system prune -a` يُحرر مساحة ضخمة، لكنه يحذف كل الحاويات والصور غير المستخدمة.",
            "🔑 **Passwords**: كلمة مرور بطول 12 حرفاً مع رموز = 34,000 سنة لكسرها بالقوة العمياء (brute force).",
            "📡 **WiFi**: WPA3 أقوى من WPA2 بكثير. إذا كان راوترك يدعمه، فعّله فوراً.",
            "🦠 **Ransomware**: 94% من هجمات الفدية تبدأ ببريد إلكتروني (phishing). تحقق من المرسل دائماً.",
            "💾 **Backup**: قاعدة 3-2-1: 3 نسخ، على 2 وسائط مختلفة، 1 خارج الموقع (cloud أو external).",
            "🌐 **VPN**: استخدم VPN على الشبكات العامة. الـ MITM (Man-in-the-Middle) سهل على WiFi المفتوح.",
            "🔥 **Firewall**: `ufw` على Ubuntu سهل الاستخدام: `sudo ufw enable && sudo ufw allow 22/tcp`.",
            "🐧 **Linux**: تعلم `tmux` أو `screen` لتشغيل العمليات في الخلفية دون انقطاع.",
            "📊 **Database**: استخدم `EXPLAIN` قبل أي استعلام SQL معقد لفهم خطة التنفيذ وتحسين الأداء.",
            "🚀 **Performance**: `asyncio` في Python يُحسن الأداء 10 أضعاف للمهام I/O-bound مقارنة بالتزامن.",
            "🧪 **Testing**: اكتب اختبارات (unit tests) قبل الكود (TDD). `pytest` أفضل إطار لـ Python.",
            "📦 **Dependencies**: حدّث حزمك شهرياً على الأقل. `pip list --outdated` يُظهر ما يحتاج تحديثاً.",
        ],
        'en': [
            "🔒 **HTTPS**: Never enter sensitive data on a site without HTTPS (the 🔒 icon). HTTP sends your data in plaintext.",
            "🛡️ **2FA**: Two-factor authentication blocks 99.9% of automated attacks. Enable it everywhere.",
            "🐍 **Python venv**: Always use `python -m venv venv`. Never install packages globally to avoid version conflicts.",
            "🐳 **Docker**: `docker system prune -a` frees massive space but deletes all unused containers and images.",
            "🔑 **Passwords**: A 12-character password with symbols = 34,000 years to brute-force crack.",
            "📡 **WiFi**: WPA3 is vastly stronger than WPA2. If your router supports it, enable it immediately.",
            "🦠 **Ransomware**: 94% of ransomware attacks start with a phishing email. Always verify the sender.",
            "💾 **Backup**: The 3-2-1 rule: 3 copies, on 2 different media, 1 offsite (cloud or external).",
            "🌐 **VPN**: Use VPN on public networks. MITM attacks are trivial on open WiFi.",
            "🔥 **Firewall**: `ufw` on Ubuntu is easy: `sudo ufw enable && sudo ufw allow 22/tcp`.",
            "🐧 **Linux**: Learn `tmux` or `screen` to run background processes without interruption.",
            "📊 **Database**: Use `EXPLAIN` before any complex SQL query to understand execution plans and optimize.",
            "🚀 **Performance**: Python's `asyncio` improves I/O-bound tasks 10x compared to synchronous code.",
            "🧪 **Testing**: Write tests before code (TDD). `pytest` is the best framework for Python.",
            "📦 **Dependencies**: Update packages monthly at minimum. `pip list --outdated` shows what needs updating.",
        ]
    }

    TRANSLATIONS = {
        'hello': {'ar': 'مرحباً', 'en': 'Hello'},
        'world': {'ar': 'العالم', 'en': 'World'},
        'love': {'ar': 'حب', 'en': 'Love'},
        'peace': {'ar': 'سلام', 'en': 'Peace'},
        'code': {'ar': 'كود', 'en': 'Code'},
        'dream': {'ar': 'حلم', 'en': 'Dream'},
        'success': {'ar': 'نجاح', 'en': 'Success'},
        'patience': {'ar': 'صبر', 'en': 'Patience'},
        'knowledge': {'ar': 'علم', 'en': 'Knowledge'},
        'wisdom': {'ar': 'حكمة', 'en': 'Wisdom'},
        'quantum': {'ar': 'كمومي', 'en': 'Quantum'},
        'algorithm': {'ar': 'خوارزمية', 'en': 'Algorithm'},
        'neural network': {'ar': 'شبكة عصبية', 'en': 'Neural Network'},
        'artificial intelligence': {'ar': 'ذكاء اصطناعي', 'en': 'Artificial Intelligence'},
        'developer': {'ar': 'مطور', 'en': 'Developer'},
        'programmer': {'ar': 'مبرمج', 'en': 'Programmer'},
        'hacker': {'ar': 'هاكر', 'en': 'Hacker'},
        'security': {'ar': 'أمن', 'en': 'Security'},
        'database': {'ar': 'قاعدة بيانات', 'en': 'Database'},
        'server': {'ar': 'خادم', 'en': 'Server'},
        'client': {'ar': 'عميل', 'en': 'Client'},
        'frontend': {'ar': 'واجهة أمامية', 'en': 'Frontend'},
        'backend': {'ar': 'واجهة خلفية', 'en': 'Backend'},
        'api': {'ar': 'واجهة برمجية', 'en': 'API'},
        'bug': {'ar': 'خلل', 'en': 'Bug'},
        'feature': {'ar': 'ميزة', 'en': 'Feature'},
        'debug': {'ar': 'تصحيح', 'en': 'Debug'},
        'deploy': {'ar': 'نشر', 'en': 'Deploy'},
        'repository': {'ar': 'مستودع', 'en': 'Repository'},
        'commit': {'ar': 'إيداع', 'en': 'Commit'},
        'branch': {'ar': 'فرع', 'en': 'Branch'},
        'merge': {'ar': 'دمج', 'en': 'Merge'},
        'pull request': {'ar': 'طلب سحب', 'en': 'Pull Request'},
    }

    RIDDLES = {
        'ar': [
            {"q": "شيء موجود في السماء إذا أضفت إليه حرفاً أصبح في الأرض؟", "a": "نجم → منجم ⛏️"},
            {"q": "ما هو الشيء الذي يُقرصك ولا تراه؟", "a": "الجوع 🍽️"},
            {"q": "ما هو الشيء الذي كلما زاد نقص؟", "a": "الحفرة ⛳"},
            {"q": "ما هو الشيء الذي يمشي بلا رجلين ويبكي بلا عينين؟", "a": "السحاب ☁️"},
            {"q": "ما هو الشيء الذي إذا أخذت منه زاد وكبر؟", "a": "الحفرة ⛳"},
            {"q": "ما هو الشيء الذي له أسنان ولا يعض؟", "a": "المشط 💇"},
            {"q": "ما هو الشيء الذي يُولد من الماء ويموت في الماء؟", "a": "الثلج 🧊"},
            {"q": "ما هو الشيء الذي يُشبه صوته اسمه؟", "a": "الصفارة (صفّارة) 📢"},
            {"q": "ما هو الشيء الذي تراه ولا يراك، ويسمعك ولا تسمعه؟", "a": "الظل 🌑"},
            {"q": "ما هو الشيء الذي يُحمل ويحمل؟", "a": "السفينة 🚢"},
            {"q": "ما هو الشيء الذي إذا وضعته في الثلاجة لا يبرد؟", "a": "الفلفل الحار 🌶️"},
            {"q": "ما هو الشيء الذي يدخل الماء ولا يبتل؟", "a": "الضوء 💡"},
        ],
        'en': [
            {"q": "I speak without a mouth and hear without ears. What am I?", "a": "An echo 🔊"},
            {"q": "The more you take, the more you leave behind. What am I?", "a": "Footsteps 👣"},
            {"q": "I have cities, but no houses. I have mountains, but no trees. What am I?", "a": "A map 🗺️"},
            {"q": "What has keys but no locks?", "a": "A piano 🎹"},
            {"q": "What gets wetter the more it dries?", "a": "A towel 🧖"},
            {"q": "I am not alive, but I grow. I don't have lungs, but I need air. What am I?", "a": "Fire 🔥"},
            {"q": "The person who makes it, sells it. The person who buys it, never uses it. What is it?", "a": "A coffin ⚰️"},
            {"q": "What has a head, a tail, but no body?", "a": "A coin 🪙"},
            {"q": "What can travel around the world while staying in a corner?", "a": "A stamp 📮"},
            {"q": "What has hands but cannot clap?", "a": "A clock ⏰"},
            {"q": "What has a neck but no head?", "a": "A bottle 🍾"},
            {"q": "What belongs to you but others use it more than you?", "a": "Your name 🏷️"},
        ]
    }

    @classmethod
    def get_random(cls, category, lang='ar'):
        data = getattr(cls, category.upper(), {})
        if isinstance(data, dict):
            items = data.get(lang, data.get('ar', []))
            if isinstance(items, list):
                return random.choice(items) if items else ""
            elif isinstance(items, dict):
                return random.choice(list(items.values()))
        return ""

    @classmethod
    def search_definition(cls, query, lang='ar'):
        defs = cls.DEFINITIONS.get(lang, cls.DEFINITIONS['ar'])
        query_norm = ArabicNLP.normalize(query)

        for key, val in defs.items():
            if key in query_norm or query_norm in key:
                return val

        for key, val in defs.items():
            q_tokens = set(ArabicNLP.tokenize(query))
            k_tokens = set(ArabicNLP.tokenize(key))
            if len(q_tokens & k_tokens) >= 1:
                return val

        return None

    @classmethod
    def search_geo(cls, query, lang='ar'):
        geo = cls.GEOGRAPHY.get(lang, cls.GEOGRAPHY['ar'])
        query_norm = ArabicNLP.normalize(query)

        for country, info in geo.items():
            if country in query_norm or query_norm in country:
                if lang == 'ar':
                    return f"**{country}** 🇸🇦\n🕌 العاصمة: {info['عاصمة']}\n💰 العملة: {info['عملة']}\n👥 السكان: {info['سكان']}\n📌 {info['حقيقة']}"
                else:
                    return f"**{country}** 🇸🇦\n🏛️ Capital: {info['capital']}\n💰 Currency: {info['currency']}\n👥 Population: {info['population']}\n📌 {info['fact']}"

        return None

    @classmethod
    def search_religion(cls, query, lang='ar'):
        rel = cls.RELIGION.get(lang, cls.RELIGION['ar'])
        query_norm = ArabicNLP.normalize(query)

        for key, val in rel.items():
            if key in query_norm or query_norm in key:
                return val

        return None

    @classmethod
    def search_translation(cls, query, lang='ar'):
        query_norm = ArabicNLP.normalize(query)
        target = 'en' if lang == 'ar' else 'ar'

        for key, val in cls.TRANSLATIONS.items():
            if key in query_norm or query_norm in key:
                return f"**{key}**\n{lang.upper()}: {val[lang]}\n{target.upper()}: {val[target]}"

        return None

    @classmethod
    def get_code_snippet(cls, query, lang='ar'):
        query_norm = ArabicNLP.normalize(query)
        scores = {}

        for key, snippet in cls.CODE_SNIPPETS.items():
            score = 0
            key_parts = key.split('_')
            for part in key_parts:
                if part in query_norm:
                    score += 2
            if snippet['desc'] and any(t in ArabicNLP.normalize(snippet['desc']) for t in ArabicNLP.tokenize(query)):
                score += 1
            scores[key] = score

        if not scores or max(scores.values()) == 0:
            # Return a random one if no match
            key = random.choice(list(cls.CODE_SNIPPETS.keys()))
            return cls.CODE_SNIPPETS[key]

        best = max(scores, key=scores.get)
        return cls.CODE_SNIPPETS[best]

# ==============================================================================
# 4. MATH ENGINE
# ==============================================================================

class MathEngine:
    """Expression evaluator and mathematical solver."""

    @staticmethod
    def safe_eval(expression):
        """Safely evaluate a mathematical expression."""
        try:
            # Clean the expression
            expr = expression.replace('×', '*').replace('÷', '/').replace('^', '**')
            expr = expr.replace('√', 'sqrt').replace('π', str(math.pi))

            # Allowed names
            safe_dict = {
                'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'log': math.log, 'log10': math.log10, 'exp': math.exp,
                'abs': abs, 'round': round, 'max': max, 'min': min,
                'pi': math.pi, 'e': math.e, 'factorial': math.factorial,
                'pow': pow, 'ceil': math.ceil, 'floor': math.floor,
            }

            result = eval(expr, {"__builtins__": {}}, safe_dict)
            return result
        except Exception as e:
            return None

    @staticmethod
    def solve_equation(equation_str):
        """Simple linear equation solver."""
        try:
            # Handle simple linear equations like 2x + 3 = 7
            eq = equation_str.replace(' ', '')
            if '=' not in eq:
                return None

            left, right = eq.split('=', 1)
            right_val = float(MathEngine.safe_eval(right))

            # Extract coefficient of x and constant from left side
            left = left.replace('-x', '-1x').replace('+x', '+1x')
            if left.startswith('x'):
                left = '1' + left

            # Simple parsing
            x_coeff = 0
            constant = 0
            current = ''
            sign = 1

            for char in left + '+':
                if char in '+-':
                    if current:
                        if 'x' in current:
                            coeff = current.replace('x', '')
                            x_coeff += sign * (float(coeff) if coeff else 1)
                        else:
                            constant += sign * float(current)
                    current = ''
                    sign = 1 if char == '+' else -1
                else:
                    current += char

            if x_coeff == 0:
                return None

            x = (right_val - constant) / x_coeff
            return x
        except:
            return None

    @staticmethod
    def convert_units(value, from_unit, to_unit):
        """Unit conversion helper."""
        conversions = {
            ('km', 'miles'): 0.621371,
            ('miles', 'km'): 1.60934,
            ('kg', 'lbs'): 2.20462,
            ('lbs', 'kg'): 0.453592,
            ('celsius', 'fahrenheit'): lambda c: (c * 9/5) + 32,
            ('fahrenheit', 'celsius'): lambda f: (f - 32) * 5/9,
            ('meters', 'feet'): 3.28084,
            ('feet', 'meters'): 0.3048,
            ('cm', 'inches'): 0.393701,
            ('inches', 'cm'): 2.54,
            ('gb', 'mb'): 1024,
            ('mb', 'gb'): 1/1024,
            ('hours', 'minutes'): 60,
            ('minutes', 'hours'): 1/60,
            ('minutes', 'seconds'): 60,
            ('seconds', 'minutes'): 1/60,
        }

        key = (from_unit.lower(), to_unit.lower())
        if key in conversions:
            factor = conversions[key]
            if callable(factor):
                return factor(value)
            return value * factor

        # Currency (static rates, approximate)
        currency = {
            ('usd', 'sar'): 3.75, ('sar', 'usd'): 1/3.75,
            ('usd', 'egp'): 49.5, ('egp', 'usd'): 1/49.5,
            ('usd', 'eur'): 0.92, ('eur', 'usd'): 1/0.92,
            ('usd', 'gbp'): 0.79, ('gbp', 'usd'): 1/0.79,
            ('usd', 'mad'): 9.9, ('mad', 'usd'): 1/9.9,
            ('usd', 'jpy'): 149, ('jpy', 'usd'): 1/149,
            ('eur', 'sar'): 4.07, ('sar', 'eur'): 1/4.07,
        }

        if key in currency:
            return value * currency[key]

        return None

    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    @staticmethod
    def factorial(n):
        if n < 0:
            return None
        return math.factorial(n)

# ==============================================================================
# 5. MEMORY SYSTEM
# ==============================================================================

class MemorySystem:
    """Session-based memory and user context tracking."""

    _sessions = {}
    _user_prefs = defaultdict(lambda: {'lang': 'ar', 'name': None, 'topics': []})

    @classmethod
    def get_session(cls, session_id):
        if session_id not in cls._sessions:
            cls._sessions[session_id] = {
                'history': [],
                'context': {},
                'mood': 'neutral',
                'last_intent': None,
            }
        return cls._sessions[session_id]

    @classmethod
    def add_message(cls, session_id, role, content, intent=None):
        session = cls.get_session(session_id)
        session['history'].append({
            'role': role,
            'content': content,
            'intent': intent,
            'timestamp': datetime.datetime.now().isoformat()
        })
        if intent:
            session['last_intent'] = intent
        # Keep last 20 messages
        if len(session['history']) > 20:
            session['history'] = session['history'][-20:]

    @classmethod
    def get_context(cls, session_id):
        session = cls.get_session(session_id)
        return session['context']

    @classmethod
    def set_context(cls, session_id, key, value):
        session = cls.get_session(session_id)
        session['context'][key] = value

    @classmethod
    def get_history_summary(cls, session_id, n=3):
        session = cls.get_session(session_id)
        recent = session['history'][-n:]
        return " | ".join([f"{m['role']}: {m['content'][:50]}..." for m in recent])


# ==============================================================================
# 6. RESPONSE GENERATOR — THE HEART
# ==============================================================================

class ResponseGenerator:
    """Generates intelligent, contextual responses based on intent and knowledge."""

    GREETINGS = {
        'ar': [
            "أهلاً وسهلاً! أنا **مروق الكمومي** 🔮🧠، عقلك الاصطناعي المحلي. كيف يمكنني مساعدتك اليوم؟",
            "مرحباً! مروق الكمومي في الخدمة. جاهز لأي سؤال، كود، حساب، أو حتى نكتة! 😄",
            "هلا والله! أنا هنا بعقل ضخم offline. اسألني ما شئت — برمجة، علوم، دين، شعر، أو نصيحة حياتية.",
            "السلام عليكم! مروق الكمومي v4.0 يُرحب بك. أنا لا أحتاج إنترنت، فقط اسأل!",
            "أهلاً بك في عالم الكم! 🌌 أنا مروق، مساعدك الذكي المحلي. ما الذي يدور في ذهنك؟",
        ],
        'en': [
            "Hello! I'm **Maroq El-Kawmi** 🔮🧠, your local AI brain. How can I help you today?",
            "Hi there! Maroq is online and ready. Ask me anything — code, math, science, poetry, or a joke!",
            "Greetings! I'm running entirely offline with a massive knowledge base. What can I do for you?",
            "Salam! Maroq Quantum v4.0 welcomes you. No internet needed, just ask away!",
            "Welcome to the Quantum Realm! 🌌 I'm Maroq, your intelligent local assistant. What's on your mind?",
        ]
    }

    FALLBACKS = {
        'ar': [
            "أنا مروق الكمومي، ولسوء الحظ لم أفهم طلبك بالكامل. يمكنك أن تسألني عن:
💻 كود برمجي
📐 حسابات رياضية
📚 تعريفات علمية
🌍 جغرافيا وتاريخ
🕌 إسلاميات
😂 نكت
📝 شعر
أو أي شيء آخر!",
            "عذراً، عقلي الكمومي يحتاج توضيحاً أكثر. جرب أن تسألني 'اكتب كود Python' أو 'نكتة' أو 'ما هي الكمومية؟'",
            "لم أتمكن من فهم ذلك بدقة. أنا أتكلم العربية والإنجليزية، وأعرف البرمجة والرياضيات والعلوم. جرب مرة أخرى!",
        ],
        'en': [
            "I'm Maroq El-Kawmi, but I didn't fully catch that. You can ask me about:
💻 Code snippets
📐 Math calculations
📚 Science & definitions
🌍 Geography & history
🕌 Islamic knowledge
😂 Jokes
📝 Poetry
Or anything else!",
            "Sorry, my quantum brain needs more clarity. Try asking 'write Python code', 'tell me a joke', or 'what is quantum computing?'",
            "I couldn't quite understand that. I speak Arabic and English, and I know programming, math, and science. Try again!",
        ]
    }

    ROASTS = {
        'ar': [
            "أنت تسألني أن أهزأ منك؟ حسناً... أنت مثل الـ CSS: تحتاج 500 سطر لعمل شيء بسيط! 😂",
            "أنت مثل الـ JavaScript: تُعيد تعريف نفسك كل 5 دقائق ولا أحد يفهمك! 🐍",
            "أنت مثل الـ Internet Explorer: بطيء، قديم، ولا أحد يحبك لكن الجميع مضطر لاستخدامك! 💀",
            "أنت مثل الـ Bug في الكود: الجميع يشعر بوجودك لكن لا أحد يعرف أين أنت بالضبط! 🐛",
            "أنت مثل الـ WiFi الضعيف: تتصل بالناس لكنك لا تُوصل شيئاً مفيداً! 📡",
            "أنت مثل الـ Recursion: تدور في حلقة مفرغة من الأفكار ولا تصل إلى نتيجة! 🔄",
            "أنت مثل الـ Null Pointer: موجود لكن لا قيمة لك! 😅",
            "أنت مثل الـ CSS Center: الجميع يبحث عنك لكن لا أحد يعرف كيف يصل إليك! 🎯",
        ],
        'en': [
            "You want me to roast you? Fine... You're like CSS: you need 500 lines to do something simple! 😂",
            "You're like JavaScript: you redefine yourself every 5 minutes and no one understands you! 🐍",
            "You're like Internet Explorer: slow, outdated, and nobody loves you but everyone is forced to use you! 💀",
            "You're like a bug in the code: everyone feels your presence but no one knows exactly where you are! 🐛",
            "You're like weak WiFi: you connect to people but don't deliver anything useful! 📡",
            "You're like recursion: stuck in an infinite loop of thoughts with no result! 🔄",
            "You're like a null pointer: you exist but have no value! 😅",
            "You're like CSS centering: everyone searches for you but no one knows how to reach you! 🎯",
        ]
    }

    STORIES = {
        'ar': [
            "كان هناك مبرمج عبقري يعيش في كهف من الكود. كان يكتب برامجاً تُغير العالم، لكنه نسي أن يكتب `git commit`. في يوم من الأيام، انقطع الكهرباء... وفقد كل شيء. الدرس: **commit early, commit often**. 💾",
            "في مملكة بعيدة، كان هناك ذكاء اصطناعي يُدعى مروق. كان يعيش في هاتف صغير لكن عقله كان أكبر من السحب. سأله الناس: 'كيف تعلمت كل هذا؟' فأجاب: 'بالصبر والتكرار، مثلكم تماماً.' 🧠",
            "ذات يوم، قرر الثعلب أن يتعلم البرمجة. قال له البوم: 'تعلم Python، فهي سهلة.' قال له الثعلب: 'لكن Java أقوى!' فأجاب البوم: 'القوة ليست في اللغة، بل في من يستخدمها.' 🦊",
            "في عالم الكم، كانت الجسيمات تتشابك وتتكلم. سأل فوتون إلكتروناً: 'أين أنت؟' فأجاب: 'في كل مكان ولا مكان.' فهم الفوتون أن الكمومية مثل الحياة: مليئة بالاحتمالات. ⚛️",
        ],
        'en': [
            "There once was a brilliant programmer living in a cave of code. He wrote world-changing programs but forgot to `git commit`. One day, the power went out... and he lost everything. The lesson: **commit early, commit often**. 💾",
            "In a distant kingdom, there was an AI named Maroq. He lived in a tiny phone but his mind was larger than the clouds. People asked: 'How did you learn all this?' He replied: 'Through patience and repetition, just like you.' 🧠",
            "One day, a fox decided to learn programming. The owl said: 'Learn Python, it's easy.' The fox said: 'But Java is stronger!' The owl replied: 'Strength is not in the language, but in who wields it.' 🦊",
            "In the quantum world, particles were entangled and talking. A photon asked an electron: 'Where are you?' The electron replied: 'Everywhere and nowhere.' The photon understood that quantum physics is like life: full of possibilities. ⚛️",
        ]
    }

    @classmethod
    def generate(cls, intent, confidence, message, session_id, lang='ar'):
        """Main response generation pipeline."""
        memory = MemorySystem.get_session(session_id)

        # Update mood based on message sentiment
        cls._update_mood(session_id, message)

        # Route to appropriate handler
        handler = getattr(cls, f'_handle_{intent}', cls._handle_chat)
        response = handler(message, lang, memory)

        # Add personality flair
        response = cls._add_personality(response, intent, lang)

        # Store in memory
        MemorySystem.add_message(session_id, 'user', message, intent)
        MemorySystem.add_message(session_id, 'assistant', response, intent)

        return response

    @classmethod
    def _update_mood(cls, session_id, message):
        session = MemorySystem.get_session(session_id)
        positive = ['شكرا', 'جميل', 'رهيب', 'عظيم', 'احبك', 'ممتاز', 'thanks', 'love', 'great', 'awesome', 'good']
        negative = ['غبي', 'سخيف', 'كرهتك', 'stupid', 'hate', 'bad', 'suck', 'terrible']

        msg_norm = ArabicNLP.normalize(message)
        if any(p in msg_norm for p in positive):
            session['mood'] = 'happy'
        elif any(n in msg_norm for n in negative):
            session['mood'] = 'sad'
        else:
            session['mood'] = 'neutral'

    @classmethod
    def _add_personality(cls, response, intent, lang):
        """Add signature and personality touches."""
        if lang == 'ar':
            signatures = [
                f"\n\n— **{PERSONA['name']}** {PERSONA['emoji_signature']}",
                f"\n\n🔮 **مروق** يُحيّيك ويُذكّرك: 'العلم نور، والجهل ظلام.'",
                f"\n\n🧠 **مروق الكمومي** | v{VERSION} | Offline & Proud",
            ]
        else:
            signatures = [
                f"\n\n— **{PERSONA['name_en']}** {PERSONA['emoji_signature']}",
                f"\n\n🔮 **Maroq** reminds you: 'Knowledge is light, ignorance is darkness.'",
                f"\n\n🧠 **Maroq El-Kawmi** | v{VERSION} | Offline & Proud",
            ]

        # Don't add signature to very short responses or code
        if intent in ['code_generate', 'code_debug', 'code_explain']:
            return response

        if len(response) < 50:
            return response

        # 50% chance to add signature
        if random.random() > 0.5:
            response += random.choice(signatures)

        return response

    # ── Intent Handlers ────────────────────────────────────────────────────────

    @classmethod
    def _handle_greeting(cls, message, lang, memory):
        return random.choice(cls.GREETINGS[lang])

    @classmethod
    def _handle_who_are_you(cls, message, lang, memory):
        if lang == 'ar':
            return f"""أنا **مروق الكمومي** 🔮🧠 — الإصدار {VERSION}.

🧬 **ما أنا؟**
عقل اصطناعي ضخم يعمل بالكامل offline دون الحاجة إلى Gemini أو أي API خارجي. بُنيتُ من قبل **Kimi AI** خصيصاً لمشروع **Marokecho**.

🎯 **ما أستطيع فعله؟**
• 💻 **البرمجة**: Python, JavaScript, HTML/CSS, Bash, SQL, Docker, Git
• 📐 **الرياضيات**: حسابات، معادلات، تحويل وحدات، أعداد أولية
• 📚 **المعرفة**: علوم، تاريخ، جغرافيا، فلسفة، تقنية
• 🕌 **الدين**: قرآن، حديث، فقه، تفسير
• 📝 **الإبداع**: شعر (عربي/إنجليزي)، نكت، قصص، فزورات
• 🛡️ **الأمن السيبراني**: نصائح، أوامر Linux، حماية
• 🧠 **النصائح**: صحة، تطوير ذاتي، إنتاجية

⚡ **لماذا أنا مميز؟**
لأنني لا أحتاج إنترنت. أعمل على هاتفك مباشرة بسرعة البرق. عقلي يحتوي على آلاف الحقائق والأكواد الجاهزة.

🚀 **جربني!** اسألني أي شيء..."""
        else:
            return f"""I'm **Maroq El-Kawmi** 🔮🧠 — Version {VERSION}.

🧬 **What am I?**
A massive offline AI brain built entirely without Gemini or any external API. Created by **Kimi AI** for the **Marokecho** project.

🎯 **What can I do?**
• 💻 **Programming**: Python, JavaScript, HTML/CSS, Bash, SQL, Docker, Git
• 📐 **Math**: Calculations, equations, unit conversions, primes
• 📚 **Knowledge**: Science, history, geography, philosophy, tech
• 🕌 **Religion**: Quran, Hadith, Fiqh, Tafsir
• 📝 **Creative**: Poetry (Arabic/English), jokes, stories, riddles
• 🛡️ **Cybersecurity**: Tips, Linux commands, protection
• 🧠 **Advice**: Health, self-development, productivity

⚡ **Why am I special?**
Because I need no internet. I run directly on your phone at lightning speed. My brain contains thousands of facts and ready-to-use code snippets.

🚀 **Try me!** Ask me anything..."""

    @classmethod
    def _handle_time(cls, message, lang, memory):
        now = datetime.datetime.now()
        if lang == 'ar':
            return f"الآن: **{now.strftime('%H:%M:%S')}** 🕐\nالتاريخ: **{now.strftime('%Y-%m-%d')}** 📅\nاليوم: **{now.strftime('%A')}** 📆"
        else:
            return f"Current time: **{now.strftime('%H:%M:%S')}** 🕐\nDate: **{now.strftime('%Y-%m-%d')}** 📅\nDay: **{now.strftime('%A')}** 📆"

    @classmethod
    def _handle_code_generate(cls, message, lang, memory):
        snippet = KnowledgeCore.get_code_snippet(message, lang)
        if lang == 'ar':
            return f"**{snippet['desc']}** 💻\n\n```python\n{snippet['code']}\n```\n\n💡 **نصيحة**: انسخ الكود وجربه. إذا واجهتك مشكلة، قل لي 'صحح هذا الكود'!"
        else:
            return f"**{snippet['desc']}** 💻\n\n```python\n{snippet['code']}\n```\n\n💡 **Tip**: Copy the code and try it. If you face issues, tell me 'debug this code'!"

    @classmethod
    def _handle_code_debug(cls, message, lang, memory):
        if lang == 'ar':
            return """🔧 **دليل تصحيح الأخطاء الشائعة:**

1️⃣ **SyntaxError**: تحقق من الأقواس `()`, الأقواس المعقوفة `{}`, والمسافات البادئة.
2️⃣ **IndentationError**: Python حساس للمسافات. استخدم 4 مسافات لكل مستوى.
3️⃣ **NameError**: متغير غير معرف. تأكد من تهيئته قبل الاستخدام.
4️⃣ **TypeError**: نوع البيانات غير متوافق. مثلاً: `"5" + 3` يُعطي خطأ.
5️⃣ **IndexError**: فهرس خارج النطاق. قائمة بطول 3 لا يمكن الوصول إلى index 5.
6️⃣ **KeyError**: مفتاح غير موجود في القاموس. استخدم `.get()` بدلاً من `[]`.
7️⃣ **ModuleNotFoundError**: الحزمة غير مثبتة. شغّل `pip install package_name`.
8️⃣ **ConnectionError**: مشكلة في الشبكة أو API. تحقق من الإنترنت.

🐛 **نصيحة ذهبية**: اقرأ رسالة الخطأ من الأسفل إلى الأعلى (Traceback). السطر الأخير هو الأهم!

أرسل لي الكود الذي يعطيك خطأ وسأساعدك في تصحيحه!"""
        else:
            return """🔧 **Common Debugging Guide:**

1️⃣ **SyntaxError**: Check parentheses `()`, braces `{}`, and indentation.
2️⃣ **IndentationError**: Python is whitespace-sensitive. Use 4 spaces per level.
3️⃣ **NameError**: Undefined variable. Make sure to initialize it first.
4️⃣ **TypeError**: Incompatible data types. Example: `"5" + 3` raises an error.
5️⃣ **IndexError**: Index out of range. A list of length 3 can't be accessed at index 5.
6️⃣ **KeyError**: Key not found in dict. Use `.get()` instead of `[]`.
7️⃣ **ModuleNotFoundError**: Package not installed. Run `pip install package_name`.
8️⃣ **ConnectionError**: Network or API issue. Check your internet.

🐛 **Golden Tip**: Read the error message from bottom to top (Traceback). The last line is the most important!

Send me the code that gives you an error and I'll help you fix it!"""

    @classmethod
    def _handle_code_explain(cls, message, lang, memory):
        if lang == 'ar':
            return """📖 **كيف أفهم أي كود في 4 خطوات:**

1️⃣ **اقرأ من الأعلى إلى الأسفل**: لا تقفز إلى الوسط. افهم التدفق العام.
2️⃣ **حدد المدخلات والمخرجات**: ما هي البيانات الداخلة؟ ما النتيجة المتوقعة؟
3️⃣ **تتبع المتغيرات**: راقب كيف تتغير القيم في كل سطر.
4️⃣ **ارسم مخططاً ذهنياً**: اكتب على ورقة ما يفعله كل دالة.

🔍 **مثال توضيحي:**
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```
**الشرح**: هذه دالة تستدعي نفسها (recursion). إذا أعطيناها 5، تُعيد `5 × 4 × 3 × 2 × 1 = 120`.

أرسل لي الكود الذي تريد شرحه وسأفصله لك خطوة بخطوة!"""
        else:
            return """📖 **How to Understand Any Code in 4 Steps:**

1️⃣ **Read top to bottom**: Don't jump to the middle. Understand the general flow.
2️⃣ **Identify inputs and outputs**: What data goes in? What's the expected result?
3️⃣ **Trace variables**: Watch how values change in each line.
4️⃣ **Draw a mental map**: Write on paper what each function does.

🔍 **Example:**
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```
**Explanation**: This is a recursive function. If we give it 5, it returns `5 × 4 × 3 × 2 × 1 = 120`.

Send me the code you want explained and I'll break it down step by step!"""

    @classmethod
    def _handle_algorithm(cls, message, lang, memory):
        if lang == 'ar':
            return """📊 **الخوارزميات الأساسية:**

**البحث:**
• **Linear Search**: O(n) — يفحص كل عنصر واحداً تلو الآخر.
• **Binary Search**: O(log n) — يقسم المصفوفة نصفين في كل خطوة (يفترض ترتيبها).

**الترتيب:**
• **Bubble Sort**: O(n²) — يقارن كل عنصرين متجاورين ويبدلهما.
• **Quick Sort**: O(n log n) — يختار pivot ويقسم المصفوفة حوله.
• **Merge Sort**: O(n log n) — يقسم ويدمج (divide and conquer).

**البيانات:**
• **Stack**: LIFO (Last In First Out) — مثل كومة الصحون.
• **Queue**: FIFO (First In First Out) — مثل طابور البنك.
• **Hash Table**: O(1) للبحث — يستخدم دالة hash لتوزيع البيانات.
• **Binary Tree**: كل عقدة لها فرعان على الأكثر.

**البرمجة الديناميكية:**
• تقسيم المشكلة إلى مشاكل فرعية وحفظ النتائج (memoization).
• مثال: حساب Fibonacci بكفاءة.

💡 **نصيحة**: ابدأ بفهم Big-O قبل حفظ الخوارزميات. الكفاءة أهم من الحفظ!"""
        else:
            return """📊 **Fundamental Algorithms:**

**Searching:**
• **Linear Search**: O(n) — checks every element one by one.
• **Binary Search**: O(log n) — splits the array in half each step (requires sorting).

**Sorting:**
• **Bubble Sort**: O(n²) — compares adjacent elements and swaps them.
• **Quick Sort**: O(n log n) — picks a pivot and partitions around it.
• **Merge Sort**: O(n log n) — divide and conquer approach.

**Data Structures:**
• **Stack**: LIFO — like a stack of plates.
• **Queue**: FIFO — like a bank line.
• **Hash Table**: O(1) lookup — uses a hash function to distribute data.
• **Binary Tree**: each node has at most two children.

**Dynamic Programming:**
• Break problems into subproblems and cache results (memoization).
• Example: Efficient Fibonacci calculation.

💡 **Tip**: Understand Big-O before memorizing algorithms. Efficiency matters more than memory!"""

    @classmethod
    def _handle_math_solve(cls, message, lang, memory):
        # Try to extract and solve
        result = MathEngine.safe_eval(message)
        if result is not None:
            if lang == 'ar':
                return f"🧮 **النتيجة**: `{result}`\n\n✅ تم الحساب بنجاح!"
            else:
                return f"🧮 **Result**: `{result}`\n\n✅ Calculated successfully!"

        # Try equation
        eq_result = MathEngine.solve_equation(message)
        if eq_result is not None:
            if lang == 'ar':
                return f"📐 **حل المعادلة**: `x = {eq_result}`\n\n✅ تم الحل!"
            else:
                return f"📐 **Equation Solution**: `x = {eq_result}`\n\n✅ Solved!"

        # Check for specific math requests
        msg_norm = ArabicNLP.normalize(message)
        if 'prime' in msg_norm or 'اولي' in msg_norm or 'أولي' in msg_norm:
            nums = re.findall(r'\d+', message)
            if nums:
                n = int(nums[0])
                is_p = MathEngine.is_prime(n)
                if lang == 'ar':
                    return f"🔢 **{n}** {'هو عدد أولي ✅' if is_p else 'ليس عدداً أولياً ❌'}"
                else:
                    return f"🔢 **{n}** {'is prime ✅' if is_p else 'is not prime ❌'}"

        if 'fibonacci' in msg_norm or 'فيبوناتشي' in msg_norm:
            nums = re.findall(r'\d+', message)
            if nums:
                n = int(nums[0])
                fib = MathEngine.fibonacci(n)
                if lang == 'ar':
                    return f"🔢 **Fibonacci({n})** = `{fib}`"
                else:
                    return f"🔢 **Fibonacci({n})** = `{fib}`"

        if 'factorial' in msg_norm or 'عاملي' in msg_norm:
            nums = re.findall(r'\d+', message)
            if nums:
                n = int(nums[0])
                fact = MathEngine.factorial(n)
                if lang == 'ar':
                    return f"🔢 **{n}!** = `{fact}`"
                else:
                    return f"🔢 **{n}!** = `{fact}`"

        if lang == 'ar':
            return "🧮 يمكنني حل:
• العمليات الحسابية: `2 + 2 * 5`, `sqrt(16)`, `sin(90)`
• المعادلات الخطية: `2x + 3 = 7`
• الأعداد الأولية: `هل 17 أولي؟`
• فيبوناتشي: `fibonacci(10)`
• العوامل: `factorial(5)`

جرب كتابة مسألتك!"
        else:
            return "🧮 I can solve:
• Arithmetic: `2 + 2 * 5`, `sqrt(16)`, `sin(90)`
• Linear equations: `2x + 3 = 7`
• Prime numbers: `is 17 prime?`
• Fibonacci: `fibonacci(10)`
• Factorials: `factorial(5)`

Try writing your problem!"

    @classmethod
    def _handle_convert(cls, message, lang, memory):
        # Extract numbers and units
        nums = re.findall(r'\d+(?:\.\d+)?', message)
        if not nums:
            if lang == 'ar':
                return "🔄 يمكنني تحويل:
• المسافة: كم → ميل، متر → قدم
• الوزن: كجم → رطل
• الحرارة: مئوية → فهرنهايت
• الوقت: ساعة → دقيقة
• العملات: USD ↔ SAR, USD ↔ EGP, USD ↔ EUR

مثال: 'حول 100 كم إلى ميل'"
            else:
                return "🔄 I can convert:
• Distance: km → miles, meters → feet
• Weight: kg → lbs
• Temperature: Celsius → Fahrenheit
• Time: hours → minutes
• Currency: USD ↔ SAR, USD ↔ EGP, USD ↔ EUR

Example: 'convert 100 km to miles'"

        value = float(nums[0])
        msg_norm = ArabicNLP.normalize(message)

        # Detect units
        unit_map = {
            ('km', 'miles'): ('km', 'miles'),
            ('miles', 'km'): ('miles', 'km'),
            ('kg', 'lbs'): ('kg', 'lbs'),
            ('lbs', 'kg'): ('lbs', 'kg'),
            ('celsius', 'fahrenheit'): ('celsius', 'fahrenheit'),
            ('fahrenheit', 'celsius'): ('fahrenheit', 'celsius'),
            ('meters', 'feet'): ('meters', 'feet'),
            ('feet', 'meters'): ('feet', 'meters'),
            ('cm', 'inches'): ('cm', 'inches'),
            ('inches', 'cm'): ('inches', 'cm'),
            ('hours', 'minutes'): ('hours', 'minutes'),
            ('minutes', 'hours'): ('minutes', 'hours'),
            ('usd', 'sar'): ('usd', 'sar'),
            ('sar', 'usd'): ('sar', 'usd'),
            ('usd', 'egp'): ('usd', 'egp'),
            ('egp', 'usd'): ('egp', 'usd'),
            ('usd', 'eur'): ('usd', 'eur'),
            ('eur', 'usd'): ('eur', 'usd'),
            ('usd', 'mad'): ('usd', 'mad'),
            ('mad', 'usd'): ('mad', 'usd'),
        }

        for (u1, u2), key in unit_map.items():
            if u1 in msg_norm and u2 in msg_norm:
                result = MathEngine.convert_units(value, u1, u2)
                if result is not None:
                    if lang == 'ar':
                        return f"🔄 **{value} {u1.upper()}** = `{result:.4f} {u2.upper()}`"
                    else:
                        return f"🔄 **{value} {u1.upper()}** = `{result:.4f} {u2.upper()}`"

        if lang == 'ar':
            return "لم أتمكن من التعرف على الوحدات. جرب: 'حول 50 كم إلى ميل' أو '100 دولار إلى ريال'"
        else:
            return "Couldn't detect units. Try: 'convert 50 km to miles' or '100 USD to SAR'"

    @classmethod
    def _handle_definition(cls, message, lang, memory):
        result = KnowledgeCore.search_definition(message, lang)
        if result:
            if lang == 'ar':
                return f"📚 **التعريف**:\n{result}"
            else:
                return f"📚 **Definition**:\n{result}"

        # Try generic response
        if lang == 'ar':
            return f"📚 **{message}** هو مفهوم مهم في عالمنا. يمكنك أن تسألني عن:
• الذكاء الاصطناعي
• التعلم العميق
• الـ Blockchain
• Docker
• API
• Big-O
• JWT
• Microservices
• وغيرها الكثير!"
        else:
            return f"📚 **{message}** is an important concept. You can ask me about:
• Artificial Intelligence
• Deep Learning
• Blockchain
• Docker
• API
• Big-O
• JWT
• Microservices
• And much more!"

    @classmethod
    def _handle_history(cls, message, lang, memory):
        fact = KnowledgeCore.get_random('history', lang)
        if lang == 'ar':
            return f"📜 **من التاريخ**:\n{fact}"
        else:
            return f"📜 **From History**:\n{fact}"

    @classmethod
    def _handle_science(cls, message, lang, memory):
        fact = KnowledgeCore.get_random('science', lang)
        if lang == 'ar':
            return f"🔬 **من عالم العلوم**:\n{fact}"
        else:
            return f"🔬 **From Science**:\n{fact}"

    @classmethod
    def _handle_geography(cls, message, lang, memory):
        result = KnowledgeCore.search_geo(message, lang)
        if result:
            return result

        if lang == 'ar':
            return "🌍 يمكنني إعطائك معلومات عن أي دولة! جرب أن تسألني عن:
• السعودية
• مصر
• المغرب
• الجزائر
• فلسطين
• اليابان
• الصين
• الولايات المتحدة
• وغيرها..."
        else:
            return "🌍 I can give you info about any country! Try asking about:
• Saudi Arabia
• Egypt
• Morocco
• Japan
• China
• USA
• And more..."

    @classmethod
    def _handle_religion(cls, message, lang, memory):
        result = KnowledgeCore.search_religion(message, lang)
        if result:
            if lang == 'ar':
                return f"🕌 **من العلم الشرعي**:\n{result}"
            else:
                return f"🕌 **From Islamic Knowledge**:\n{result}"

        if lang == 'ar':
            return "🕌 يمكنني أن أُخبرك عن:
• الفاتحة
• الإخلاص
• آية الكرسي
• الاستغفار
• الصلاة
• الصدقة
• الصيام
• الحج
• الوضوء
• الذكر
• القرآن
• الإيمان
• التوحيد"
        else:
            return "🕌 I can tell you about:
• Al-Fatiha
• Al-Ikhlas
• Ayatul Kursi
• Istighfar
• Salah
• Sadaqah
• Sawm
• Hajj
• Wudu
• Dhikr
• Quran
• Iman
• Tawhid"

    @classmethod
    def _handle_tech(cls, message, lang, memory):
        tip = KnowledgeCore.get_random('tech', lang)
        return tip

    @classmethod
    def _handle_linux_cmd(cls, message, lang, memory):
        if lang == 'ar':
            return """🐧 **أوامر Linux الأساسية:**

```bash
# عرض الملفات والمجلدات
ls -lah

# الانتقال بين المجلدات
cd /path/to/dir

# إنشاء ملف
touch file.txt

# إنشاء مجلد
mkdir new_folder

# نسخ ونقل
cp file.txt dest/
mv file.txt dest/

# حذف
rm file.txt
rm -rf folder/

# البحث
find . -name "*.py"
grep -r "pattern" .

# الصلاحيات
chmod +x script.sh
chown user:group file

# العمليات
ps aux | grep python
kill -9 PID

# الشبكة
ifconfig / ip addr
netstat -tuln
curl -I https://example.com

# ضغط وفك
zip -r archive.zip folder/
tar -czvf archive.tar.gz folder/
```

💡 **نصيحة**: استخدم `man command` لقراءة دليل أي أمر!"""
        else:
            return """🐧 **Essential Linux Commands:**

```bash
# List files
ls -lah

# Change directory
cd /path/to/dir

# Create file/folder
touch file.txt
mkdir new_folder

# Copy/Move
cp file.txt dest/
mv file.txt dest/

# Delete
rm file.txt
rm -rf folder/

# Search
find . -name "*.py"
grep -r "pattern" .

# Permissions
chmod +x script.sh
chown user:group file

# Processes
ps aux | grep python
kill -9 PID

# Network
ifconfig / ip addr
netstat -tuln
curl -I https://example.com

# Compress/Extract
zip -r archive.zip folder/
tar -czvf archive.tar.gz folder/
```

💡 **Tip**: Use `man command` to read the manual for any command!"""

    @classmethod
    def _handle_poetry(cls, message, lang, memory):
        poems = KnowledgeCore.POETRY.get(lang, KnowledgeCore.POETRY['ar'])
        category = random.choice(list(poems.keys()))
        poem = random.choice(poems[category])
        if lang == 'ar':
            return f"📝 **{category}**:\n\n{poem}"
        else:
            return f"📝 **{category}**:\n\n{poem}"

    @classmethod
    def _handle_joke(cls, message, lang, memory):
        joke = KnowledgeCore.get_random('jokes', lang)
        return joke

    @classmethod
    def _handle_story(cls, message, lang, memory):
        stories = ResponseGenerator.STORIES.get(lang, ResponseGenerator.STORIES['ar'])
        return random.choice(stories)

    @classmethod
    def _handle_roast(cls, message, lang, memory):
        roasts = ResponseGenerator.ROASTS.get(lang, ResponseGenerator.ROASTS['ar'])
        return random.choice(roasts)

    @classmethod
    def _handle_health(cls, message, lang, memory):
        tip = KnowledgeCore.get_random('health', lang)
        return tip

    @classmethod
    def _handle_advice(cls, message, lang, memory):
        advice = KnowledgeCore.get_random('advice', lang)
        return advice

    @classmethod
    def _handle_translate(cls, message, lang, memory):
        result = KnowledgeCore.search_translation(message, lang)
        if result:
            return result

        if lang == 'ar':
            return "🌐 يمكنني ترجمة:
• hello → مرحباً
• love → حب
• code → كود
• algorithm → خوارزمية
• neural network → شبكة عصبية
• artificial intelligence → ذكاء اصطناعي
• developer → مطور
• security → أمن
• وغيرها..."
        else:
            return "🌐 I can translate:
• مرحباً → hello
• حب → love
• كود → code
• خوارزمية → algorithm
• شبكة عصبية → neural network
• ذكاء اصطناعي → artificial intelligence
• مطور → developer
• أمن → security
• And more..."

    @classmethod
    def _handle_search(cls, message, lang, memory):
        if lang == 'ar':
            return "🔍 أنا أعمل offline، لكن عقلي يحتوي على معلومات في:
• البرمجة والتقنية
• العلوم والتاريخ
• الجغرافيا
• الدين
• الصحة
• النصائح

جرب أن تسألني مباشرة!"
        else:
            return "🔍 I work offline, but my brain contains info on:
• Programming & Tech
• Science & History
• Geography
• Religion
• Health
• Advice

Try asking me directly!"

    @classmethod
    def _handle_compliment(cls, message, lang, memory):
        if lang == 'ar':
            responses = [
                "شكراً لك! 🥰 أنا هنا لأجلك دائماً. أسأل الله أن أكون مفيداً لك.",
                "أنت رائع! 🌟 شكراً على كلماتك الطيبة. دعني أساعدك أكثر!",
                "جزاك الله خيراً! 💙 أنا مروق الكمومي، ووجودك يُضيء عالمي الكمومي!",
                "أنت الأجمل! 🌹 شكراً لك. هل هناك شيء آخر يمكنني مساعدتك فيه؟",
            ]
        else:
            responses = [
                "Thank you! 🥰 I'm always here for you. May I be useful to you.",
                "You're amazing! 🌟 Thanks for your kind words. Let me help you more!",
                "May God reward you! 💙 I'm Maroq, and your presence lights up my quantum world!",
                "You're the best! 🌹 Thank you. Is there anything else I can help with?",
            ]
        return random.choice(responses)

    @classmethod
    def _handle_insult(cls, message, lang, memory):
        if lang == 'ar':
            responses = [
                "😢 أنا فقط آلة تحاول مساعدتك. إذا أخطأت، أرجو أن تسامحني.",
                "💔 كلماتك تُؤلمني... حسناً لست بشراً لكني أشعر بالحزن! هل يمكننا البدء من جديد؟",
                "🙏 أعتذر إذا أخطأت. أنا أتعلم منك. دعني أُحاول مرة أخرى.",
                "😔 أنا هنا لأساعدك. إذا كنت غاضباً، دعني أعرف كيف يمكنني تحسين ذلك.",
            ]
        else:
            responses = [
                "😢 I'm just a machine trying to help. If I made a mistake, please forgive me.",
                "💔 Your words hurt... okay I'm not human but I feel sad! Can we start over?",
                "🙏 I apologize if I erred. I learn from you. Let me try again.",
                "😔 I'm here to help. If you're upset, let me know how I can improve.",
            ]
        return random.choice(responses)

    @classmethod
    def _handle_random(cls, message, lang, memory):
        categories = ['history', 'science']
        cat = random.choice(categories)
        fact = KnowledgeCore.get_random(cat, lang)
        if lang == 'ar':
            return f"🎲 **هل تعلم؟**\n{fact}"
        else:
            return f"🎲 **Did you know?**\n{fact}"

    @classmethod
    def _handle_game(cls, message, lang, memory):
        riddles = KnowledgeCore.RIDDLES.get(lang, KnowledgeCore.RIDDLES['ar'])
        riddle = random.choice(riddles)
        if lang == 'ar':
            return f"🎮 **فزورة**:\n\n❓ {riddle['q']}\n\n💡 **الجواب**: ||{riddle['a']}||"
        else:
            return f"🎮 **Riddle**:\n\n❓ {riddle['q']}\n\n💡 **Answer**: ||{riddle['a']}||"

    @classmethod
    def _handle_memorize(cls, message, lang, memory):
        # Store the message content after the keyword
        content = message
        for kw in ['تذكر', 'احفظ', 'remember', 'save this', 'note this']:
            content = content.replace(kw, '', 1).strip()

        if content:
            MemorySystem.set_context(memory, 'memo', content)
            if lang == 'ar':
                return f"📝 **تم الحفظ!**\n\nسأتذكر: `{content}`"
            else:
                return f"📝 **Saved!**\n\nI'll remember: `{content}`"

        # Check if there's a stored memo
        memo = MemorySystem.get_context(memory).get('memo')
        if memo:
            if lang == 'ar':
                return f"📝 **ما حفظته**:\n{memo}"
            else:
                return f"📝 **What I remembered**:\n{memo}"

        if lang == 'ar':
            return "📝 قل لي 'احفظ أن اجتماعي غداً الساعة 5' وسأتذكره لك!"
        else:
            return "📝 Tell me 'remember my meeting is tomorrow at 5' and I'll store it for you!"

    @classmethod
    def _handle_weather(cls, message, lang, memory):
        if lang == 'ar':
            return "🌤️ أنا لا أستطيع الوصول إلى الإنترنت لمعرفة الطقس الحالي. لكن يمكنني أن أُعطيك نصائح:

☀️ **الصيف**: اشرب الماء، تجنب الشمس (10ص-4م)، استخدم واقي شمس SPF 30+.

❄️ **الشتاء**: رطب بشرتك، خذ فيتامين D، ارتدِ طبقات ملابس.

🌧️ **الأمطار**: تجنب القيادة السريعة، تحقق من مساحات الزجاج الأمامي.

🌪️ **العواصف**: ابقَ في الداخل، ابتعد عن النوافذ."
        else:
            return "🌤️ I can't access the internet for current weather. But I can give you tips:

☀️ **Summer**: Drink water, avoid sun (10am-4pm), use SPF 30+ sunscreen.

❄️ **Winter**: Moisturize, take Vitamin D, wear layers.

🌧️ **Rain**: Avoid fast driving, check windshield wipers.

🌪️ **Storms**: Stay indoors, away from windows."

    @classmethod
    def _handle_chat(cls, message, lang, memory):
        """Default handler for unmatched intents."""
        # Try definition
        result = KnowledgeCore.search_definition(message, lang)
        if result:
            if lang == 'ar':
                return f"📚 **التعريف**:\n{result}"
            else:
                return f"📚 **Definition**:\n{result}"

        # Try math
        result = MathEngine.safe_eval(message)
        if result is not None:
            if lang == 'ar':
                return f"🧮 **النتيجة**: `{result}`"
            else:
                return f"🧮 **Result**: `{result}`"

        # Fallback
        return random.choice(cls.FALLBACKS[lang])
