document.getElementById('payment-form').addEventListener('submit', function(e) {
  e.preventDefault(); // Prevents the page from refreshing

  const cardNumber = document.getElementById('card-number').value;

  // Basic Validation Check
  if (cardNumber.length < 16) {
    alert("Please enter a valid 16-digit card number.");
    return;
  }

  // Visual feedback for the user
  const btn = document.querySelector('.place-order');
  btn.innerText = "Processing...";
  btn.disabled = true;

  // In a real app, you would send this data to a payment processor here
  setTimeout(() => {
    alert("Payment of $45.00 Successful! Your order is being prepared.");
    window.location.href = "order-success.html";
  }, 2000);
});