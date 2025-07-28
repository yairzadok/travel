let html5QrCode;
let scannedIds = new Set();
let scannerActive = false;

function startScanner() {
    const reader = document.getElementById('reader');
    const scanBtn = document.querySelector('.btn-scan');

    if (scannerActive) {
        html5QrCode.stop().then(() => {
            reader.style.display = 'none';
            scanBtn.innerText = '📷 התחל סריקה';
            scannerActive = false;
        }).catch(err => console.error("שגיאה בהפסקת סריקה", err));
        return;
    }

    reader.style.display = 'block';
    scanBtn.innerText = '🛑 עצור סריקה';

    html5QrCode = new Html5Qrcode("reader");

    html5QrCode.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: { width: 250, height: 250 } },
        qrCodeMessage => {
            if (scannedIds.has(qrCodeMessage)) return;

            const input = document.getElementById("presence_" + qrCodeMessage);
            if (input) {
                input.checked = true;
                updateAttendance(input.id.split('_')[1], true);
                input.closest('.participant-row')?.classList.add('present');
                document.getElementById('beep-sound').play();
                showToast('✅ נוכחות עודכנה בהצלחה', 'success');
                scannedIds.add(qrCodeMessage);
                updateAttendanceCounter();
            } else {
                showToast('⚠️ לא נמצא משתתף מתאים', 'warning');
            }
        },
        error => {}
    ).then(() => {
        scannerActive = true;
    }).catch(err => {
        showToast("🚫 שגיאה בהפעלת מצלמה", 'danger');
    });
}

function updateAttendance(registrationId, isPresent) {
    fetch("/update_presence/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `id=${registrationId}&present=${isPresent}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const card = document.getElementById('card_' + registrationId);
            if (card) {
                card.classList.toggle('present', isPresent);
            }
            updateAttendanceCounter();
        }
    });
}

function clearAllPresence() {
    if (confirm("האם אתה בטוח שברצונך לנקות את כל הסימונים?")) {
        document.querySelectorAll('input[type="checkbox"]').forEach(input => {
            input.checked = false;
            updateAttendance(input.id.split('_')[1], false);
        });
        document.querySelectorAll('.participant-row').forEach(card => {
            card.classList.remove('present');
        });
        updateAttendanceCounter();
    }
}

function sendParticipantsByEmail() {
    const now = new Date();
    const timestamp = now.toLocaleString('he-IL');
    const rows = document.querySelectorAll('.participant-row');

    if (rows.length === 0) {
        showToast("אין משתתפים לשליחה", 'warning');
        return;
    }

    let bodyText = `דו״ח נוכחות - ${timestamp}\n\nשם מלא | טלפון | נוכחות\n-----------------------------\n`;

    rows.forEach(row => {
        const name = row.querySelector('strong')?.innerText || '';
        const phone = row.querySelector('small')?.innerText || '';
        const checked = row.querySelector('input[type="checkbox"]').checked;
        const status = checked ? "✅ נוכח" : "❌ לא נוכח";
        bodyText += `${name} | ${phone} | ${status}\n`;
    });

    const subject = `דו״ח נוכחות - ${timestamp}`;
    window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(bodyText)}`;
}

function showToast(message, type='primary') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${type} border-0 show`;
    toast.role = 'alert';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>`;
    document.querySelector('.toast-container').appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

function updateAttendanceCounter() {
    const total = document.querySelectorAll('.participant-row').length;
    const present = document.querySelectorAll('.participant-row input[type="checkbox"]:checked').length;
    document.getElementById('attendance-counter').innerText = `נוכחים: ${present} / ${total}`;
}

function getCookie(name) {
    const cookies = document.cookie.split(';').map(c => c.trim());
    for (let cookie of cookies) {
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.split('=')[1]);
        }
    }
    return null;
}
