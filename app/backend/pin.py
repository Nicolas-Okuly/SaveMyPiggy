from .backend import *

class GetPin(QObject):
    sendPinData = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def receivePinData(self):
        # send pin data or 0 if the pin is unset

        self.sendPinData.emit(1234) # Test data

class SetPin(QObject):
    sendSetPin = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
    
    @pyqtSlot(int)
    def receiveNewPin(self, pin):
        # Set pin sent from the front, return true if successful and false if it failed (it shouldnt fail)

        self.sendSetPin.emit(True) # Test data