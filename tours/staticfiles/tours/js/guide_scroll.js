
function scrollGuides(direction) {
  const container = document.getElementById('guideScrollContainer');
  const scrollAmount = 400;
  container.scrollBy({
    left: direction * scrollAmount,
    behavior: 'smooth'
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById('guideScrollContainer');
  let autoScrollInterval = setInterval(() => scrollGuides(1), 3000);

  container.addEventListener('mouseover', () => clearInterval(autoScrollInterval));
  container.addEventListener('mouseleave', () => {
    autoScrollInterval = setInterval(() => scrollGuides(1), 3000);
  });
});
