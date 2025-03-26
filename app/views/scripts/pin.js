let setPin;
let getPin;
let gotPin;

new QWebChannel(qt.webChannelTransport, (channel) => {
    setPin = channel.objects.setPin;
    getPin = channel.objects.getPin;

    getPin.sendPinData.connect(async (message) => {
        gotPin = message;
    });

    setPin.sendSetPin.connect(async (message) => {
        console.error(message);
    });

    getPin.receivePinData();
    // setPin.receiveNewPin(1234);
});

/**
 * Handle the pin data and process it all
 * @param {Number} pin 
 */
function handlePinData(pin) {
    if (pin == gotPin) window.location = "index.html";
    else {
        if(window.location.href.includes("?failed=true")) 
            window.location = window.location;
        else 
            window.location = `${window.location}?failed=true`;
    }
}

const CheckableParams = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
});

if (CheckableParams.failed == "true") {
    document.getElementById("error").innerText = "Please try again"
}