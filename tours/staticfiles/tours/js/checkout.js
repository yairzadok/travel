window.addEventListener("DOMContentLoaded", () => {
  const coupons = {
    TRAVEL10: 10,
    SUMMER20: 20,
    VIP30: 30
  };

  const priceDisplay = document.getElementById('price-amount');
  const messageBox = document.getElementById('coupon-message');
  const iframe = document.querySelector('iframe');
  const basePrice = parseFloat(priceDisplay.innerText.replace(/[^\d.]/g, ''));
  let currentDiscount = 0;

  window.applyCoupon = function () {
    const code = document.getElementById('coupon-code').value.trim().toUpperCase();

    if (coupons[code]) {
      currentDiscount = coupons[code];
      const discounted = basePrice - (basePrice * currentDiscount) / 100;
      priceDisplay.innerText = `₪${discounted.toFixed(2)}`;
      messageBox.innerText = `קוד קופון הופעל (${currentDiscount}% הנחה)!`;
      messageBox.className = 'form-text text-success mt-1';
      iframe.src = `https://direct.tranzila.com/fxpyairzadok/iframenew.php?sum=${discounted.toFixed(2)}`;
    } else {
      currentDiscount = 0;
      priceDisplay.innerText = `₪${basePrice.toFixed(2)}`;
      messageBox.innerText = 'קוד הקופון אינו תקף.';
      messageBox.className = 'form-text text-danger mt-1';
      iframe.src = `https://direct.tranzila.com/fxpyairzadok/iframenew.php?sum=${basePrice.toFixed(2)}`;
    }
  };
});
