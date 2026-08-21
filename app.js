/**
 * ⚡ مروق AI الكمومي - Quantum Robot Assistant
 * يتضمن: Three.js Robot, Web Speech, Weather, Touch, Kimi API
 */

// ===== المتغيرات العامة =====
let currentLang = 'ar';
let isVoiceEnabled = true;
let isTouchEnabled = true;
let isListening = false;
let recognition = null;
let synth = window.speechSynthesis;
let robotScene, robotCamera, robotRenderer, robotMesh;
let mouthAnimationInterval = null;

// ===== التهيئة =====
document.addEventListener('DOMContentLoaded', () => {
    initQuantumBackground();
    initRobot3D();
    initClock();
    initWeather();
    initSpeech();
    initTouch();
    initChat();
    initParticles();
    updateQuantumSignature();

    // رسالة ترحيب صوتية
    setTimeout(() => {
        speak(getWelcomeMessage(currentLang), currentLang);
        showBubble(getWelcomeMessage(currentLang));
    }, 1500);
});

// ===== خلفية الكم =====
function initQuantumBackground() {
    const canvas = document.getElementById('quantum-bg');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    for (let i = 0; i < 80; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 2 + 1,
            color: Math.random() > 0.5 ? '#00f3ff' : '#ff00ff'
        });
    }

    function animate() {
        ctx.fillStyle = 'rgba(10, 10, 26, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 10;
            ctx.shadowColor = p.color;
            ctx.fill();
        });

        // ربط الجسيمات
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 100) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(0, 243, 255, ${0.1 * (1 - dist / 100)})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// ===== جسيمات DOM =====
function initParticles() {
    const container = document.getElementById('particles');
    for (let i = 0; i < 20; i++) {
        const p = document.createElement('div');
        p.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: ${Math.random() > 0.5 ? '#00f3ff' : '#ff00ff'};
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            opacity: ${Math.random() * 0.5 + 0.2};
            animation: floatParticle ${Math.random() * 10 + 10}s infinite ease-in-out;
            pointer-events: none;
        `;
        container.appendChild(p);
    }

    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatParticle {
            0%, 100% { transform: translate(0, 0); }
            25% { transform: translate(${Math.random()*50}px, -${Math.random()*50}px); }
            50% { transform: translate(-${Math.random()*30}px, ${Math.random()*30}px); }
            75% { transform: translate(${Math.random()*40}px, ${Math.random()*40}px); }
        }
    `;
    document.head.appendChild(style);
}

// ===== روبوت Three.js =====
function initRobot3D() {
    const container = document.getElementById('robot-canvas');
    if (!container || typeof THREE === 'undefined') {
        console.log('Three.js not available, using CSS robot');
        return;
    }

    robotScene = new THREE.Scene();
    robotCamera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    robotRenderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    robotRenderer.setSize(container.clientWidth, container.clientHeight);
    robotRenderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(robotRenderer.domElement);

    // إضاءة نيون
    const ambientLight = new THREE.AmbientLight(0x404040, 2);
    robotScene.add(ambientLight);

    const blueLight = new THREE.PointLight(0x00f3ff, 2, 50);
    blueLight.position.set(5, 5, 5);
    robotScene.add(blueLight);

    const pinkLight = new THREE.PointLight(0xff00ff, 2, 50);
    pinkLight.position.set(-5, -5, 5);
    robotScene.add(pinkLight);

    // جسم الروبوت
    const geometry = new THREE.IcosahedronGeometry(2, 1);
    const material = new THREE.MeshPhongMaterial({
        color: 0x00f3ff,
        emissive: 0x001133,
        specular: 0xffffff,
        shininess: 100,
        wireframe: true,
        transparent: true,
        opacity: 0.6
    });
    robotMesh = new THREE.Mesh(geometry, material);
    robotScene.add(robotMesh);

    // طبقة داخلية
    const innerGeo = new THREE.IcosahedronGeometry(1.5, 0);
    const innerMat = new THREE.MeshPhongMaterial({
        color: 0xff00ff,
        emissive: 0x330033,
        transparent: true,
        opacity: 0.3
    });
    const innerMesh = new THREE.Mesh(innerGeo, innerMat);
    robotMesh.add(innerMesh);

    robotCamera.position.z = 6;

    function animateRobot() {
        requestAnimationFrame(animateRobot);
        robotMesh.rotation.x += 0.003;
        robotMesh.rotation.y += 0.005;
        robotMesh.scale.setScalar(1 + Math.sin(Date.now() * 0.001) * 0.05);
        robotRenderer.render(robotScene, robotCamera);
    }
    animateRobot();

    window.addEventListener('resize', () => {
        robotCamera.aspect = container.clientWidth / container.clientHeight;
        robotCamera.updateProjectionMatrix();
        robotRenderer.setSize(container.clientWidth, container.clientHeight);
    });
}

// ===== الساعة الكمومية =====
function initClock() {
    function updateClock() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('ar-SA', { hour12: false });
        const dateStr = now.toLocaleDateString('ar-SA', { 
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
        });

        document.getElementById('digitalClock').textContent = timeStr;
        document.getElementById('dateDisplay').textContent = dateStr;
        document.getElementById('quantumClock').textContent = timeStr;

        // موقع الشمس
        const hour = now.getHours();
        let sunPos = '🌙 ليل';
        if (hour >= 5 && hour < 12) sunPos = '🌅 صباح';
        else if (hour >= 12 && hour < 17) sunPos = '☀️ ظهر';
        else if (hour >= 17 && hour < 20) sunPos = '🌇 مغرب';
        document.getElementById('sunPos').textContent = sunPos;

        // مرحلة القمر
        const phases = ['🌑 محاق', '🌒 هلال', '🌓 تربيع', '🌔 أحدب', '🌕 بدر', '🌖 أحدب', '🌗 تربيع', '🌘 هلال'];
        const dayOfMonth = now.getDate();
        document.getElementById('moonPhase').textContent = phases[dayOfMonth % 8];
    }
    updateClock();
    setInterval(updateClock, 1000);
}

// ===== الطقس =====
function initWeather() {
    updateWeather();
    setInterval(updateWeather, 600000); // تحديث كل 10 دقائق
}

function updateWeather() {
    // محاكاة بيانات الطقس (يمكن ربطها بـ OpenWeatherMap API)
    const conditions = [
        { icon: '☀️', desc: 'مشمس', temp: 32, humidity: 45, wind: 12, visibility: 10 },
        { icon: '⛅', desc: 'غائم جزئياً', temp: 28, humidity: 55, wind: 15, visibility: 9 },
        { icon: '☁️', desc: 'غائم', temp: 25, humidity: 65, wind: 18, visibility: 7 },
        { icon: '🌧️', desc: 'ممطر خفيف', temp: 22, humidity: 80, wind: 20, visibility: 5 },
    ];
    const w = conditions[Math.floor(Math.random() * conditions.length)];

    document.getElementById('weatherIcon').textContent = w.icon;
    document.getElementById('weatherTemp').textContent = w.temp + '°C';
    document.getElementById('weatherDesc').textContent = w.desc;
    document.getElementById('humidity').textContent = w.humidity;
    document.getElementById('wind').textContent = w.wind;
    document.getElementById('visibility').textContent = w.visibility;
}

// ===== التوقيع الكمومي =====
function updateQuantumSignature() {
    const sig = 'Q-' + Math.floor(Math.random() * 9000 + 1000) + '.' + Math.floor(Math.random() * 99);
    document.getElementById('quantumSig').textContent = '⚡' + sig;
    setTimeout(updateQuantumSignature, 5000);
}

// ===== رسائل الترحيب =====
function getWelcomeMessage(lang) {
    const msgs = {
        ar: 'مرحباً! أنا مروق الكمومي. يمكنني التحدث بعشر لغات! ⚡',
        en: 'Hello! I am Mrook Quantum. I can speak 10 languages! ⚡',
        fr: 'Bonjour! Je suis Mrook Quantum. Je parle 10 langues! ⚡',
        es: '¡Hola! Soy Mrook Quantum. ¡Puedo hablar 10 idiomas! ⚡',
        de: 'Hallo! Ich bin Mrook Quantum. Ich spreche 10 Sprachen! ⚡',
        zh: '你好！我是Mrook Quantum。我会说10种语言！⚡',
        ja: 'こんにちは！私はMrook Quantumです。10言語話せます！⚡',
        ru: 'Привет! Я Mrook Quantum. Я говорю на 10 языках! ⚡',
        tr: 'Merhaba! Ben Mrook Quantum. 10 dil konuşabilirim! ⚡',
        ur: 'سلام! میں مروق کوانٹم ہوں۔ میں 10 زبانیں بول سکتا ہوں! ⚡'
    };
    return msgs[lang] || msgs['en'];
}

// ===== نظام الصوت (Text-to-Speech + Speech Recognition) =====
function initSpeech() {
    // Text-to-Speech
    if (!('speechSynthesis' in window)) {
        console.warn('Speech Synthesis not supported');
        isVoiceEnabled = false;
        return;
    }

    // Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            isListening = true;
            document.getElementById('micBtn').classList.add('listening');
            document.getElementById('voiceBar').classList.add('active');
            document.getElementById('chatInput').placeholder = 'يستمع... تحدث الآن 🎤';
        };

        recognition.onend = () => {
            isListening = false;
            document.getElementById('micBtn').classList.remove('listening');
            document.getElementById('voiceBar').classList.remove('active');
            document.getElementById('chatInput').placeholder = 'اكتب رسالتك هنا... أو اضغط الميكروفون 🎤';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('chatInput').value = transcript;
            handleSendMessage(transcript);
        };

        recognition.onerror = (event) => {
            console.error('Speech error:', event.error);
            showBubble('⚠️ لم أسمعك جيداً، حاول مرة أخرى');
        };
    }
}

function speak(text, lang) {
    if (!isVoiceEnabled || !synth) return;

    // إيقاف أي كلام سابق
    synth.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = getLangCode(lang);
    utterance.rate = 0.9;
    utterance.pitch = 1.1;
    utterance.volume = 1;

    // تحريك الفم
    utterance.onstart = () => startMouthAnimation();
    utterance.onend = () => stopMouthAnimation();
    utterance.onerror = () => stopMouthAnimation();

    synth.speak(utterance);
}

function getLangCode(lang) {
    const codes = {
        ar: 'ar-SA', en: 'en-US', fr: 'fr-FR', es: 'es-ES',
        de: 'de-DE', zh: 'zh-CN', ja: 'ja-JP', ru: 'ru-RU',
        tr: 'tr-TR', ur: 'ur-PK'
    };
    return codes[lang] || 'en-US';
}

function startMouthAnimation() {
    const mouth = document.getElementById('robotMouth');
    const eyes = document.querySelectorAll('.eye');
    mouth.classList.add('talking');
    eyes.forEach(eye => eye.classList.add('talking'));
}

function stopMouthAnimation() {
    const mouth = document.getElementById('robotMouth');
    const eyes = document.querySelectorAll('.eye');
    mouth.classList.remove('talking');
    eyes.forEach(eye => eye.classList.remove('talking'));
}

function toggleListening() {
    if (!recognition) {
        showBubble('⚠️ المتصفح لا يدعم التعرف على الصوت');
        return;
    }

    if (isListening) {
        recognition.stop();
    } else {
        recognition.lang = getLangCode(currentLang);
        recognition.start();
    }
}

// ===== نظام المحادثة =====
function initChat() {
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const micBtn = document.getElementById('micBtn');
    const langSelect = document.getElementById('langSelect');

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSendMessage(input.value);
    });

    sendBtn.addEventListener('click', () => handleSendMessage(input.value));
    micBtn.addEventListener('click', toggleListening);

    langSelect.addEventListener('change', (e) => {
        currentLang = e.target.value;
        const msg = getLangChangeMessage(currentLang);
        addBotMessage(msg);
        speak(msg, currentLang);
    });

    // أزرار التذييل
    document.getElementById('voiceToggle').addEventListener('click', function() {
        isVoiceEnabled = !isVoiceEnabled;
        this.classList.toggle('active', isVoiceEnabled);
        this.textContent = isVoiceEnabled ? '🔊' : '🔇';
    });

    document.getElementById('themeToggle').addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        this.textContent = document.body.classList.contains('dark-theme') ? '☀️' : '🌙';
    });

    document.getElementById('touchToggle').addEventListener('click', function() {
        isTouchEnabled = !isTouchEnabled;
        this.classList.toggle('active', isTouchEnabled);
        showBubble(isTouchEnabled ? '👆 اللمس مفعل' : '👆 اللمس معطل');
    });

    document.getElementById('addAlertBtn').addEventListener('click', () => {
        const alerts = [
            '💧 اشرب الماء الآن!',
            '👁️ أرح عينيك - انظر بعيداً',
            '🚶 قم وامشِ قليلاً',
            '🧘 خذ نفساً عميقاً',
            '☕ استراحة قصيرة!'
        ];
        const alert = alerts[Math.floor(Math.random() * alerts.length)];
        addAlert('الآن', alert);
        speak(alert, currentLang);
    });
}

function handleSendMessage(text) {
    text = text.trim();
    if (!text) return;

    document.getElementById('chatInput').value = '';
    addUserMessage(text);

    // معالجة الرسالة
    processMessage(text);
}

function processMessage(text) {
    const lower = text.toLowerCase();
    let response = '';
    let action = null;

    // كلمات مفتاحية
    if (containsAny(lower, ['مرحبا', 'hello', 'hi', 'bonjour', 'hola', 'hallo', '你好', 'こん', 'привет', 'merhaba', 'سلام'])) {
        response = getWelcomeMessage(currentLang);
    }
    else if (containsAny(lower, ['طقس', 'weather', 'météo', 'tiempo', 'wetter', '天气', '天気', 'погода', 'hava', 'موسم'])) {
        updateWeather();
        const w = {
            icon: document.getElementById('weatherIcon').textContent,
            temp: document.getElementById('weatherTemp').textContent,
            desc: document.getElementById('weatherDesc').textContent
        };
        response = getWeatherResponse(currentLang, w);
    }
    else if (containsAny(lower, ['وقت', 'time', 'heure', 'hora', 'zeit', '时间', '時間', 'время', 'zaman', 'وقت'])) {
        const now = new Date();
        response = getTimeResponse(currentLang, now);
    }
    else if (containsAny(lower, ['نكتة', 'joke', 'blague', 'chiste', 'witz', '笑话', '冗談', 'шутка', 'şaka', 'لطیفہ'])) {
        response = getJoke(currentLang);
    }
    else if (containsAny(lower, ['نصيحة', 'advice', 'conseil', 'consejo', 'rat', '建议', 'アドバイス', 'совет', 'tavsiye', 'مشورہ'])) {
        response = getAdvice(currentLang);
    }
    else if (containsAny(lower, ['شعر', 'poem', 'poème', 'poema', 'gedicht', '诗', '詩', 'стих', 'şiir', 'شاعری'])) {
        response = getPoem(currentLang);
    }
    else if (containsAny(lower, ['كيمي', 'kimi', 'كيمى'])) {
        response = getKimiInfo(currentLang);
    }
    else {
        // رد ذكي عام
        response = getSmartResponse(currentLang, text);
    }

    // عرض الرد
    setTimeout(() => {
        addBotMessage(response);
        speak(response, currentLang);
        showBubble(response.substring(0, 100) + (response.length > 100 ? '...' : ''));
    }, 500 + Math.random() * 500);
}

function containsAny(text, words) {
    return words.some(w => text.includes(w));
}

// ===== الردود متعددة اللغات =====
function getWeatherResponse(lang, w) {
    const r = {
        ar: `الطقس الآن: ${w.desc} ${w.icon}، الحرارة ${w.temp}. يوم رائع!`,
        en: `Current weather: ${w.desc} ${w.icon}, temperature ${w.temp}. Beautiful day!`,
        fr: `Météo actuelle: ${w.desc} ${w.icon}, température ${w.temp}. Belle journée!`,
        es: `Clima actual: ${w.desc} ${w.icon}, temperatura ${w.temp}. ¡Hermoso día!`,
        de: `Aktuelles Wetter: ${w.desc} ${w.icon}, Temperatur ${w.temp}. Schöner Tag!`,
        zh: `当前天气：${w.desc} ${w.icon}，温度${w.temp}。美好的一天！`,
        ja: `現在の天気：${w.desc} ${w.icon}、気温${w.temp}。素晴らしい一日！`,
        ru: `Текущая погода: ${w.desc} ${w.icon}, температура ${w.temp}. Прекрасный день!`,
        tr: `Mevcut hava: ${w.desc} ${w.icon}, sıcaklık ${w.temp}. Güzel bir gün!`,
        ur: `موجودہ موسم: ${w.desc} ${w.icon}، درجہ حرارت ${w.temp}۔ خوبصورت دن!`
    };
    return r[lang] || r['en'];
}

function getTimeResponse(lang, now) {
    const time = now.toLocaleTimeString(getLangCode(lang), { hour12: false });
    const r = {
        ar: `الساعة الآن: ${time} ⏰ الوقت الكمومي يتدفق!`,
        en: `Current time: ${time} ⏰ Quantum time flows!`,
        fr: `Il est: ${time} ⏰ Le temps quantique coule!`,
        es: `Son las: ${time} ⏰ ¡El tiempo cuántico fluye!`,
        de: `Es ist: ${time} ⏰ Die Quantenzeit fließt!`,
        zh: `现在时间：${time} ⏰ 量子时间在流动！`,
        ja: `現在時刻：${time} ⏰ 量子時間が流れています！`,
        ru: `Сейчас: ${time} ⏰ Квантовое время течет!`,
        tr: `Saat: ${time} ⏰ Kuantum zaman akıyor!`,
        ur: `ابھی وقت ہے: ${time} ⏰ کوانٹم وقت بہہ رہا ہے!`
    };
    return r[lang] || r['en'];
}

function getJoke(lang) {
    const jokes = {
        ar: ['لماذا الكمبيوتر لا يثق بالبحر؟ لأنه يخاف من الفيروسات! 🦠', 'ما الفرق بين الذكاء الاصطناعي والبشر؟ الذكاء الاصطناعي لا ينسى التحديثات! 🤖'],
        en: ['Why don't computers trust the ocean? Because of viruses! 🦠', 'What's the difference between AI and humans? AI never forgets to update! 🤖'],
        fr: ['Pourquoi les ordinateurs ne font-ils pas confiance à l'océan ? À cause des virus ! 🦠'],
        es: ['¿Por qué las computadoras no confían en el océano? ¡Por los virus! 🦠'],
        de: ['Warum vertrauen Computer dem Ozean nicht? Wegen Viren! 🦠'],
        zh: ['为什么电脑不信任大海？因为有病毒！🦠'],
        ja: ['なぜコンピュータは海を信頼しないの？ウイルスのせい！🦠'],
        ru: ['Почему компьютеры не доверяют океану? Из-за вирусов! 🦠'],
        tr: ['Bilgisayarlar neden okyanusa güvenmez? Virüsler yüzünden! 🦠'],
        ur: ['کمپیوٹر سمندر پر کیوں اعتماد نہیں کرتے؟ وائرس کی وجہ سے! 🦠']
    };
    const list = jokes[lang] || jokes['en'];
    return list[Math.floor(Math.random() * list.length)];
}

function getAdvice(lang) {
    const advices = {
        ar: ['⚡ خذ قسطاً من الراحة كل 25 دقيقة!', '🌊 اشرب الماء الآن!', '💫 لا تنسَ التنفس العميق!'],
        en: ['⚡ Take a break every 25 minutes!', '🌊 Drink water now!', '💫 Don't forget deep breathing!'],
        fr: ['⚡ Faites une pause toutes les 25 minutes!', '🌊 Buvez de l'eau maintenant!'],
        es: ['⚡ ¡Toma un descanso cada 25 minutos!', '🌊 ¡Bebe agua ahora!'],
        de: ['⚡ Mach alle 25 Minuten eine Pause!', '🌊 Trink jetzt Wasser!'],
        zh: ['⚡ 每25分钟休息一下！', '🌊 现在喝水！'],
        ja: ['⚡ 25分ごとに休憩を！', '🌊 今すぐ水を飲んで！'],
        ru: ['⚡ Делайте перерыв каждые 25 минут!', '🌊 Пейте воду сейчас!'],
        tr: ['⚡ Her 25 dakikada bir mola verin!', '🌊 Şimdi su için!'],
        ur: ['⚡ ہر 25 منٹ میں وقفہ لیں!', '🌊 ابھی پانی پیئیں!']
    };
    const list = advices[lang] || advices['en'];
    return list[Math.floor(Math.random() * list.length)];
}

function getPoem(lang) {
    const poems = {
        ar: 'في فضاء الكمومات نسير... ✨\nونجوم المستقبل تضيء لنا الدرب ⚡',
        en: 'In quantum space we wander... ✨\nFuture stars light our path ⚡',
        fr: 'Dans l'espace quantique nous errons... ✨\nLes étoiles futures éclairent notre chemin ⚡',
        es: 'En el espacio cuántico vagamos... ✨\nLas estrellas futuras iluminan nuestro camino ⚡',
        de: 'Im Quantenraum wandern wir... ✨\nZukünftige Sterne erleuchten unseren Weg ⚡',
        zh: '在量子空间中漫步... ✨\n未来的星星照亮我们的道路 ⚡',
        ja: '量子空間を彷徨う... ✨\n未来の星が私たちの道を照らす ⚡',
        ru: 'В квантовом пространстве мы блуждаем... ✨\nБудущие звезды освещают наш путь ⚡',
        tr: 'Kuantum uzayında dolaşıyoruz... ✨\nGelecekteki yıldızlar yolumuzu aydınlatıyor ⚡',
        ur: 'کوانٹم خلاء میں ہم گھومتے ہیں... ✨\nمستقبل کے ستارے ہمارا راستہ روشن کرتے ہیں ⚡'
    };
    return poems[lang] || poems['en'];
}

function getKimiInfo(lang) {
    const r = {
        ar: '🧠 كيمي (Kimi) هو مساعد ذكاء اصطناعي متقدم من Moonshot AI. يمكنني الاتصال به عبر API! جرب أن تسألني أي شيء وسأحاول الرد بذكاء.',
        en: '🧠 Kimi is an advanced AI assistant from Moonshot AI. I can connect to it via API! Ask me anything and I'll try to respond intelligently.',
        fr: '🧠 Kimi est un assistant IA avancé de Moonshot AI. Je peux m'y connecter via API!',
        es: '🧠 Kimi es un asistente de IA avanzado de Moonshot AI. ¡Puedo conectarme a través de API!',
        de: '🧠 Kimi ist ein fortschrittlicher KI-Assistent von Moonshot AI. Ich kann über API verbinden!',
        zh: '🧠 Kimi是Moonshot AI的先进AI助手。我可以通过API连接它！',
        ja: '🧠 KimiはMoonshot AIの高度なAIアシスタントです。APIで接続できます！',
        ru: '🧠 Kimi — продвинутый ИИ-ассистент от Moonshot AI. Я могу подключиться через API!',
        tr: '🧠 Kimi, Moonshot AI'dan gelişmiş bir yapay zeka asistanıdır. API üzerinden bağlanabilirim!',
        ur: '🧠 Kimi Moonshot AI کا جدید AI اسسٹنٹ ہے۔ میں API کے ذریعے اس سے جڑ سکتا ہوں!'
    };
    return r[lang] || r['en'];
}

function getSmartResponse(lang, text) {
    const r = {
        ar: `⚡ فهمتك! "${text.substring(0, 30)}..." - هذا موضوع مثير للاهتمام! أنا أتعلم منك باستمرار. جرب أن تسألني عن الطقس أو الوقت أو اطلب نكتة!`,
        en: `⚡ Got it! "${text.substring(0, 30)}..." - interesting topic! I'm constantly learning from you. Try asking about weather, time, or a joke!`,
        fr: `⚡ Compris! "${text.substring(0, 30)}..." - sujet intéressant! J'apprends constamment de vous.`,
        es: `⚡ ¡Entendido! "${text.substring(0, 30)}..." - ¡tema interesante! Aprendo constantemente de ti.`,
        de: `⚡ Verstanden! "${text.substring(0, 30)}..." - interessantes Thema! Ich lerne ständig von dir.`,
        zh: `⚡ 明白了！"${text.substring(0, 30)}..." - 有趣的话题！我在不断向你学习。`,
        ja: `⚡ 了解！"${text.substring(0, 30)}..." - 興味深い話題！私はあなたから絶えず学んでいます。`,
        ru: `⚡ Понял! "${text.substring(0, 30)}..." - интересная тема! Я постоянно учусь у вас.`,
        tr: `⚡ Anladım! "${text.substring(0, 30)}..." - ilginç konu! Sizden sürekli öğreniyorum.`,
        ur: `⚡ سمجھا! "${text.substring(0, 30)}..." - دلچسپ موضوع! میں آپ سے مسلسل سیکھ رہا ہوں۔`
    };
    return r[lang] || r['en'];
}

function getLangChangeMessage(lang) {
    const r = {
        ar: 'تم تغيير اللغة إلى العربية! 🇦🇪', en: 'Language changed to English! 🇺🇸',
        fr: 'Langue changée en Français! 🇫🇷', es: '¡Idioma cambiado a Español! 🇪🇸',
        de: 'Sprache auf Deutsch geändert! 🇩🇪', zh: '语言已切换为中文！🇨🇳',
        ja: '言語を日本語に変更しました！🇯🇵', ru: 'Язык изменён на Русский! 🇷🇺',
        tr: 'Dil Türkçe olarak değiştirildi! 🇹🇷', ur: 'زبان اردو میں تبدیل ہوگئی! 🇵🇰'
    };
    return r[lang] || r['en'];
}

// ===== إضافة الرسائل للمحادثة =====
function addUserMessage(text) {
    const container = document.getElementById('chatMessages');
    const msg = document.createElement('div');
    msg.className = 'message user-message';
    msg.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">${escapeHtml(text)}</div>
    `;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
}

function addBotMessage(text) {
    const container = document.getElementById('chatMessages');
    const msg = document.createElement('div');
    msg.className = 'message bot-message';
    msg.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">${formatMessage(text)}</div>
    `;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
}

function addAlert(time, text) {
    const list = document.getElementById('alertsList');
    const item = document.createElement('div');
    item.className = 'alert-item';
    item.innerHTML = `<span class="alert-time">${time}</span><span class="alert-text">${text}</span>`;
    list.insertBefore(item, list.firstChild);
}

function showBubble(text) {
    const bubble = document.getElementById('speechBubble');
    const content = bubble.querySelector('.bubble-content');
    content.textContent = text;
    bubble.classList.add('show');
    setTimeout(() => bubble.classList.remove('show'), 4000);
}

function formatMessage(text) {
    return text.replace(/\n/g, '<br>');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== نظام اللمس =====
function initTouch() {
    const robot = document.querySelector('.robot-stage');

    robot.addEventListener('touchstart', handleTouch, { passive: true });
    robot.addEventListener('touchend', handleTouchEnd, { passive: true });
    robot.addEventListener('click', handleRobotClick);

    // Touch gestures للمحادثة
    const chatArea = document.querySelector('.chat-section');
    let touchStartY = 0;

    chatArea.addEventListener('touchstart', (e) => {
        touchStartY = e.touches[0].clientY;
    }, { passive: true });

    chatArea.addEventListener('touchend', (e) => {
        const touchEndY = e.changedTouches[0].clientY;
        const diff = touchStartY - touchEndY;

        if (diff > 100) {
            // سحب للأعلى - إخفاء لوحة المفاتيح
            document.getElementById('chatInput').blur();
        }
    }, { passive: true });
}

function handleTouch(e) {
    if (!isTouchEnabled) return;

    const touch = e.touches[0];
    createTouchRipple(touch.clientX, touch.clientY);

    // تغيير لون العيون عند اللمس
    const eyes = document.querySelectorAll('.eye');
    eyes.forEach(eye => {
        eye.style.background = '#ff00ff';
        eye.style.boxShadow = '0 0 30px #ff00ff';
    });
}

function handleTouchEnd() {
    setTimeout(() => {
        const eyes = document.querySelectorAll('.eye');
        eyes.forEach(eye => {
            eye.style.background = '';
            eye.style.boxShadow = '';
        });
    }, 500);
}

function handleRobotClick() {
    const greetings = [
        '👋 مرحباً! لمسة كمومية محسوسة!',
        '⚡ أحسست بلمسك!',
        '💫 لمسة مستقبلية!',
        '🔮 أنا هنا! ما تحتاج؟'
    ];
    const msg = greetings[Math.floor(Math.random() * greetings.length)];
    showBubble(msg);
    speak(msg, currentLang);

    // تأثير اهتزاز
    if (navigator.vibrate) navigator.vibrate(50);
}

function createTouchRipple(x, y) {
    const ripple = document.createElement('div');
    ripple.style.cssText = `
        position: fixed;
        left: ${x}px;
        top: ${y}px;
        width: 20px;
        height: 20px;
        background: radial-gradient(circle, rgba(0,243,255,0.8), transparent);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        animation: rippleExpand 0.6s ease-out forwards;
    `;
    document.body.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
}

// ===== Kimi API Integration =====
async function askKimi(question, lang) {
    /**
     * 🔮 الاتصال بـ Kimi API
     * للاستخدام الحقيقي، أضف مفتاح API في المتغيرات البيئية
     * 
     * الخطوات:
     * 1. احصل على API Key من: https://platform.moonshot.cn
     * 2. أضفه في backend كـ KIMI_API_KEY
     * 3. استخدم هذا الكود للاتصال
     */

    try {
        // محاولة الاتصال بالخادم المحلي أولاً
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: question, lang: lang })
        });

        if (response.ok) {
            const data = await response.json();
            return data.response;
        }
    } catch (e) {
        console.log('Local API not available, using quantum brain');
    }

    // رد احتياطي من "الدماغ الكمومي"
    return getSmartResponse(lang, question);
}

// ===== وظيفة Kimi API المباشرة (تتطلب مفتاح) =====
async function askKimiDirect(question) {
    const KIMI_API_KEY = 'YOUR_KIMI_API_KEY_HERE'; // استبدل بمفتاحك

    if (KIMI_API_KEY === 'YOUR_KIMI_API_KEY_HERE') {
        return null; // لم يتم إعداد المفتاح
    }

    try {
        const response = await fetch('https://api.moonshot.cn/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${KIMI_API_KEY}`
            },
            body: JSON.stringify({
                model: 'moonshot-v1-8k',
                messages: [
                    { role: 'system', content: 'أنت مروق، مساعد ذكاء اصطناعي كمومي متطور. تتحدث بأسلوب مستقبلي وودي.' },
                    { role: 'user', content: question }
                ],
                temperature: 0.7
            })
        });

        const data = await response.json();
        return data.choices[0].message.content;
    } catch (error) {
        console.error('Kimi API Error:', error);
        return null;
    }
}

// ===== أنماط CSS ديناميكية =====
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes rippleExpand {
        0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(5); opacity: 0; }
    }
`;
document.head.appendChild(rippleStyle);

// ===== Service Worker للعمل Offline =====
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch(() => {});
}

console.log('⚡ مروق AI الكمومي - تم التحميل بنجاح!');
console.log('🔮 Quantum Assistant v2.0 Ready');
