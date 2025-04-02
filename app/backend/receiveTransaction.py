from .backend import *


# Class for handling the addition of a new transaction
class receiveTransaction(QObject):
    # Signal to notify the frontend (JS) whether the transaction was successfully received
    receiveTransaction = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()  # Ensure the database and required tables exist if missing

    @pyqtSlot(str)
    def receiveTransactionData(self, data):
        '''
            The method is designed to handle a new transaction by:
            - Parsing the incoming JSON data.
            - Inserting the transaction into the database.
            - Updating the `after` balance based on transaction type (income or expense).
        '''
        # Convert the incoming JSON string into a Python list (correctly parse it)
        data = json.loads(data)  
        print(f'Got {data}')

        # Establish connection to the database
        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.receiveTransaction.emit(False)  # Emit failure signal if connection fails
            return
        
        cursor = conn.cursor()

        # Retrieve the last transaction to calculate the new 'after' balance
        cursor.execute("SELECT after FROM transactions ORDER BY date DESC LIMIT 1")
        last_transaction = cursor.fetchone()

        # Round the amount to 2 decimal places
        data[1] = round(float(data[1]), 2)

        # Safely calculate the new 'after' balance based on the type of transaction (expense or income)
        if data[3] == 'expense':
            if last_transaction:
                # Subtract from the last balance if it's an expense
                new_after = float(last_transaction[0]) - data[1]
            else:
                # If no last transaction, start the balance as negative
                new_after = -1 * data[1]
        
        else:  # If it's an income
            if last_transaction:
                # Add to the last balance if it's an income
                new_after = float(last_transaction[0]) + data[1]
            else:
                # If no last transaction, start the balance with the income value
                new_after = data[1]
        
        # Convert the date from the incoming format to a proper datetime object
        data[4] = str(datetime.strptime(data[4], "%Y-%m-%dT%H:%M:%S.%fZ"))

        # Append the calculated new 'after' balance to the data list
        data.append(round(new_after, 2))

        # Insert the new transaction into the database
        cursor.execute(
            'INSERT INTO transactions (name, amount, category, type, date, after) VALUES (?, ?, ?, ?, ?, ?)', 
            tuple(data)
        )
        conn.commit()  # Commit the transaction to the database
        conn.close()

        # Recalculate and update the 'after' amounts for all transactions
        updateData()

        # Emit success signal to notify frontend (JS) that the transaction was successfully added
        self.receiveTransaction.emit(True)