from .backend import *

class GetPin(QObject):
    sendPinData = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        create_file_if_absent()

    @pyqtSlot()
    def receivePinData(self):
        # send pin data or 0 if the pin is unset
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT pin FROM pin')
        pin = cursor.fetchone()[0]

        conn.close()

        self.sendPinData.emit(pin) # Test data

class SetPin(QObject):
    sendSetPin = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()
    
    @pyqtSlot(int)
    def receiveNewPin(self, new_pin):
        # Set pin sent from the front, return true if successful and false if it failed (it shouldnt fail)
        print("Updating Pin to ", new_pin)
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('UPDATE pin SET pin = ?', (new_pin,))

        conn.commit()
        conn.close()

        self.sendSetPin.emit(True) # Test data