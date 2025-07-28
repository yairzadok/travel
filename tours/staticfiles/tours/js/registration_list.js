document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("searchInput");
    if (!input) return;

    input.addEventListener("input", function () {
        const searchValue = input.value.toLowerCase();
        const rows = document.querySelectorAll("tbody tr");

        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(searchValue) ? "" : "none";
        });
    });
});
