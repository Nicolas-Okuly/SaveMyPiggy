from .backend import *


# For adding a new transaction
class receiveTransaction(QObject):
    receiveTransaction = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()

    @pyqtSlot(str)
    def receiveTransactionData(self, data):
        # Add a transaction to the users transactions

        # Convert JSON to list
        data = str(data).replace('[', '').replace(']', '').replace('"', '').split(',')
        print(f'Got {str(data)}')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Calculate after value
        cursor.execute("SELECT after FROM transactions ORDER BY id DESC LIMIT 1")
        data[3] = float(data[3])
        new_after = cursor.fetchone()[0] + data[3]
        data.append(new_after)

        # Add data to database
        cursor.executemany('INSERT INTO transactions (name, type, category, amount, date, after) VALUES (?, ?, ?, ?, ?, ?)', tuple(data))
        conn.commit()

        conn.close()
        self.receiveTransaction.emit(True)