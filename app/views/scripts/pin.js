let setPin;
let getPin;
let gotPin;

const CheckableParams = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
});


new QWebChannel(qt.webChannelTransport, (channel) => {
    setPin = channel.objects.setPin;
    getPin = channel.objects.getPin;

    getPin.sendPinData.connect(async (message) => {
        if(message == 0) return handleNoPin();
        gotPin = message;
    });

    setPin.sendSetPin.connect(async (message) => {
    });

    getPin.receivePinData();
    // setPin.receiveNewPin(1234);
});

function handleNoPin() {
    if (CheckableParams.newpin) {
        setPin.receiveNewPin(CheckableParams.newpin);
        window.location = window.location;
        return;
    }
    window.location = window.location.host + "nopin.html";
}

/**
 * Handle the pin data and process it all
 * @param {Number} pin 
 */
function handlePinData(pin) {
    if (pin == gotPin) window.location = "index.html";
    else {
        document.getElementById("error").innerText = "The PIN was incorrect. Please try again."; // Update error message
        if(window.location.href.includes("?failed=true")) 
            window.location = window.location;
        else
            window.location = `${window.location}?failed=true`;
    }
}

if (CheckableParams.failed == "true") {
    document.getElementById("error").innerText = "Please try again"
}