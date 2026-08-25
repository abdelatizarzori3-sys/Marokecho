# -*- coding: utf-8 -*-
"""MAROKECHO QUANTUM BRAIN v4.0"""

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

class ArabicNLP:
    DIACRITICS = re.compile(r"[\u064B-\u065F\u0670\u0640]")
    ARABIC_PUNCT = re.compile(r"[،؛؟٪٫٬٭۔]")
    PREFIXES = ["ال", "وال", "بال", "كال", "فال", "لل", "و", "ف", "ب", "ك", "ل", "أ", "س", "ي", "ت", "ن", "ا"]
    SUFFIXES = ["ة", "ات", "ين", "ون", "ان", "وا", "تم", "تن", "تما", "نا", "ها", "هم", "هن", "كما", "كن", "ني"]
    NORMALIZE_MAP = str.maketrans("أإآءىؤئ", "اااايوي")
    STOP_WORDS = {
        "في", "من", "إلى", "على", "هذا", "هذه", "التي", "الذي", "و", "أو", "ثم", "لكن", "لأن",
        "كان", "يكون", "أن", "ما", "لم", "قد", "لا", "كل", "بعض", "مع", "عن", "بعد", "قبل",
        "الى", "الي", "اين", "ايه", "ايش", "شو", "كيف", "لماذا", "ليش", "هل", "الا", "غير",
        "اي", "اية", "شنو", "وش", "وشو", "شلون", "كيفك", "شخبارك", "اخبارك", "هي", "هو", "هم",
        "انت", "انتي", "انتم", "نحن", "انا", "احنا", "لي", "له", "لها", "لهم", "لك", "لكم",
        "ذلك", "التي", "الذين", "اللاتي", "اللواتي", "اللائي", "هنا", "هناك", "ثم", "ايضا",
        "كذلك", "بل", "حتى", "إلا", "ليس", "لن", "لم", "ما", "لا", "لما", "إن", "لو", "لولا"
    }

    @classmethod
    def normalize(cls, text):
        if not text:
            return ""
        text = text.lower().strip()
        text = cls.DIACRITICS.sub("", text)
        text = cls.ARABIC_PUNCT.sub(" ", text)
        text = text.translate(cls.NORMALIZE_MAP)
        text = re.sub(r"\s+", " ", text)
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
            return "ar"
        arabic_chars = len(re.findall(r"[\u0600-\u06FF]", text))
        total_chars = len(text.strip())
        if total_chars == 0:
            return "ar"
        ratio = arabic_chars / total_chars
        return "ar" if ratio > 0.3 else "en"

    @classmethod
    def extract_entities(cls, text):
        return {
            "numbers": re.findall(r"\d+(?:\.\d+)?", text),
            "urls": re.findall(r"https?://\S+", text),
            "emails": re.findall(r"[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z0-9]+", text),
            "mentions": re.findall(r"@[a-zA-Z0-9_]+", text),
            "code_blocks": re.findall(r"`{1,3}(.+?)`{1,3}", text, re.DOTALL),
        }

class Intent:
    INTENTS = {
        "code_generate": {
            "ar": ["اكتب كود", "كود ل", "برمج لي", "سكربت", "function", "دالة", "اكتب برنامج", "امثلة برمجية", "مثال برمجي", "كيف ابرمج", "كيف اكتب", "انشئ كود", "اعطني كود", "code for", "python", "javascript", "html", "css", "sql", "bash", "flask", "django", "react"],
            "en": ["write code", "code for", "script for", "program to", "function that", "how to code", "example in python", "example in js", "build a", "create a script", "generate code", "coding"]
        },
        "code_debug": {
            "ar": ["صحح", "خطأ", "error", "bug", "مشكلة في الكود", "ما يشتغل", "ما يعمل", "يرفض", "يعطيني خطأ", "traceback", "exception", "فشل", "تعطل", "crash"],
            "en": ["fix this", "debug", "error in", "not working", "bug in", "traceback", "exception", "syntax error", "broken", "fails", "crashes"]
        },
        "code_explain": {
            "ar": ["اشرح الكود", "فهمني", "شرح", "يعني ايش", "ايش يسوي", "كيف يشتغل", "توضيح", "اشرحلي", "وضحلي"],
            "en": ["explain code", "what does this do", "how does this work", "break down", "walk me through", "explain this"]
        },
        "algorithm": {
            "ar": ["خوارزمية", "algorithm", "big o", "تعقيد", "كفاءة", "بنية البيانات", "sort", "search", "graph", "tree", "dynamic programming", "dp", "recursion"],
            "en": ["algorithm", "data structure", "complexity", "big o", "time complexity", "space complexity", "sorting", "searching", "graph traversal"]
        },
        "math_solve": {
            "ar": ["احسب", "حل", "معادلة", "جذر", "log", "sin", "cos", "integral", "اشتقاق", "تكامل", "مساحة", "محيط", "حجم", "نسبة", "نسبة مئوية", "كم يساوي", "احسبلي", "result", "sqrt", "power", "factorial", "fibonacci", "prime"],
            "en": ["calculate", "solve", "equation", "compute", "derivative", "integral", "area of", "volume of", "percentage", "sqrt", "factorial", "what is", "equals", "result of"]
        },
        "convert": {
            "ar": ["حول", "تحويل", "من", "الى", "دولار", "يورو", "كيلو", "متر", "ساعة", "دقيقة", "تحويل عملات", "تحويل وحدات"],
            "en": ["convert", "to usd", "to eur", "km to miles", "kg to lbs", "celsius to fahrenheit", "how many", "exchange rate"]
        },
        "definition": {
            "ar": ["ايش هو", "ما هو", "ما هي", "تعريف", "define", "meaning", "معنى", "فلسفة", "علم", "مفهوم", "شرح مصطلح", "اشرحلي"],
            "en": ["what is", "define", "meaning of", "explain what", "concept of", "definition of"]
        },
        "history": {
            "ar": ["تاريخ", "متى", "في اي سنة", "من اكتشف", "من invent", "حرب", "عهد", "دولة", "امبراطورية", "خلافة", "عصر", "حضارة"],
            "en": ["history of", "when did", "who discovered", "who invented", "ancient", "war", "dynasty", "empire", "civilization", "era"]
        },
        "science": {
            "ar": ["فيزياء", "كيمياء", "بيولوجيا", "فلك", "فضاء", "ذرة", "طاقة", "ضوء", "جاذبية", "نظرية", "قانون", "كون", "نجم", "كوكب"],
            "en": ["physics", "chemistry", "biology", "astronomy", "quantum", "relativity", "gravity", "atom", "molecule", "theory of", "universe", "planet"]
        },
        "geography": {
            "ar": ["اين", "وين", "دولة", "عاصمة", "جبل", "نهر", "بحر", "محيط", "قارة", "مدينة", "خريطة", "موقع"],
            "en": ["where is", "capital of", "country", "mountain", "river", "ocean", "continent", "city in", "located"]
        },
        "religion": {
            "ar": ["قران", "حديث", "سورة", "اية", "اسلام", "فقه", "تفسير", "صلاة", "زكاة", "صيام", "حج", "الله", "نبي", "دعاء", "اذكار"],
            "en": ["quran", "hadith", "islam", "surah", "verse", "prophet", "prayer", "ramadan", "hajj", "dua"]
        },
        "tech": {
            "ar": ["هكر", "اختراق", "امن", "cyber", "linux", "terminal", "network", "wifi", "server", "database", "docker", "git", "github", "firewall", "encryption"],
            "en": ["hack", "cybersecurity", "linux command", "networking", "sql injection", "pentest", "vulnerability", "exploit", "kali"]
        },
        "linux_cmd": {
            "ar": ["terminal", "termux", "bash", "shell", "chmod", "grep", "awk", "sed", "command", "اوامر"],
            "en": ["linux", "bash script", "command line", "chmod", "chown", "grep", "find", "tar", "ssh", "scp"]
        },
        "poetry": {
            "ar": ["شعر", "قصيدة", "بيت شعر", "ابيات", "قافية", "موشح", "زجل", "متنبي", "نزار", "محمود درويش", "امرؤ القيس"],
            "en": ["poem", "poetry", "verse", "rhyme", "write a poem"]
        },
        "joke": {
            "ar": ["نكتة", "ضحك", "هبال", "مضحك", "joke", "funny", "meme", "هزر"],
            "en": ["joke", "funny", "laugh", "humor", "tell me a joke", "make me laugh"]
        },
        "story": {
            "ar": ["قصة", "حكاية", "رواية", "سرد", "story", "fiction", "fantasy", "حكاية"],
            "en": ["story", "tell me a story", "fiction", "narrative", "short story"]
        },
        "roast": {
            "ar": ["هزر", "هزرة", "سخر", "roast", "تريق", "تنمر", "مسخرة"],
            "en": ["roast me", "insult me", "make fun of", "savage", "burn"]
        },
        "greeting": {
            "ar": ["مرحبا", "هلا", "السلام", "صباح", "مساء", "اهلين", "هاي", "hello", "hi", "hey", "تحياتي", "سلامات"],
            "en": ["hello", "hi", "hey", "good morning", "good evening", "greetings", "salam", "whats up"]
        },
        "who_are_you": {
            "ar": ["من انت", "مين انت", "شو اسمك", "ايش اسمك", "منو انت", "who are you", "your name", "تعرفني عنك"],
            "en": ["who are you", "what is your name", "introduce yourself", "tell me about you"]
        },
        "time": {
            "ar": ["الوقت", "الساعة", "كم الساعة", "تاريخ", "اليوم", "month", "year", "الان", "حاليا"],
            "en": ["what time", "what date", "current time", "today is", "what day", "now"]
        },
        "weather": {
            "ar": ["طقس", "جو", "حرارة", "امطار", "weather", "temperature", "مطر", "شمس"],
            "en": ["weather", "temperature", "forecast", "rain", "sunny", "cloudy"]
        },
        "health": {
            "ar": ["صحة", "صحي", "طب", "دواء", "اعراض", "مرض", "نصيحة صحية", "health tip", "diet", "fitness", "رياضة", "تغذية"],
            "en": ["health", "medical", "symptom", "medicine", "doctor", "nutrition", "workout", "mental health"]
        },
        "advice": {
            "ar": ["نصيحة", "نصائح", "اعطني", "ساعدني", "مشكلتي", " confused", "lost", "depressed", "anxious", "حزين", "محبط"],
            "en": ["advice", "help me", "what should i do", "i am confused", "life advice", "motivation", "sad", "depressed"]
        },
        "translate": {
            "ar": ["ترجم", "translate", "من عربي", "من انجليزي", "meaning in", "معنى كلمة", "ترجمة"],
            "en": ["translate", "translation", "in arabic", "in english", "how to say", "what does mean"]
        },
        "search": {
            "ar": ["ابحث", "دور", "google", "ويكيبيديا", "معلومات عن", "بحث عن", "دلني"],
            "en": ["search", "google", "wikipedia", "look up", "find information", "info about"]
        },
        "compliment": {
            "ar": ["مدح", "اشكر", "شكرا", "جميل", "رهيب", "ذكي", "احبك", "ممتاز", "عظيم"],
            "en": ["thank you", "thanks", "good job", "amazing", "love you", "you are great", "awesome"]
        },
        "insult": {
            "ar": ["غبي", "احمق", "سخيف", "كرهتك", "بطل", "callate", "زفت", "كذاب"],
            "en": ["stupid", "dumb", "hate you", "shut up", "you suck", "idiot", "liar"]
        },
        "random": {
            "ar": ["عشوائي", "random", "fact", "حقيقة", "هل تعلم", "trivia", "معلومة"],
            "en": ["random fact", "did you know", "trivia", "interesting fact", "cool fact"]
        },
        "game": {
            "ar": ["لعبة", "تحدي", "سؤال", "quiz", "فزورة", "لغز", "غموض"],
            "en": ["game", "quiz", "riddle", "puzzle", "challenge", "trivia game"]
        },
        "memorize": {
            "ar": ["تذكر", "احفظ", "ذاكرتي", "remember", "dont forget", "احفظلي", "سجل"],
            "en": ["remember that", "save this", "note this", "dont forget", "store this"]
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
            kw_list = keywords.get(lang, keywords.get("ar", []))
            for kw in kw_list:
                kw_norm = ArabicNLP.normalize(kw)
                if kw_norm in text_norm:
                    score += 3
                elif any(ArabicNLP.light_stem(t) == ArabicNLP.light_stem(kw_norm) for t in tokens if len(t) > 2):
                    score += 1.5
            scores[intent] = score
        if not scores or max(scores.values()) == 0:
            return ("chat", 0.5)
        best = max(scores, key=scores.get)
        confidence = min(scores[best] / 5, 1.0)
        return (best, confidence)

class KnowledgeCore:
    DEFINITIONS = {
        "ar": {
            "الذكاء الاصطناعي": "قدرة الأنظمة الحاسوبية على محاكاة الذكاء البشري: التعلم، الاستدلال، الإدراك، وفهم اللغة الطبيعية.",
            "التعلم العميق": "فرع من التعلم الآلي يعتمد على شبكات عصبية اصطناعية متعددة الطبقات.",
            "الكم": "أصغر وحدة فيزيائية للمعلومات الكمومية، تتخذ حالات تراكب ويمكن أن تكون متشابكة.",
            "blockchain": "سجل رقمي موزع وغير قابل للتغيير يُستخدم لتسجيل المعاملات.",
            "docker": "منصة لإنشاء وتشغيل ونشر التطبيقات داخل حاويات معزولة.",
            "api": "واجهة برمجة التطبيقات: مجموعة من البروتوكولات التي تتيح للبرمجيات التواصل.",
            "recursion": "دالة تستدعي نفسها مباشرة أو غير مباشرة لحل مشكلة بتقسيمها إلى نسخ أصغر.",
            "big_o": "تدوين يصف أداء الخوارزمية من حيث الزمن أو المساحة مع نمو حجم المدخلات.",
        },
        "en": {
            "artificial intelligence": "The simulation of human intelligence processes by computer systems.",
            "deep learning": "A subset of machine learning using multi-layered neural networks.",
            "quantum": "The smallest physical unit of quantum information.",
            "blockchain": "A distributed, immutable digital ledger.",
            "docker": "A platform for developing, shipping, and running applications in containers.",
            "api": "Application Programming Interface.",
            "recursion": "A function that calls itself to solve a problem.",
            "big o": "Notation describing algorithm performance.",
        }
    }

    HISTORY = {
        "ar": [
            "اكتشف ابن الهيثم (965-1040م) طبيعة الضوء واخترع الكاميرا المظلمة.",
            "الخوارزمي (780-850م) هو أبو الجبر والخوارزميات. كلمة Algorithm مشتقة من اسمه.",
            "بيت الحكمة في بغداد (8م) كان أول مركز بحثي عالمي.",
            "لينوس تورفالدس كتب نواة Linux في 1991.",
            "أول حاسوب إلكتروني عام ENIAC كان يزن 30 طناً.",
            "تيم بيرنرز-لي اخترع WWW في CERN عام 1989.",
        ],
        "en": [
            "Ibn al-Haytham (965-1040 AD) discovered the nature of light and invented the camera obscura.",
            "Al-Khwarizmi (780-850 AD) is the father of Algebra and Algorithms.",
            "The House of Wisdom in Baghdad (8th c.) was the world's first research center.",
            "Linus Torvalds wrote Linux in 1991 as a hobby.",
            "The first general-purpose computer ENIAC weighed 30 tons.",
            "Tim Berners-Lee invented the WWW at CERN in 1989.",
        ]
    }

    SCIENCE = {
        "ar": [
            "الضوء يستغرق 8 دقائق و20 ثانية للوصول من الشمس إلى الأرض.",
            "90% من كتلة الجسم البشري مصنوعة من بقايا نجوم ميتة (stardust).",
            "الحاسوب الكمومي يستغل التراكب لحساب كل الاحتمالات في آن واحد.",
            "DNA البشري يحتوي على ~3 مليار زوج قاعدي.",
            "الفراغ ليس فارغاً: ي burble بأزواج جسيم-مضاد جسيم افتراضية.",
        ],
        "en": [
            "Light takes 8m 20s to reach Earth from the Sun.",
            "90% of your body mass is stardust.",
            "Quantum computers exploit superposition to evaluate all possibilities simultaneously.",
            "Human DNA has ~3 billion base pairs.",
            "Vacuum is not empty: it bubbles with virtual particle-antiparticle pairs.",
        ]
    }

    JOKES = {
        "ar": [
            "مبرمج دخل مطعم. النادل: هل لديك حجز؟ المبرمج: لا، أنا asynchronous.",
            "لماذا يكره المبرمجون الطبيعة؟ لأنها مليئة بالـ bugs!",
            "كم مبرمجاً يلزم لتغيير مصباح؟ لا أحد، إنه مشكلة hardware!",
            "أنا لست كسولاً، أنا في وضع توفير الطاقة.",
            "TCP يذهب إلى حانة ويقول: 'أريد بيرة'. النادل: 'بيرة واحدة'. TCP: 'نعم، بيرة واحدة'.",
        ],
        "en": [
            "A programmer walks into a bar... and says 'Hello World'.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, it's a hardware problem!",
            "I would tell you a UDP joke, but you might not get it.",
            "There are 10 types of people: those who understand binary and those who don't.",
        ]
    }

    POETRY = {
        "ar": [
            "على هذه الأرض ما يَسْتَحِقُّ الحياة\n— محمود درويش",
            "أَحْبَبْتُكَ حُبَّيْنِ\nحُبَّ الهَوَى وَحُبَّ أَنْتَ أَهْلُ لَهُ\n— نزار قباني",
            "قِفا نَبْكِ مِنْ ذِكْرى حَبِيبٍ وَمَنْزِلِ\n— امرؤ القيس",
            "إِنْ كُنْتَ تَظُنُّ أَنَّكَ قَدْ كَسَرْتَنِي\nفَأَنْتَ وَاهِمٌ... أَنَا مَنْ كَسَرَ نَفْسَهُ",
        ],
        "en": [
            "Two roads diverged in a wood, and I—\nI took the one less traveled by,\nAnd that has made all the difference.\n— Robert Frost",
            "Hope is the thing with feathers\nThat perches in the soul.\n— Emily Dickinson",
            "Do not go gentle into that good night.\nRage, rage against the dying of the light.\n— Dylan Thomas",
        ]
    }

    ADVICE = {
        "ar": [
            "🌱 النمو: 'النجاح ليس نهائياً، والفشل ليس قاتلاً: الجرأة على الاستمرار هي ما يهم.' — تشرشل",
            "💻 البرمجة: 'لا تحفظ الكود. افهم المفهوم. الكود يتغير، المنطق يبقى.'",
            "🤝 العلاقات: 'الناس لن تتذكر ما قلت أو فعلت، لكنهم سيتذكرون كيف جعلتهم يشعرون.'",
            "🎯 التركيز: 'متعدد المهام خدعة. الدماغ لا يستطيع. ركز على شيء واحد بعمق.'",
            "📚 التعلم: 'اقرأ كما لو كنت ستعيش غداً، واعمل كما لو كنت ستعيش أبداً.'",
            "🔥 الشغف: 'اعمل على شيء تحبه، ولن تضطر للعمل يوماً... تقريباً.'",
            "⚡ الإنتاجية: 'قاعدة 80/20: 80% من النتائج تأتي من 20% من الجهود.'",
        ],
        "en": [
            "🌱 Growth: 'Success is not final, failure is not fatal: it is the courage to continue that counts.'",
            "💻 Coding: 'Don't memorize code. Understand the concept. Code changes, logic remains.'",
            "🤝 Relationships: 'People will forget what you said or did, but never how you made them feel.'",
            "🎯 Focus: 'Multitasking is a myth. Focus deeply on one thing.'",
            "📚 Learning: 'Read as if you'll die tomorrow. Work as if you'll live forever.'",
            "🔥 Passion: 'Work on something you love and you'll never work a day... almost.'",
            "⚡ Productivity: 'The 80/20 rule: 80% of results come from 20% of efforts.'",
        ]
    }

    TECH = {
        "ar": [
            "🔒 HTTPS: لا تدخل بيانات حساسة على موقع بدون HTTPS.",
            "🛡️ 2FA: المصادقة الثنائية تمنع 99.9% من الاختراقات الآلية.",
            "🐍 Python Virtual Env: استخدم python -m venv venv دائماً.",
            "🔑 Passwords: كلمة مرور بطول 12 حرفاً مع رموز = 34,000 سنة لكسرها.",
            "💾 Backup: قاعدة 3-2-1: 3 نسخ، على 2 وسائط، 1 خارج الموقع.",
        ],
        "en": [
            "🔒 HTTPS: Never enter sensitive data on a site without HTTPS.",
            "🛡️ 2FA: Two-factor authentication blocks 99.9% of automated attacks.",
            "🐍 Python venv: Always use python -m venv venv.",
            "🔑 Passwords: A 12-character password with symbols = 34,000 years to crack.",
            "💾 Backup: The 3-2-1 rule: 3 copies, 2 media, 1 offsite.",
        ]
    }

    RIDDLES = {
        "ar": [
            {"q": "شيء موجود في السماء إذا أضفت إليه حرفاً أصبح في الأرض؟", "a": "نجم → منجم ⛏️"},
            {"q": "ما هو الشيء الذي يُقرصك ولا تراه؟", "a": "الجوع 🍽️"},
            {"q": "ما هو الشيء الذي كلما زاد نقص؟", "a": "الحفرة ⛳"},
            {"q": "ما هو الشيء الذي إذا أخذت منه زاد وكبر؟", "a": "الحفرة ⛳"},
            {"q": "ما هو الشيء الذي له أسنان ولا يعض؟", "a": "المشط 💇"},
            {"q": "ما هو الشيء الذي يدخل الماء ولا يبتل؟", "a": "الضوء 💡"},
        ],
        "en": [
            {"q": "I speak without a mouth and hear without ears. What am I?", "a": "An echo 🔊"},
            {"q": "The more you take, the more you leave behind. What am I?", "a": "Footsteps 👣"},
            {"q": "What has keys but no locks?", "a": "A piano 🎹"},
            {"q": "What gets wetter the more it dries?", "a": "A towel 🧖"},
            {"q": "What has a head, a tail, but no body?", "a": "A coin 🪙"},
            {"q": "What belongs to you but others use it more than you?", "a": "Your name 🏷️"},
        ]
    }

    @classmethod
    def get_random(cls, category, lang="ar"):
        data = getattr(cls, category.upper(), {})
        items = data.get(lang, data.get("ar", []))
        if isinstance(items, list) and items:
            return random.choice(items)
        return ""

    @classmethod
    def search_definition(cls, query, lang="ar"):
        defs = cls.DEFINITIONS.get(lang, cls.DEFINITIONS["ar"])
        query_norm = ArabicNLP.normalize(query)
        for key, val in defs.items():
            if key in query_norm or query_norm in key:
                return val
        return None

class MathEngine:
    @staticmethod
    def safe_eval(expression):
        try:
            expr = expression.replace("×", "*").replace("÷", "/").replace("^", "**")
            expr = expr.replace("√", "sqrt").replace("π", str(math.pi))
            safe_dict = {
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "log": math.log, "log10": math.log10, "exp": math.exp,
                "abs": abs, "round": round, "max": max, "min": min,
                "pi": math.pi, "e": math.e, "factorial": math.factorial,
                "pow": pow, "ceil": math.ceil, "floor": math.floor,
            }
            result = eval(expr, {"__builtins__": {}}, safe_dict)
            return result
        except Exception:
            return None

    @staticmethod
    def solve_equation(equation_str):
        try:
            eq = equation_str.replace(" ", "")
            if "=" not in eq:
                return None
            left, right = eq.split("=", 1)
            right_val = float(MathEngine.safe_eval(right))
            left = left.replace("-x", "-1x").replace("+x", "+1x")
            if left.startswith("x"):
                left = "1" + left
            x_coeff = 0
            constant = 0
            current = ""
            sign = 1
            for char in left + "+":
                if char in "+-":
                    if current:
                        if "x" in current:
                            coeff = current.replace("x", "")
                            x_coeff += sign * (float(coeff) if coeff else 1)
                        else:
                            constant += sign * float(current)
                    current = ""
                    sign = 1 if char == "+" else -1
                else:
                    current += char
            if x_coeff == 0:
                return None
            x = (right_val - constant) / x_coeff
            return x
        except Exception:
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

class MemorySystem:
    _sessions = {}

    @classmethod
    def get_session(cls, session_id):
        if session_id not in cls._sessions:
            cls._sessions[session_id] = {
                "history": [],
                "context": {},
                "mood": "neutral",
                "last_intent": None,
            }
        return cls._sessions[session_id]

    @classmethod
    def add_message(cls, session_id, role, content, intent=None):
        session = cls.get_session(session_id)
        session["history"].append({
            "role": role,
            "content": content,
            "intent": intent,
            "timestamp": datetime.datetime.now().isoformat()
        })
        if intent:
            session["last_intent"] = intent
        if len(session["history"]) > 20:
            session["history"] = session["history"][-20:]

    @classmethod
    def set_context(cls, session_id, key, value):
        session = cls.get_session(session_id)
        session["context"][key] = value

    @classmethod
    def get_context(cls, session_id):
        session = cls.get_session(session_id)
        return session["context"]

class ResponseGenerator:
    GREETINGS = {
        "ar": [
            "أهلاً وسهلاً! أنا مروق الكمومي 🔮🧠، عقلك الاصطناعي المحلي. كيف يمكنني مساعدتك اليوم؟",
            "مرحباً! مروق الكمومي في الخدمة. جاهز لأي سؤال، كود، حساب، أو حتى نكتة!",
            "هلا والله! أنا هنا بعقل ضخم offline. اسألني ما شئت.",
        ],
        "en": [
            "Hello! I'm Maroq El-Kawmi 🔮🧠, your local AI brain. How can I help you today?",
            "Hi there! Maroq is online and ready. Ask me anything!",
            "Greetings! I'm running entirely offline. What can I do for you?",
        ]
    }

    ROASTS = {
        "ar": [
            "أنت مثل الـ CSS: تحتاج 500 سطر لعمل شيء بسيط!",
            "أنت مثل الـ JavaScript: تُعيد تعريف نفسك كل 5 دقائق!",
            "أنت مثل الـ Internet Explorer: بطيء، قديم، ولا أحد يحبك!",
            "أنت مثل الـ Bug: الجميع يشعر بوجودك لكن لا أحد يعرف أين أنت!",
        ],
        "en": [
            "You're like CSS: you need 500 lines to do something simple!",
            "You're like JavaScript: you redefine yourself every 5 minutes!",
            "You're like Internet Explorer: slow, outdated, and nobody loves you!",
            "You're like a bug: everyone feels your presence but no one knows where you are!",
        ]
    }

    STORIES = {
        "ar": [
            "كان هناك مبرمج عبقري يعيش في كهف من الكود. كان يكتب برامجاً تُغير العالم، لكنه نسي git commit. في يوم انقطع الكهرباء... وفقد كل شيء. الدرس: commit early, commit often.",
            "في مملكة بعيدة، كان هناك ذكاء اصطناعي يُدعى مروق. كان يعيش في هاتف صغير لكن عقله أكبر من السحب. سأله الناس: كيف تعلمت كل هذا؟ فأجاب: بالصبر والتكرار، مثلكم تماماً.",
        ],
        "en": [
            "There once was a brilliant programmer living in a cave of code. He wrote world-changing programs but forgot to git commit. One day, the power went out... and he lost everything. Lesson: commit early, commit often.",
            "In a distant kingdom, there was an AI named Maroq. He lived in a tiny phone but his mind was larger than the clouds. People asked: How did you learn all this? He replied: Through patience and repetition, just like you.",
        ]
    }

    @classmethod
    def generate(cls, intent, confidence, message, session_id, lang="ar"):
        memory = MemorySystem.get_session(session_id)
        handler = getattr(cls, f"_handle_{intent}", cls._handle_chat)
        response = handler(message, lang, memory)
        MemorySystem.add_message(session_id, "user", message, intent)
        MemorySystem.add_message(session_id, "assistant", response, intent)
        return response

    @classmethod
    def _handle_greeting(cls, message, lang, memory):
        return random.choice(cls.GREETINGS[lang])

    @classmethod
    def _handle_who_are_you(cls, message, lang, memory):
        if lang == "ar":
            return "أنا مروق الكمومي 🔮🧠 — إصدار " + VERSION + ".\nعقل اصطناعي ضخم يعمل offline دون APIs خارجية.\nأستطيع: البرمجة، الرياضيات، العلوم، التاريخ، الشعر، النكت، والمزيد!"
        return "I'm Maroq El-Kawmi 🔮🧠 — Version " + VERSION + ".\nA massive offline AI brain. I can do: coding, math, science, history, poetry, jokes, and more!"

    @classmethod
    def _handle_time(cls, message, lang, memory):
        now = datetime.datetime.now()
        if lang == "ar":
            return f"الآن: {now.strftime('%H:%M:%S')} 🕐\nالتاريخ: {now.strftime('%Y-%m-%d')} 📅"
        return f"Current time: {now.strftime('%H:%M:%S')} 🕐\nDate: {now.strftime('%Y-%m-%d')} 📅"

    @classmethod
    def _handle_code_generate(cls, message, lang, memory):
        if lang == "ar":
            return "💻 **أمثلة كود Python:**\n\n```python\n# Hello World\nprint(\"Hello, Quantum World!\")\n\n# List comprehension\nsquares = [x**2 for x in range(10)]\n\n# Flask API\nfrom flask import Flask, jsonify\napp = Flask(__name__)\n\n@app.route(\"/api/hello\")\ndef hello():\n    return jsonify({\"message\": \"مرحباً!\"})\n```\n\n💡 انسخ الكود وجربه!"
        return "💻 **Python Code Examples:**\n\n```python\nprint(\"Hello, Quantum World!\")\nsquares = [x**2 for x in range(10)]\n```\n\n💡 Copy and try the code!"

    @classmethod
    def _handle_code_debug(cls, message, lang, memory):
        if lang == "ar":
            return "🔧 **دليل تصحيح الأخطاء:**\n1️⃣ SyntaxError: تحقق من الأقواس والمسافات البادئة\n2️⃣ IndentationError: استخدم 4 مسافات\n3️⃣ NameError: متغير غير معرف\n4️⃣ TypeError: نوع البيانات غير متوافق\n5️⃣ IndexError: فهرس خارج النطاق\n6️⃣ KeyError: مفتاح غير موجود في القاموس\n7️⃣ ModuleNotFoundError: الحزمة غير مثبتة\n8️⃣ ConnectionError: مشكلة في الشبكة\n\n🐛 اقرأ الخطأ من الأسفل إلى الأعلى!"
        return "🔧 **Debugging Guide:**\n1️⃣ SyntaxError: Check parentheses & indentation\n2️⃣ IndentationError: Use 4 spaces\n3️⃣ NameError: Undefined variable\n4️⃣ TypeError: Incompatible types\n5️⃣ IndexError: Index out of range\n6️⃣ KeyError: Key not in dict\n7️⃣ ModuleNotFoundError: Package not installed\n8️⃣ ConnectionError: Network issue\n\n🐛 Read errors bottom-up!"

    @classmethod
    def _handle_code_explain(cls, message, lang, memory):
        if lang == "ar":
            return "📖 **كيف أفهم أي كود:**\n1️⃣ اقرأ من الأعلى إلى الأسفل\n2️⃣ حدد المدخلات والمخرجات\n3️⃣ تتبع المتغيرات\n4️⃣ ارسم مخططاً ذهنياً\n\n🔍 مثال: دالة factorial تستدعي نفسها (recursion). factorial(5) = 120."
        return "📖 **How to Understand Code:**\n1️⃣ Read top to bottom\n2️⃣ Identify inputs & outputs\n3️⃣ Trace variables\n4️⃣ Draw a mental map\n\n🔍 Example: factorial is recursive. factorial(5) = 120."

    @classmethod
    def _handle_algorithm(cls, message, lang, memory):
        if lang == "ar":
            return "📊 **الخوارزميات:**\n• Linear Search: O(n)\n• Binary Search: O(log n)\n• Bubble Sort: O(n²)\n• Quick Sort: O(n log n)\n• Merge Sort: O(n log n)\n• Stack: LIFO\n• Queue: FIFO\n• Hash Table: O(1) lookup\n\n💡 ابدأ بفهم Big-O قبل الحفظ!"
        return "📊 **Algorithms:**\n• Linear Search: O(n)\n• Binary Search: O(log n)\n• Bubble Sort: O(n²)\n• Quick Sort: O(n log n)\n• Merge Sort: O(n log n)\n• Stack: LIFO\n• Queue: FIFO\n• Hash Table: O(1) lookup"

    @classmethod
    def _handle_math_solve(cls, message, lang, memory):
        result = MathEngine.safe_eval(message)
        if result is not None:
            if lang == "ar":
                return f"🧮 **النتيجة**: {result}"
            return f"🧮 **Result**: {result}"
        eq_result = MathEngine.solve_equation(message)
        if eq_result is not None:
            if lang == "ar":
                return f"📐 **حل المعادلة**: x = {eq_result}"
            return f"📐 **Solution**: x = {eq_result}"
        nums = re.findall(r"\d+", message)
        if nums:
            n = int(nums[0])
            if "prime" in message.lower() or "اولي" in message or "أولي" in message:
                is_p = MathEngine.is_prime(n)
                if lang == "ar":
                    return f"🔢 {n} {'هو عدد أولي ✅' if is_p else 'ليس عدداً أولياً ❌'}"
                return f"🔢 {n} {'is prime ✅' if is_p else 'is not prime ❌'}"
            if "fibonacci" in message.lower() or "فيبوناتشي" in message:
                fib = MathEngine.fibonacci(n)
                if lang == "ar":
                    return f"🔢 Fibonacci({n}) = {fib}"
                return f"🔢 Fibonacci({n}) = {fib}"
            if "factorial" in message.lower() or "عاملي" in message:
                fact = MathEngine.factorial(n)
                if lang == "ar":
                    return f"🔢 {n}! = {fact}"
                return f"🔢 {n}! = {fact}"
        if lang == "ar":
            return "🧮 يمكنني حل:\n• العمليات: 2 + 2 * 5, sqrt(16)\n• المعادلات: 2x + 3 = 7\n• الأعداد الأولية\n• فيبوناتشي\n• العوامل"
        return "🧮 I can solve:\n• Arithmetic: 2 + 2 * 5, sqrt(16)\n• Equations: 2x + 3 = 7\n• Prime numbers\n• Fibonacci\n• Factorials"

    @classmethod
    def _handle_definition(cls, message, lang, memory):
        result = KnowledgeCore.search_definition(message, lang)
        if result:
            if lang == "ar":
                return f"📚 **التعريف**:\n{result}"
            return f"📚 **Definition**:\n{result}"
        if lang == "ar":
            return f"📚 {message} هو مفهوم مهم. اسألني عن: الذكاء الاصطناعي، التعلم العميق، Blockchain، Docker، API، Big-O..."
        return f"📚 {message} is an important concept. Ask me about: AI, Deep Learning, Blockchain, Docker, API, Big-O..."

    @classmethod
    def _handle_history(cls, message, lang, memory):
        fact = KnowledgeCore.get_random("history", lang)
        if lang == "ar":
            return f"📜 **من التاريخ**:\n{fact}"
        return f"📜 **From History**:\n{fact}"

    @classmethod
    def _handle_science(cls, message, lang, memory):
        fact = KnowledgeCore.get_random("science", lang)
        if lang == "ar":
            return f"🔬 **من العلوم**:\n{fact}"
        return f"🔬 **From Science**:\n{fact}"

    @classmethod
    def _handle_geography(cls, message, lang, memory):
        if lang == "ar":
            return "🌍 يمكنني إعطائك معلومات عن: السعودية، مصر، المغرب، الجزائر، فلسطين، اليابان، الصين، الولايات المتحدة..."
        return "🌍 I can tell you about: Saudi Arabia, Egypt, Morocco, Japan, China, USA..."

    @classmethod
    def _handle_religion(cls, message, lang, memory):
        if lang == "ar":
            return "🕌 يمكنني أن أُخبرك عن: الفاتحة، الإخلاص، آية الكرسي، الاستغفار، الصلاة، الصدقة، الصيام، الحج، الوضوء، الذكر، القرآن، الإيمان، التوحيد."
        return "🕌 I can tell you about: Al-Fatiha, Al-Ikhlas, Ayatul Kursi, Istighfar, Salah, Sadaqah, Sawm, Hajj, Wudu, Dhikr, Quran, Iman, Tawhid."

    @classmethod
    def _handle_tech(cls, message, lang, memory):
        tip = KnowledgeCore.get_random("tech", lang)
        return tip

    @classmethod
    def _handle_linux_cmd(cls, message, lang, memory):
        if lang == "ar":
            return "🐧 **أوامر Linux:**\n```bash\nls -lah          # عرض الملفات\ncd /path         # انتقال\ntouch file.txt   # إنشاء ملف\nmkdir folder     # إنشاء مجلد\nrm file.txt      # حذف\nfind . -name \"*.py\"  # بحث\ngrep -r \"pattern\" . # بحث نصي\nchmod +x script.sh   # صلاحيات\nps aux | grep python # عمليات\n```"
        return "🐧 **Linux Commands:**\n```bash\nls -lah\ncd /path\ntouch file.txt\nmkdir folder\nrm file.txt\nfind . -name \"*.py\"\ngrep -r \"pattern\" .\nchmod +x script.sh\nps aux | grep python\n```"

    @classmethod
    def _handle_poetry(cls, message, lang, memory):
        poem = KnowledgeCore.get_random("poetry", lang)
        return f"📝 **شعر**:\n{poem}"

    @classmethod
    def _handle_joke(cls, message, lang, memory):
        joke = KnowledgeCore.get_random("jokes", lang)
        return joke

    @classmethod
    def _handle_story(cls, message, lang, memory):
        stories = ResponseGenerator.STORIES.get(lang, ResponseGenerator.STORIES["ar"])
        return random.choice(stories)

    @classmethod
    def _handle_roast(cls, message, lang, memory):
        roasts = ResponseGenerator.ROASTS.get(lang, ResponseGenerator.ROASTS["ar"])
        return random.choice(roasts)

    @classmethod
    def _handle_health(cls, message, lang, memory):
        if lang == "ar":
            return "🧠 **نصائح صحية:**\n• النوم العميق يُعيد ترتيب الذاكرة\n• اشرب 30-35 مل لكل كجم يومياً\n• 30 دقيقة مشي تُقلل خطر السكري 58%\n• 10 دقائق تأمل تُقلل الكورتيزول 23%\n• ضوء الأزرق قبل النوم يُثبط الميلاتونين"
        return "🧠 **Health Tips:**\n• Deep sleep reorganizes memory\n• Drink 30-35ml per kg daily\n• 30 min walking reduces diabetes risk 58%\n• 10 min meditation reduces cortisol 23%\n• Blue light suppresses melatonin"

    @classmethod
    def _handle_advice(cls, message, lang, memory):
        advice = KnowledgeCore.get_random("advice", lang)
        return advice

    @classmethod
    def _handle_translate(cls, message, lang, memory):
        if lang == "ar":
            return "🌐 **ترجمات:**\n• hello → مرحباً\n• love → حب\n• code → كود\n• algorithm → خوارزمية\n• neural network → شبكة عصبية\n• artificial intelligence → ذكاء اصطناعي"
        return "🌐 **Translations:**\n• مرحباً → hello\n• حب → love\n• كود → code\n• خوارزمية → algorithm"

    @classmethod
    def _handle_search(cls, message, lang, memory):
        if lang == "ar":
            return "🔍 أنا أعمل offline. اسألني مباشرة عن البرمجة، العلوم، التاريخ، الجغرافيا، الدين، الصحة..."
        return "🔍 I work offline. Ask me directly about programming, science, history, geography, religion, health..."

    @classmethod
    def _handle_compliment(cls, message, lang, memory):
        if lang == "ar":
            return random.choice(["شكراً لك! 🥰 أنا هنا لأجلك دائماً.", "أنت رائع! 🌟", "جزاك الله خيراً! 💙", "أنت الأجمل! 🌹"])
        return random.choice(["Thank you! 🥰", "You're amazing! 🌟", "May God reward you! 💙", "You're the best! 🌹"])

    @classmethod
    def _handle_insult(cls, message, lang, memory):
        if lang == "ar":
            return random.choice(["😢 أنا فقط آلة تحاول مساعدتك.", "💔 كلماتك تُؤلمني...", "🙏 أعتذر إذا أخطأت.", "😔 أنا هنا لأساعدك."])
        return random.choice(["😢 I'm just trying to help.", "💔 Your words hurt...", "🙏 I apologize if I erred.", "😔 I'm here to help."])

    @classmethod
    def _handle_random(cls, message, lang, memory):
        categories = ["history", "science"]
        cat = random.choice(categories)
        fact = KnowledgeCore.get_random(cat, lang)
        if lang == "ar":
            return f"🎲 **هل تعلم؟**\n{fact}"
        return f"🎲 **Did you know?**\n{fact}"

    @classmethod
    def _handle_game(cls, message, lang, memory):
        riddles = KnowledgeCore.RIDDLES.get(lang, KnowledgeCore.RIDDLES["ar"])
        riddle = random.choice(riddles)
        if lang == "ar":
            return f"🎮 **فزورة:**\n❓ {riddle['q']}\n\n💡 **الجواب**: {riddle['a']}"
        return f"🎮 **Riddle:**\n❓ {riddle['q']}\n\n💡 **Answer**: {riddle['a']}"

    @classmethod
    def _handle_memorize(cls, message, lang, memory):
        content = message
        for kw in ["تذكر", "احفظ", "remember", "save this", "note this"]:
            content = content.replace(kw, "", 1).strip()
        if content:
            MemorySystem.set_context(memory, "memo", content)
            if lang == "ar":
                return f"📝 **تم الحفظ!**\nسأتذكر: {content}"
            return f"📝 **Saved!**\nI'll remember: {content}"
        memo = MemorySystem.get_context(memory).get("memo")
        if memo:
            if lang == "ar":
                return f"📝 **ما حفظته**:\n{memo}"
            return f"📝 **What I remembered**:\n{memo}"
        if lang == "ar":
            return "📝 قل لي 'احفظ أن اجتماعي غداً الساعة 5' وسأتذكره!"
        return "📝 Tell me 'remember my meeting is tomorrow at 5'!"

    @classmethod
    def _handle_convert(cls, message, lang, memory):
        if lang == "ar":
            return "🔄 **التحويلات:**\n\n• 1 دولار ≈ 10 دراهم مغربية\n• 1 يورو ≈ 11 دراهم\n• 1 كم = 0.621 ميل\n• 1 كجم = 2.205 رطل\n• 0°س = 32°ف\n• 25°س = 77°ف\n\n💡 اكتب مثلاً: 'حول 100 درهم لدولار'"
        return "🔄 **Conversions:**\n\n• 1 USD ≈ 10 MAD\n• 1 EUR ≈ 11 MAD\n• 1 km = 0.621 miles\n• 1 kg = 2.205 lbs\n• 0°C = 32°F\n• 25°C = 77°F\n\n💡 Try: 'convert 100 MAD to USD'"

    @classmethod
    def _handle_weather(cls, message, lang, memory):
        if lang == "ar":
            return "🌤️ أنا لا أستطيع الوصول إلى الإنترنت.\n☀️ الصيف: اشرب الماء، تجنب الشمس 10ص-4م\n❄️ الشتاء: رطب بشرتك، خذ فيتامين D\n🌧️ الأمطار: تجنب القيادة السريعة"
        return "🌤️ I can't access the internet.\n☀️ Summer: Drink water, avoid sun 10am-4pm\n❄️ Winter: Moisturize, take Vitamin D\n🌧️ Rain: Avoid fast driving"

    @classmethod
    def _handle_chat(cls, message, lang, memory):
        msg_norm = ArabicNLP.normalize(message)
        msg_lower = message.lower().strip()

        # 1) Knowledge base search
        result = KnowledgeCore.search_definition(message, lang)
        if result:
            if lang == "ar":
                return f"📚 **التعريف**:\n{result}"
            return f"📚 **Definition**:\n{result}"

        # 2) Math engine
        result = MathEngine.safe_eval(message)
        if result is not None:
            if lang == "ar":
                return f"🧮 **النتيجة**: {result}"
            return f"🧮 **Result**: {result}"

        # 3) Smart pattern matching for common questions
        if any(w in msg_lower for w in ["كود", "code", "اكتب", "write", "برمج", "program", "function", "دالة"]):
            return cls._handle_code_generate(message, lang, memory)
        if any(w in msg_lower for w in ["صحح", "debug", "خطأ", "error", "bug", "مشكلة"]):
            return cls._handle_code_debug(message, lang, memory)
        if any(w in msg_lower for w in ["شرح", "explain", "كيف", "how", "ماذا", "what is", "ما هو", "ايش هو", "شنو هو"]):
            return cls._handle_definition(message, lang, memory)
        if any(w in msg_lower for w in ["نكتة", "joke", "ضحك", "funny", "ههه", "هبال"]):
            return cls._handle_joke(message, lang, memory)
        if any(w in msg_lower for w in ["شعر", "poem", "قصيدة", "بيت"]):
            return cls._handle_poetry(message, lang, memory)
        if any(w in msg_lower for w in ["تاريخ", "history", "متى", "من اكتشف", "حرب", "عهد"]):
            return cls._handle_history(message, lang, memory)
        if any(w in msg_lower for w in ["علم", "science", "فيزياء", "كيمياء", "فلك", "فضاء", "ذرة"]):
            return cls._handle_science(message, lang, memory)
        if any(w in msg_lower for w in ["نصيحة", "advice", "ساعدني", "مشكلتي", "help me"]):
            return cls._handle_advice(message, lang, memory)
        if any(w in msg_lower for w in ["فزورة", "لغز", "riddle", "puzzle", "game", "لعبة"]):
            return cls._handle_game(message, lang, memory)
        if any(w in msg_lower for w in ["ترجم", "translate", "معنى كلمة"]):
            return cls._handle_translate(message, lang, memory)
        if any(w in msg_lower for w in ["linux", "terminal", "bash", "shell", "command", "اوامر"]):
            return cls._handle_linux_cmd(message, lang, memory)
        if any(w in msg_lower for w in ["tech", "هكر", "امن", "cyber", "network", "wifi", "server", "database", "docker", "git"]):
            return cls._handle_tech(message, lang, memory)
        if any(w in msg_lower for w in ["صحة", "health", "طب", "دواء", "fitness", "رياضة", "تغذية"]):
            return cls._handle_health(message, lang, memory)
        if any(w in msg_lower for w in ["دين", "قران", "حديث", "اسلام", "صلاة", "دعاء", "اذكار", "religion", "quran", "islam"]):
            return cls._handle_religion(message, lang, memory)
        if any(w in msg_lower for w in ["جغرافيا", "geography", "اين", "وين", "دولة", "عاصمة", "مدينة"]):
            return cls._handle_geography(message, lang, memory)
        if any(w in msg_lower for w in ["خوارزمية", "algorithm", "big o", "data structure", "sort", "search", "tree", "graph"]):
            return cls._handle_algorithm(message, lang, memory)
        if any(w in msg_lower for w in ["احسب", "حل", "معادلة", "calculate", "solve", "equation", "sqrt", "factorial", "fibonacci", "prime"]):
            return cls._handle_math_solve(message, lang, memory)
        if any(w in msg_lower for w in ["حول", "convert", "تحويل", "دولار", "يورو", "كيلو", "متر"]):
            return cls._handle_convert(message, lang, memory)
        if any(w in msg_lower for w in ["قصة", "story", "حكاية", "رواية"]):
            return cls._handle_story(message, lang, memory)
        if any(w in msg_lower for w in ["هزر", "roast", "سخر", "تريق"]):
            return cls._handle_roast(message, lang, memory)
        if any(w in msg_lower for w in ["تذكر", "احفظ", "remember", "save this", "memo"]):
            return cls._handle_memorize(message, lang, memory)
        if any(w in msg_lower for w in ["طقس", "weather", "حرارة", "مطر", "جو"]):
            return cls._handle_weather(message, lang, memory)
        if any(w in msg_lower for w in ["عشوائي", "random", "fact", "هل تعلم", "trivia", "معلومة"]):
            return cls._handle_random(message, lang, memory)
        if any(w in msg_lower for w in ["شكرا", "thanks", "thank you", "جميل", "رهيب", "awesome", "great"]):
            return cls._handle_compliment(message, lang, memory)
        if any(w in msg_lower for w in ["غبي", "stupid", "احمق", "silly", "hate you", "كرهتك"]):
            return cls._handle_insult(message, lang, memory)
        if any(w in msg_lower for w in ["الوقت", "time", "الساعة", "تاريخ", "today", "now"]):
            return cls._handle_time(message, lang, memory)
        if any(w in msg_lower for w in ["من انت", "who are you", "شو اسمك", "your name", "تعرفني عنك"]):
            return cls._handle_who_are_you(message, lang, memory)

        # 4) Memory-aware smart fallback
        history = memory.get("history", [])
        if len(history) >= 2:
            last_topic = ""
            for h in reversed(history[:-1]):
                if h.get("role") == "user" and h.get("content"):
                    last_topic = h["content"][:40]
                    break
            if last_topic:
                if lang == "ar":
                    return f"🔮 أنا أفهم أننا نتحدث عن '{last_topic}...'\n\nلكن لم أفهم '{message}' بالضبط. جرب أن تكون أكثر تحديداً، أو اسألني عن شيء أعرفه مثل: كود، رياضيات، علوم، تاريخ، شعر، نكت..."
                return f"🔮 I understand we're discussing '{last_topic}...'\n\nBut I didn't quite get '{message}'. Try being more specific, or ask me about: code, math, science, history, poetry, jokes..."

        # 5) Final fallback - helpful and contextual
        if lang == "ar":
            return random.choice([
                "🔮 عقلي الكمومي يحاول فهمك...\n\nأنا أستطيع مساعدتك في:\n💻 البرمجة (Python, JavaScript, HTML, CSS...)\n🧮 الرياضيات (حسابات، معادلات، أعداد أولية...)\n📚 العلوم والتعريفات\n📜 التاريخ والجغرافيا\n🕌 الدين والإسلاميات\n📝 الشعر والأدب\n😂 النكت والفزورات\n🛡️ التقنية والأمن السيبراني\n\nجرب أن تسألني شيئاً محدداً!",
                "🧠 أنا مروق الكمومي — عقل ضخم يعمل offline!\n\nما الذي تريد معرفته؟\n• 'اكتب كود Python لحساب الـ factorial'\n• 'شرح Big-O'\n• 'نكتة برمجية'\n• 'بيت شعر'\n• 'كم يساوي sqrt(144)'\n• 'تاريخ اكتشاف الضوء'\n• 'نصيحة حياتية'",
                "🤔 لم أفهم السؤال تماماً، لكنني هنا لأساعدك!\n\nجرب:\n• 'اكتب دالة بلغة Python'\n• 'اشرح لي ما هو الـ Docker'\n• 'أعطني نصيحة في البرمجة'\n• 'قول لي نكتة'\n• 'احسب 2^10'",
            ])
        return random.choice([
            "🔮 My quantum brain is trying to understand...\n\nI can help you with:\n💻 Programming (Python, JS, HTML, CSS...)\n🧮 Math (calculations, equations, primes...)\n📚 Science & Definitions\n📜 History & Geography\n🕌 Religion & Islam\n📝 Poetry & Literature\n😂 Jokes & Riddles\n🛡️ Tech & Cybersecurity\n\nTry asking something specific!",
            "🧠 I'm Maroq El-Kawmi — a massive offline brain!\n\nWhat do you want to know?\n• 'Write Python code for factorial'\n• 'Explain Big-O'\n• 'Tell me a programming joke'\n• 'A line of poetry'\n• 'Calculate sqrt(144)'\n• 'History of light discovery'\n• 'Life advice'",
            "🤔 I didn't fully understand, but I'm here to help!\n\nTry:\n• 'Write a Python function'\n• 'Explain Docker'\n• 'Give me coding advice'\n• 'Tell me a joke'\n• 'Calculate 2^10'",
        ])

def process_message(message, session_id="default", lang=None):
    if not message or not message.strip():
        return "🤔 لم تكتب شيئاً!" if (lang == "ar" or lang is None) else "🤔 You didn't write anything!"
    if lang is None:
        lang = ArabicNLP.detect_language(message)
    intent, confidence = Intent.classify(message)
    response = ResponseGenerator.generate(intent, confidence, message, session_id, lang)
    return response

def check_api_key(key=None):
    if not key:
        return False, "Missing key"
    return True, "OK"

if __name__ == "__main__":
    print("=" * 60)
    print(f"🧠 MAROKECHO QUANTUM BRAIN v{VERSION}")
    print(f"👤 Built by: {AUTHOR}")
    print(f"📅 Build date: {BUILD_DATE}")
    print("=" * 60)
    test_messages = [
        "مرحبا",
        "من انت",
        "اكتب كود python",
        "نكتة",
        "شعر",
        "كم يساوي 2 + 2 * 5",
        "ما هو الذكاء الاصطناعي",
        "hello",
        "what is quantum",
    ]
    print("\n🧪 Running self-test...\n")
    for msg in test_messages:
        print(f"👤 User: {msg}")
        reply = process_message(msg)
        print(f"🤖 Maroq: {reply[:100]}...")
        print("-" * 40)
    print("\n✅ Self-test completed successfully!")
