from .backend import *

# Class for handling the editing of an existing transaction
class editTransaction(QObject):
    # Signal to notify frontend (JS) about whether the edit was successful
    editTransactionSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()  # Ensure the database and required tables exist if missing

    @pyqtSlot(str)
    def updateTransaction(self, data):
        '''
            I will send it to you as a JSON Object:
            { "id": "whatever it may be (possibly an int)", 
              "changes": { "name/amount/category/type": "new data" } }
        '''

        # Parse the incoming JSON data into a Python dictionary
        changes = json.loads(data)

        # Establish connection to the database
        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.editTransactionSignal.emit(False)  # Emit failure signal if the connection fails
            return
        
        cursor = conn.cursor()

        # Extract the transaction ID and the changes to be made
        changeID = int(changes["id"])  # Transaction ID (must be an integer)
        changesRow = changes["changes"]  # The dictionary containing the changes to be made

        # Loop through the changes and update each field accordingly
        for key in changesRow.keys():
            if key == "amount":
                # Ensure the 'amount' field is rounded to two decimal places
                changesRow[key] = round(float(changesRow[key]), 2)

            # If the new value is not zero, update the respective field in the database
            if changesRow[key] != 0:
                cursor.execute(f'UPDATE transactions SET {key} = ? WHERE id = ?', (changesRow[key], changeID))

        # Commit the changes to the database
        conn.commit()
        conn.close()

        # Recalculate and update 'after' amounts for all transactions
        updateData()

        # Emit success signal to notify frontend
        self.editTransactionSignal.emit(True)