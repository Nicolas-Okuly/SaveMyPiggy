from .backend import *

# Class for handling the deletion of a specific transaction
class deleteTransaction(QObject):
    # Signal to notify frontend (JS) whether the deletion was successful
    deleteTransactionSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()  # Ensure the database and required tables exist if missing

    @pyqtSlot(str)
    def deleteTransaction(self, id):
        print("Deleting id: " + id)

        id = int(id)  # Convert the transaction ID to an integer

        # Establish connection to the database
        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.deleteTransactionSignal.emit(False)  # Emit failure signal if connection fails
            return
        
        cursor = conn.cursor()

        # Execute SQL query to delete the transaction with the given ID
        cursor.execute(f"DELETE FROM transactions WHERE id = '{id}'")

        # Commit the transaction to the database
        conn.commit()
        conn.close()

        updateData()  # Recalculate the 'after' amounts for all transactions

        # Emit success signal to notify frontend
        self.deleteTransactionSignal.emit(True)