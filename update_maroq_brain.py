#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update Maroq Brain - Smart _handle_chat patch"""

import re

p = '/storage/emulated/0/mrook_echo/backend/components.py'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

print("📊 Original file size:", len(c), "chars")

old_chat = """    @classmethod
    def _handle_chat(cls, message, lang, memory):
        result = KnowledgeCore.search_definition(message, lang)
        if result:
            if lang == "ar":
                return f"📚 **التعريف**:\\n{result}"
            return f"📚 **Definition**:\\n{result}"
        result = MathEngine.safe_eval(message)
        if result is not None:
            if lang == "ar":
                return f"🧮 **النتيجة**: {result}"
            return f"🧮 **Result**: {result}"
        fallbacks = [
            "أنا مروق الكمومي، ولسوء الحظ لم أفهم طلبك بالكامل. يمكنك أن تسألني عن: كود برمجي، حسابات رياضية، تعريفات علمية، جغرافيا، تاريخ، إسلاميات، نكت، شعر، أو أي شيء آخر!",
            "عذراً، عقلي الكمومي يحتاج توضيحاً أكثر. جرب أن تسألني 'اكتب كود Python' أو 'نكتة' أو 'ما هي الكمومية؟'",
        ]
        return random.choice(fallbacks)"""

new_chat = """    @classmethod
    def _handle_chat(cls, message, lang, memory):
        msg_norm = ArabicNLP.normalize(message)
        msg_lower = message.lower().strip()
        
        # 1) Knowledge base search
        result = KnowledgeCore.search_definition(message, lang)
        if result:
            if lang == "ar":
                return f"📚 **التعريف**:\\n{result}"
            return f"📚 **Definition**:\\n{result}"
        
        # 2) Math engine
        result = MathEngine.safe_eval(message)
        if result is not None:
            if lang == "ar":
                return f"🧮 **النتيجة**: {result}"
            return f"🧮 **Result**: {result}"
        
        # 3) Smart keyword routing to all handlers
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
        
        # 4) Memory-aware fallback
        history = memory.get("history", [])
        if len(history) >= 2:
            last_topic = ""
            for h in reversed(history[:-1]):
                if h.get("role") == "user" and h.get("content"):
                    last_topic = h["content"][:40]
                    break
            if last_topic:
                if lang == "ar":
                    return f"🔮 أنا أفهم أننا نتحدث عن '{last_topic}...'\\n\\nلكن لم أفهم '{message}' بالضبط. جرب أن تكون أكثر تحديداً، أو اسألني عن شيء أعرفه مثل: كود، رياضيات، علوم، تاريخ، شعر، نكت..."
                return f"🔮 I understand we're discussing '{last_topic}...'\\n\\nBut I didn't quite get '{message}'. Try being more specific, or ask me about: code, math, science, history, poetry, jokes..."
        
        # 5) Rich fallback
        if lang == "ar":
            return random.choice([
                "🔮 عقلي الكمومي يحاول فهمك...\\n\\nأنا أستطيع مساعدتك في:\n💻 البرمجة (Python, JavaScript, HTML, CSS...)\n🧮 الرياضيات (حسابات، معادلات، أعداد أولية...)\n📚 العلوم والتعريفات\n📜 التاريخ والجغرافيا\n🕌 الدين والإسلاميات\n📝 الشعر والأدب\n😂 النكت والفزورات\n🛡️ التقنية والأمن السيبراني\n\nجرب أن تسألني شيئاً محدداً!",
                "🧠 أنا مروق الكمومي — عقل ضخم يعمل offline!\\n\\nما الذي تريد معرفته؟\n• 'اكتب كود Python لحساب الـ factorial'\n• 'شرح Big-O'\n• 'نكتة برمجية'\n• 'بيت شعر'\n• 'كم يساوي sqrt(144)'\n• 'تاريخ اكتشاف الضوء'\n• 'نصيحة حياتية'",
                "🤔 لم أفهم السؤال تماماً، لكنني هنا لأساعدك!\\n\\nجرب:\n• 'اكتب دالة بلغة Python'\n• 'اشرح لي ما هو الـ Docker'\n• 'أعطني نصيحة في البرمجة'\n• 'قول لي نكتة'\n• 'احسب 2^10'",
            ])
        return random.choice([
            "🔮 My quantum brain is trying to understand...\\n\\nI can help you with:\n💻 Programming (Python, JS, HTML, CSS...)\n🧮 Math (calculations, equations, primes...)\n📚 Science & Definitions\n📜 History & Geography\n🕌 Religion & Islam\n📝 Poetry & Literature\n😂 Jokes & Riddles\n🛡️ Tech & Cybersecurity\n\nTry asking something specific!",
            "🧠 I'm Maroq El-Kawmi — a massive offline brain!\\n\\nWhat do you want to know?\n• 'Write Python code for factorial'\n• 'Explain Big-O'\n• 'Tell me a programming joke'\n• 'A line of poetry'\n• 'Calculate sqrt(144)'\n• 'History of light discovery'\n• 'Life advice'",
            "🤔 I didn't fully understand, but I'm here to help!\\n\\nTry:\n• 'Write a Python function'\n• 'Explain Docker'\n• 'Give me coding advice'\n• 'Tell me a joke'\n• 'Calculate 2^10'",
        ])"""

if old_chat in c:
    c = c.replace(old_chat, new_chat)
    print("✅ _handle_chat replaced directly!")
else:
    print("⚠️ Direct match failed, trying regex...")
    pattern = r'(@classmethod\s+def _handle_chat\(cls, message, lang, memory\):.*?)(?=\n    @classmethod\s+def _handle_greeting)'
    match = re.search(pattern, c, re.DOTALL)
    if match:
        c = c.replace(match.group(1), new_chat + "\n\n")
        print("✅ _handle_chat replaced via regex!")
    else:
        print("❌ Could not find _handle_chat. Aborting.")
        exit(1)

if "def _handle_convert" not in c:
    convert_method = """
    @classmethod
    def _handle_convert(cls, message, lang, memory):
        if lang == "ar":
            return "🔄 **التحويلات:**\n\n• 1 دولار ≈ 10 دراهم مغربية\n• 1 يورو ≈ 11 دراهم\n• 1 كم = 0.621 ميل\n• 1 كجم = 2.205 رطل\n• 0°س = 32°ف\n• 25°س = 77°ف\n\n💡 اكتب مثلاً: 'حول 100 درهم لدولار'"
        return "🔄 **Conversions:**\n\n• 1 USD ≈ 10 MAD\n• 1 EUR ≈ 11 MAD\n• 1 km = 0.621 miles\n• 1 kg = 2.205 lbs\n• 0°C = 32°F\n• 25°C = 77°F\n\n💡 Try: 'convert 100 MAD to USD'"
"""
    c = c.replace("    @classmethod\n    def _handle_weather", convert_method + "    @classmethod\n    def _handle_weather")
    print("✅ _handle_convert added!")
else:
    print("ℹ️ _handle_convert already exists")

with open(p, "w", encoding="utf-8") as f:
    f.write(c)

print("📊 New file size:", len(c), "chars")
print("🎉 components.py updated successfully on device!")
