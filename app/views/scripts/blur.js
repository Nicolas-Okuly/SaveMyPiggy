let toggle = false; // Tracks whether the blur effect is active (true) or not (false)
let oldValue = []   // Stores the original colors of the money elements to restore after unblurring

/*
    This function blurs anything that is money when toggled to protect user privacy.
*/
function blurAll() {
    if (!toggle) {
        /* Blur anything sensitive and save the color */
        let moneyItems = document.getElementsByClassName("money"); // Selects all elements with the class "money"

        for (let i = 0; i < moneyItems.length; i++) {
            // Saves the current color of the element before applying the blur
            oldValue.push(`${getComputedStyle(moneyItems[i]).color}`);
            
            // Applies the blur effect and sets the color to black
            moneyItems[i].style.filter = "blur(15px)";
            moneyItems[i].style.color = "#000000";
        }

        toggle = true; // Sets the toggle to true, indicating the blur is active
        document.getElementById("blurBtn").src = "./icons/eye.svg"; // Changes the button image to indicate blur is on
    } else {
        /* Un-blur and restore colors */
        let moneyItems = document.getElementsByClassName("money"); // Selects all elements with the class "money"

        for (let i = 0; i < moneyItems.length; i++) {
            // Removes the blur effect and restores the original color
            moneyItems[i].style.filter = "blur(0px)";
            moneyItems[i].style.color = oldValue[i];
        }

        oldValue = []; // Clears the old color values array
        toggle = false; // Sets the toggle to false, indicating the blur is no longer active
        document.getElementById("blurBtn").src = "./icons/eye-slash.svg"; // Changes the button image to indicate blur is off
    }
}