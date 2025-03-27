from .backend import *


# For adding a new transaction
class receiveTransaction(QObject):
    receiveTransaction = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()

    @pyqtSlot(str)
    def receiveTransactionData(self, data):
        # Convert JSON string to list properly
        data = json.loads(data)  # Parse correctly
        print(f'Got {data}')

        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.receiveTransaction.emit(False)
            return
        cursor = conn.cursor()

        # Get the last transaction
        cursor.execute("SELECT after FROM transactions ORDER BY date DESC LIMIT 1")
        last_transaction = cursor.fetchone()

        data[1] = round(float(data[1]), 2)

        # Calculate `new_after` safely
        if data[3] == 'expense':
            if last_transaction:
                new_after = float(last_transaction[0]) - data[1]
            else:
                new_after = -1 * data[1]
        
        else:
            if last_transaction:
                new_after = float(last_transaction[0]) + data[1] 
            else:
                new_after = data[1]
        
        data[4] = str(datetime.strptime(data[4], "%Y-%m-%dT%H:%M:%S.%fZ"))

        data.append(new_after)

        # Insert into the database
        cursor.execute(
            'INSERT INTO transactions (name, amount, category, type, date, after) VALUES (?, ?, ?, ?, ?, ?)', 
            tuple(data)
        )
        conn.commit()
        conn.close()

        updateData()

        self.receiveTransaction.emit(True)
