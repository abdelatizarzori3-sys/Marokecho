/* ⚡ مروق AI الكمومي v3.0 — Universal Frontend */
(function() {
    "use strict";

    const API_URL = window.location.origin;  // يعمل تلقائياً على أي IP:PORT
    let currentLang = "ar";
    let isSpeaking = false;

    // ─── العناصر ──────────────────────────────
    function $(sel) { return document.querySelector(sel); }
    function $$(sel) { return document.querySelectorAll(sel); }

    const chatMessages = $("#chatMessages");
    const chatInput = $("#chatInput");
    const sendBtn = $("#sendBtn");
    const micBtn = $("#micBtn");
    const typingIndicator = $("#typingIndicator");
    const langSelect = $("#langSelect");
    const onlineStatus = $("#onlineStatus");
    const timerEl = $("#timer");
    const quantumScore = $("#quantumScore");
    const speakBtn = $("#speakBtn");

    // ─── المؤقت ───────────────────────────────
    let seconds = 0;
    setInterval(() => {
        seconds++;
        const h = String(Math.floor(seconds / 3600)).padStart(2, "0");
        const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, "0");
        const s = String(seconds % 60).padStart(2, "0");
        if (timerEl) timerEl.textContent = `${h}:${m}:${s}`;
    }, 1000);

    // ─── حالة الاتصال ─────────────────────────
    async function checkStatus() {
        try {
            const r = await fetch(`${API_URL}/api/status`, {method: "GET"});
            const data = await r.json();
            if (onlineStatus) {
                onlineStatus.textContent = data.status === "online" ? "🟢 ONLINE" : "🔴 OFFLINE";
            }
            if (quantumScore && data.memory) {
                quantumScore.textContent = `Q-${(data.memory.coherence * 10000).toFixed(2)} ⚡`;
            }
        } catch (e) {
            if (onlineStatus) onlineStatus.textContent = "🔴 OFFLINE";
        }
    }
    checkStatus();
    setInterval(checkStatus, 10000);

    // ─── إضافة رسالة ──────────────────────────
    function addMessage(text, role = "assistant", engine = "") {
        if (!chatMessages) return;
        const wrapper = document.createElement("div");
        wrapper.className = "msg-wrapper " + role;

        const avatar = document.createElement("div");
        avatar.className = "msg-avatar";
        avatar.textContent = role === "user" ? "👤" : "🔮";

        const bubble = document.createElement("div");
        bubble.className = "msg-bubble " + role;

        const p = document.createElement("p");
        p.textContent = text;
        bubble.appendChild(p);

        if (engine) {
            const badge = document.createElement("span");
            badge.className = "engine-badge";
            badge.textContent = engine;
            bubble.appendChild(badge);
        }

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);
        chatMessages.appendChild(wrapper);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // ─── إرسال رسالة ──────────────────────────
    async function sendMessage() {
        const text = chatInput ? chatInput.value.trim() : "";
        if (!text) return;

        addMessage(text, "user");
        if (chatInput) chatInput.value = "";
        if (typingIndicator) typingIndicator.style.display = "flex";

        try {
            const r = await fetch(`${API_URL}/api/chat`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: text, lang: currentLang, engine: "gemini"})
            });
            const data = await r.json();
            if (typingIndicator) typingIndicator.style.display = "none";

            if (data.reply) {
                addMessage(data.reply, "assistant", data.engine);
                if (isSpeaking && "speechSynthesis" in window) {
                    const utter = new SpeechSynthesisUtterance(data.reply);
                    utter.lang = currentLang === "ar" ? "ar-SA" : "en-US";
                    window.speechSynthesis.speak(utter);
                }
            } else {
                addMessage("عذراً، حدث خطأ في الرد.", "assistant");
            }
        } catch (e) {
            if (typingIndicator) typingIndicator.style.display = "none";
            addMessage("❌ الخادم غير متصل! تأكد من تشغيل run.sh", "assistant");
        }
    }

    // ─── أحداث ────────────────────────────────
    if (sendBtn) sendBtn.addEventListener("click", sendMessage);
    if (chatInput) {
        chatInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") sendMessage();
        });
    }

    if (langSelect) {
        langSelect.addEventListener("change", (e) => {
            currentLang = e.target.value;
        });
    }

    if (speakBtn) {
        speakBtn.addEventListener("click", () => {
            isSpeaking = !isSpeaking;
            speakBtn.textContent = isSpeaking ? "🔊" : "🔇";
            speakBtn.title = isSpeaking ? "التشغيل الصوتي مفعل" : "التشغيل الصوتي معطل";
        });
    }

    if (micBtn) {
        micBtn.addEventListener("click", () => {
            if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
                const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
                const rec = new SR();
                rec.lang = currentLang === "ar" ? "ar-SA" : "en-US";
                rec.onresult = (e) => {
                    const txt = e.results[0][0].transcript;
                    if (chatInput) chatInput.value = txt;
                    sendMessage();
                };
                rec.start();
                micBtn.textContent = "🎙️";
                setTimeout(() => { micBtn.textContent = "🎤"; }, 3000);
            } else {
                alert("المتصفح لا يدعم التعرف على الصوت");
            }
        });
    }

    // ─── محاكاة الطقس ─────────────────────────
    function loadWeather() {
        const loading = $("#weatherLoading");
        if (loading) loading.style.display = "none";

        const temp = $("#temp");
        const humidity = $("#humidity");
        const visibility = $("#visibility");
        const wind = $("#wind");

        if (temp) temp.textContent = Math.floor(20 + Math.random() * 15) + "°C";
        if (humidity) humidity.textContent = Math.floor(30 + Math.random() * 50) + "%";
        if (visibility) visibility.textContent = Math.floor(5 + Math.random() * 10) + " كم";
        if (wind) wind.textContent = Math.floor(5 + Math.random() * 20) + " كم/س";
    }
    setTimeout(loadWeather, 1500);

    console.log("⚡ مروق AI v3.0 — محمل بنجاح!");
})();
