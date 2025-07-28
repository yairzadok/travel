document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".container");
    const totalCostDiv = document.getElementById("total-cost");
    const finalTotalDiv = document.getElementById("final-total");

    const pricePerPersonRaw = container?.dataset.pricePerPerson || "0";
    const numParticipantsRaw = container?.dataset.numParticipants || "1";

    const pricePerPerson = parseFloat(pricePerPersonRaw);
    const qty = parseInt(numParticipantsRaw);

    const total = (pricePerPerson * qty).toFixed(2);

    if (totalCostDiv) totalCostDiv.innerHTML += ` <strong>${total} ₪</strong>`;
    if (finalTotalDiv) finalTotalDiv.textContent = '💸 סה"כ לתשלום: ' + total + ' ₪';
});

document.querySelector("form[method='post']").addEventListener("submit", function (e) {
    const inputs = this.querySelectorAll("input[required]");
    for (const input of inputs) {
        if (!input.checkValidity()) {
            input.classList.add("is-invalid");
            e.preventDefault();
        } else {
            input.classList.remove("is-invalid");
        }
    }
});