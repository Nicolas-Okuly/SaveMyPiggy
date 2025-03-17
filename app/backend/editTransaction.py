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
            { "id": "whatever it may be (possibly an int)", "changes: { "name/amount/category/date/type": "new data" } }
        '''

        changes = json.loads(data)

        conn = get_db_connection()
        cursor = conn.cursor()

        changeID = int(changes["id"])
        changesRow = changes["changes"] 

        query = 'UPDATE transaction SET '
        for key in changesRow.keys():
            query += key + " = '" + changesRow[key] + "', "

        query += 'WHERE id = ' + changeID
        cursor.execute(query)

        conn.commit()
        conn.close()

        self.editTransactionSignal.emit(True)