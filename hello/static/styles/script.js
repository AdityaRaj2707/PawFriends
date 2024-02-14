let cartCount = 0; // Counter to keep track of number of items in cart
let cartItems = []; // Array to store cart items
const cartCountElement = document.querySelector('.cart-count');
const cartListElement = document.querySelector('.cart-items');
const cartTotalElement = document.querySelector('.cart-total');

function addToCart(itemName, itemPrice) {
  cartCount++;
  cartCountElement.innerHTML = cartCount;
  cartItems.push({
    name: itemName,
    price: itemPrice
  });
  displayCartItems();
}

function displayCartItems() {
  if (!cartListElement) return; // Exit function if cartListElement is null

  cartListElement.innerHTML = ''; // Clear the list

  let totalPrice = 0; // Initialize total price variable

  // Add each item to the list
  cartItems.forEach((item) => {
    const listItem = document.createElement('li');
    listItem.innerHTML = `${item.name} - ₹${item.price}`;
    cartListElement.appendChild(listItem);
    totalPrice += parseFloat(item.price); // Add item price to total price
  });

  // Display total price at the bottom of the cart
  cartTotalElement.innerHTML = `Total Price: ₹${totalPrice}`;
}


window.addEventListener('DOMContentLoaded', () => {
  const addButtons = document.querySelectorAll('.add-btn');

  addButtons.forEach(button => {
    button.addEventListener('click', () => {
      const itemName = button.dataset.item;
      const itemPrice = button.dataset.price;
      addToCart(itemName, itemPrice);
    });
  });
});
