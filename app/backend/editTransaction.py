from .backend import *


# For editing a transaction from the list of transactions
class editTransaction(QObject):
    editTransactionSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()

    @pyqtSlot(str)
    def updateTransaction(self, data):
        '''
            I will send it to you as a JSON Object:
            { "id": "whatever it may be (possibly an int)", "changes: { "name/amount/category/type": "new data" } }
        '''

        changes = json.loads(data)

        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.editTransactionSignal.emit(False)
            return
        cursor = conn.cursor()

        changeID = int(changes["id"])
        changesRow = changes["changes"] 

        for key in changesRow.keys():
            if key == "amount":
                changesRow[key] = round(float(changesRow[key]), 2)
            if changesRow[key] != 0:
                cursor.execute(f'UPDATE transactions SET {key} = ? WHERE id = ?', (changesRow[key], changeID))

        conn.commit()
        conn.close()

        updateData()

        self.editTransactionSignal.emit(True)