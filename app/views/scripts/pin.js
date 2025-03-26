let setPin;
let getPin;
let gotPin;

new QWebChannel(qt.webChannelTransport, (channel) => {
    setPin = channel.objects.setPin;
    getPin = channel.objects.getPin;

    getPin.sendPinData.connect(async (message) => {
        gotPin = message;
        console.error(gotPin);
    });

    setPin.sendSetPin.connect(async (message) => {
        console.error(message);
    });

    getPin.receivePinData();
    setPin.receiveNewPin(1234);
});
