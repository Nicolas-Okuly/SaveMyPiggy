from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

class Backend(QObject):
    sendDataToJs = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()

    # Receivable function
    @pyqtSlot(str)
    def receiveFromJs(self, message):
        print(f"Received from JS: {message}")
        self.sendDataToJs.emit(f"Hello, {message}! This is Python.")


    