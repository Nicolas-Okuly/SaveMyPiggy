// Get the modal element, the button to open the modal, and the close button
var modal = document.getElementsByClassName("transaction-modal")[0]; // Select the modal by class name
var btn = document.getElementById("modal-open"); // Select the button to open the modal by ID
var span = document.getElementsByClassName("close")[0]; // Select the close button (X) inside the modal by class name

// When the "open modal" button is clicked, display the modal
btn.onclick = function() {
    modal.style.display = "block"; // Set the display of the modal to block to make it visible
}

// When the close button (X) is clicked, hide the modal
span.onclick = function() {
    modal.style.display = "none"; // Set the display of the modal to none to hide it
}

// Function to manually open the modal (for reuse)
function openModal() {
    modal.style.display = "block"; // Display the modal
}

// When the user clicks anywhere outside the modal, close it
window.onclick = function(event) {
    if (event.target == modal) // If the click is on the modal itself (not inside)
        modal.style.display = "none"; // Hide the modal
}