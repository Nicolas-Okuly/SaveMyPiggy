from .backend import *

# Class for retrieving the stored PIN from the database
class GetPin(QObject):
    # Signal to send the retrieved PIN to the frontend (JS)
    sendPinData = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        create_file_if_absent()  # Ensure the database and required tables exist if missing

    @pyqtSlot()
    def receivePinData(self):
        '''
            Retrieves the PIN from the database or sends 0 if the PIN is unset.
        '''
        # Establish connection to the database
        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.sendPinData.emit(-1)  # Emit -1 to signal failure
            return
        
        cursor = conn.cursor()

        # Execute the query to fetch the PIN
        cursor.execute('SELECT pin FROM pin')
        pin = cursor.fetchone()[0]  # Retrieve the PIN value from the query result

        conn.close()

        # Send the PIN data to the frontend (JS)
        self.sendPinData.emit(pin)


# Class for setting a new PIN in the database
class SetPin(QObject):
    # Signal to notify frontend about whether setting the PIN was successful
    sendSetPin = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()  # Ensure the database and required tables exist if missing
    
    @pyqtSlot(int)
    def receiveNewPin(self, new_pin):
        '''
            Sets a new PIN in the database. Returns True if successful, False if failed.
        '''
        print("Updating Pin to ", new_pin)

        # Establish connection to the database
        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.sendSetPin.emit(False)  # Emit failure signal if connection fails
            return
        
        cursor = conn.cursor()

        # Execute the query to update the PIN in the database
        cursor.execute('UPDATE pin SET pin = ?', (new_pin,))

        conn.commit()  # Commit the changes to the database
        conn.close()

        # Emit success signal to notify frontend (JS)
        self.sendSetPin.emit(True)