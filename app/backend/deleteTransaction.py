from .backend import *

# For deleting a specific transaction from the list of transactions
class deleteTransaction(QObject):
    deleteTransactionSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()


    @pyqtSlot(str)
    def deleteTransaction(self, id):
        print("Deleting id: " + id)

        id = int(id)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"DELETE FROM transactions WHERE id = '{id}'")
        
        conn.commit()
        conn.close()
        self.deleteTransactionSignal.emit(True)