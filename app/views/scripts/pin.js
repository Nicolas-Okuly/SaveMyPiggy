// Declare communication objects for interacting with the backend
let setPin;
let getPin;
let gotPin;

// Create a Proxy object to handle URL search parameters
const CheckableParams = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop), // Return the value of a search parameter
});


// Create a new QWebChannel to interact with the Qt backend
new QWebChannel(qt.webChannelTransport, (channel) => {
    // Initialize the communication objects for setting and getting the PIN
    setPin = channel.objects.setPin;
    getPin = channel.objects.getPin;

    // If the URL has a newpin parameter, set the new PIN and redirect
    if (CheckableParams.newpin) {
        setPin.receiveNewPin(CheckableParams.newpin); // Send the new pin to the backend
        window.location = "pin.html"; // Redirect to the PIN page
        return;
    }

    // Listen for the PIN data from the backend
    getPin.sendPinData.connect(async (message) => {
        if(message == 0) return handleNoPin(); // Handle case when no PIN is set
        gotPin = message; // Save the received PIN
    });

    // Listen for confirmation when the PIN is set
    setPin.sendSetPin.connect(async (message) => {
    });

    // Request the current PIN data from the backend
    getPin.receivePinData();
});

// Handle case when no PIN is set
function handleNoPin() {
    window.location = window.location.host + "nopin.html"; // Redirect to a page notifying that no PIN is set
}

/**
 * Handle the pin data and process it all
 * @param {Number} pin - The PIN input by the user
 */
function handlePinData(pin) {
    // If the entered PIN matches the stored PIN, redirect to the main page
    if (pin == gotPin) window.location = "index.html";
    else {
        // If the PIN is incorrect, show an error message
        document.getElementById("error").innerText = "The PIN was incorrect. Please try again."; // Update error message
        // If the URL includes ?failed=true, reload the page to show the error again
        if(window.location.href.includes("?failed=true")) 
            window.location = window.location;
        else
            // Otherwise, append ?failed=true to the URL to trigger the error message
            window.location = `${window.location}?failed=true`;
    }
}

// If the URL has a 'failed=true' parameter, display an error message
if (CheckableParams.failed == "true") {
    document.getElementById("error").innerText = "Please try again" // Show error message
}