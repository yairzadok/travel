function toggleMenu() {
    const modal = document.getElementById("aboutModal");
    const content = document.getElementById("aboutModalContent");

    content.innerHTML = `
        <h2 style="text-align: center; color: #0072ff; margin-bottom: 20px;">בחר אפשרות</h2>
        <div style="
            display: flex;
            flex-direction: column;
            gap: 15px;
            align-items: stretch;
            animation: fadeIn 0.4s ease-in-out;
        ">
            <button class="menu-btn btn btn-outline-primary d-flex align-items-center justify-content-start" onclick="showAbout()">
                <i class="bi bi-person-badge me-2"></i> ד"ר יאיר צדוק – מרצה ומורה דרך
            </button>
            <button class="menu-btn btn btn-outline-secondary d-flex align-items-center justify-content-start" onclick="showContact()">
                <i class="bi bi-envelope me-2"></i> צור קשר
            </button>
        </div>
    `;
    modal.style.display = "block";
}

function showAbout() {
    document.getElementById("aboutModalContent").innerHTML = `
        <h2>ד"ר יאיר צדוק – מרצה ומורה דרך</h2>
        <p>
            כמורה דרך מוסמך, אני עוסק בהובלת סיורים, ערכיים וחווייתיים ברחבי הארץ, תוך שילוב בין ידע היסטורי, גיאוגרפי, תרבותי ופדגוגי.<br><br>
            הסיורים אותם אני בונה ומדריך מבוססים על עקרונות של למידה פעילה, ומטרתם לחבר בין הלמידה לבין המציאות בשטח – באמצעות סיפור, חוויה, דיאלוג וחקירה.<br><br>
            אני מתמחה בליווי קבוצות מגוונות – סטודנטים, חיילים, סגלי חינוך ובעלי עניין מהציבור הרחב – ומתאים את התוכן וההובלה לקהל היעד, לרמת הידע שלו ולערכים שהוא מבקש לקדם.
        </p>
    `;
}

function showContact() {
    document.getElementById("aboutModalContent").innerHTML = `
        <h2>צור קשר</h2>
        <p>
            ד"ר יאיר צדוק<br>
            טלפון: <a href="tel:0528876688">052-8876688</a><br>
            מייל: <a href="mailto:yair6655@gmail.com">yair6655@gmail.com</a>
        </p>
    `;
}

function closeModal() {
    const modal = document.getElementById("aboutModal");
    if (modal) {
        modal.style.display = "none";
    }
}

window.onclick = function(event) {
    const modal = document.getElementById("aboutModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
