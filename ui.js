/**
 * مروق ايكو الخارق - سكربتات واجهة المستخدم
 * Mrook Echo - UI JavaScript
 */

// === المتغيرات العامة ===
let currentTime = 0;
let currentEnergy = 0;
let isDarkMode = false;

// === DOM Elements ===
const timeInput = document.getElementById('timeInput');
const energyInput = document.getElementById('energyInput');
const timeProgress = document.getElementById('timeProgress');
const batteryLevel = document.getElementById('batteryLevel');
const energyPercent = document.getElementById('energyPercent');
const updateTimeBtn = document.getElementById('updateTimeBtn');
const updateEnergyBtn = document.getElementById('updateEnergyBtn');
const statusText = document.getElementById('statusText');
const statusIndicator = document.getElementById('statusIndicator');
const statTime = document.getElementById('statTime');
const statEnergy = document.getElementById('statEnergy');
const statStatus = document.getElementById('statStatus');
const themeBtn = document.getElementById('themeBtn');
const toastContainer = document.getElementById('toastContainer');

// === التهيئة ===
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    setupEventListeners();
    updateStatus('جاهز للاستخدام', 'ready');
});

// === مستمعي الأحداث ===
function setupEventListeners() {
    updateTimeBtn.addEventListener('click', updateTime);
    updateEnergyBtn.addEventListener('click', updateEnergy);
    themeBtn.addEventListener('click', toggleTheme);

    // التحقق من الإدخال
    timeInput.addEventListener('input', (e) => {
        if (e.target.value < 0) e.target.value = 0;
    });

    energyInput.addEventListener('input', (e) => {
        if (e.target.value < 0) e.target.value = 0;
        if (e.target.value > 100) e.target.value = 100;
    });

    // دعم Enter
    timeInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') updateTime();
    });

    energyInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') updateEnergy();
    });
}

// === تحديث الوقت ===
function updateTime() {
    const value = parseInt(timeInput.value);

    if (isNaN(value) || value === '') {
        showToast('⚠️ يرجى إدخال قيمة صحيحة للوقت', 'warning');
        return;
    }

    if (value < 0) {
        showToast('❌ الوقت لا يمكن أن يكون سالباً', 'error');
        return;
    }

    currentTime = value;

    // تحديث شريط التقدم
    const maxTime = 1440; // 24 ساعة
    const percent = Math.min((value / maxTime) * 100, 100);
    timeProgress.style.width = percent + '%';

    // تحديث الإحصائيات
    statTime.textContent = value;

    updateStatus(`✅ تم تحديث الوقت: ${value} دقيقة`, 'ready');
    showToast(`⏱️ تم تحديث الوقت إلى ${value} دقيقة`, 'success');

    saveSettings();
}

// === تحديث الطاقة ===
function updateEnergy() {
    const value = parseInt(energyInput.value);

    if (isNaN(value) || energyInput.value === '') {
        showToast('⚠️ يرجى إدخال قيمة صحيحة للطاقة', 'warning');
        return;
    }

    if (value < 0 || value > 100) {
        showToast('❌ الطاقة يجب أن تكون بين 0 و 100', 'error');
        return;
    }

    currentEnergy = value;

    // تحديث البطارية
    batteryLevel.style.width = value + '%';
    energyPercent.textContent = value + '%';

    // تغيير لون البطارية حسب المستوى
    if (value > 60) {
        batteryLevel.style.background = 'linear-gradient(90deg, #38a169, #48bb78)';
    } else if (value > 30) {
        batteryLevel.style.background = 'linear-gradient(90deg, #d69e2e, #ecc94b)';
    } else {
        batteryLevel.style.background = 'linear-gradient(90deg, #e53e3e, #fc8181)';
    }

    // تحديث الإحصائيات
    statEnergy.textContent = value + '%';

    updateStatus(`✅ تم تحديث الطاقة: ${value}%`, 'ready');
    showToast(`🔋 تم تحديث الطاقة إلى ${value}%`, 'success');

    saveSettings();
}

// === الوضع الليلي ===
function toggleTheme() {
    isDarkMode = !isDarkMode;
    document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
    themeBtn.textContent = isDarkMode ? '☀️' : '🌙';
    showToast(isDarkMode ? '🌙 تم تفعيل الوضع الليلي' : '☀️ تم تفعيل الوضع النهاري', 'success');
    saveSettings();
}

// === شريط الحالة ===
function updateStatus(message, state) {
    statusText.textContent = message;

    const colors = {
        ready: '#48bb78',
        busy: '#ed8936',
        error: '#f56565'
    };

    statusIndicator.style.color = colors[state] || colors.ready;
}

// === الإشعارات ===
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span>${type === 'success' ? '✅' : type === 'error' ? '❌' : type === 'warning' ? '⚠️' : 'ℹ️'}</span>
        <span>${message}</span>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// === حفظ الإعدادات ===
function saveSettings() {
    const settings = {
        time: currentTime,
        energy: currentEnergy,
        darkMode: isDarkMode,
        lastUpdated: new Date().toISOString()
    };

    localStorage.setItem('mrookEchoSettings', JSON.stringify(settings));
}

// === تحميل الإعدادات ===
function loadSettings() {
    const saved = localStorage.getItem('mrookEchoSettings');
    if (saved) {
        try {
            const settings = JSON.parse(saved);
            currentTime = settings.time || 0;
            currentEnergy = settings.energy || 0;
            isDarkMode = settings.darkMode || false;

            timeInput.value = currentTime || '';
            energyInput.value = currentEnergy || '';

            if (isDarkMode) {
                document.documentElement.setAttribute('data-theme', 'dark');
                themeBtn.textContent = '☀️';
            }

            // تحديث الواجهة
            if (currentTime > 0) updateTime();
            if (currentEnergy > 0) updateEnergy();

        } catch (e) {
            console.error('Error loading settings:', e);
        }
    }
}

// === تصدير ===
window.MrookEcho = {
    updateTime,
    updateEnergy,
    toggleTheme,
    showToast
};
