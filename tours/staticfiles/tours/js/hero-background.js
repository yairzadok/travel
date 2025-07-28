document.addEventListener("DOMContentLoaded", function () {
  const backgrounds = document.querySelectorAll('.hero-bg');
  let current = 0;

  function cycleBackgrounds() {
    backgrounds.forEach((bg, index) => {
      bg.classList.remove('active');
      if (index === current) {
        bg.classList.add('active');
      }
    });
    current = (current + 1) % backgrounds.length;
  }

  if (backgrounds.length > 0) {
    cycleBackgrounds(); // הצגה ראשונה
    setInterval(cycleBackgrounds, 6000); // כל 6 שניות
  }
});
document.addEventListener("DOMContentLoaded", function () {
  const sentences = [
    "מגוון רחב של סיורים מודרכים ברחבי הארץ – בעברית ובאנגלית",
    "סיורים קבוצתיים או מותאמים אישית",
    "הסיורים מתקיימים בשעות מגוונות לאורך כל ימות השנה",
    "מותאמים לעונות ולחגי ישראל",
    "חיבור ייחודי בין היסטוריה, תרבות וסיפור מקומי.",
    "בואו לגלות את הארץ מזווית אחרת – עם מדריכים מקצועיים ואוהבי אדם."
  ];

  const target = document.getElementById("animated-sentences");
  let index = 0;

  function showNextSentence() {
    target.classList.remove("fade-in");
    void target.offsetWidth; // טריק כדי לאפס את האנימציה
    target.textContent = sentences[index];
    target.classList.add("fade-in");
    index = (index + 1) % sentences.length;
  }

  showNextSentence(); // הצג את הראשון
  setInterval(showNextSentence, 4000); // כל 4 שניות
});
