document.getElementById('payment-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const cardNumber = document.getElementById('card-number').value;

  if (cardNumber.length < 16) {
    alert("Please enter a valid 16-digit card number.");
    return;
  }

  const btn = document.querySelector('.place-order');
  btn.innerText = "Processing...";
  btn.disabled = true;

  setTimeout(() => {
    alert("Payment of $45.00 Successful! Your order is being prepared.");
    window.location.href = "order-success.html";
  }, 2000);

});