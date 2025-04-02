from .backend import *

# Class for handling the retrieval and sending of transaction history
class sendTransHistory(QObject):
    # Signal to send the transaction history to the front-end as a JSON string
    sendTransHistory = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        create_file_if_absent()  # Ensure the database exists and has necessary tables

    @pyqtSlot()
    def receiveTransHistory(self):
        '''
        This method retrieves the transaction history from the database,
        formats it, and sends it as a JSON string.
        '''
        print("Transaction history was requested.")

        # Update data to ensure the 'after' balances are correct
        updateData()

        # Connect to the database
        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.sendTransHistory.emit("")  # Emit an empty string if the database is not accessible
            return

        cursor = conn.cursor()

        # Fetch all transactions ordered by date in descending order
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        transaction_history = cursor.fetchall()

        # Modify the fetched data
        transNumber = 0
        for trans in transaction_history:
            # Convert each Row object to a dictionary for easier modification
            transaction_history[transNumber] = dict(transaction_history[transNumber])

            # Convert the date string from the database to the desired format
            dt_obj = datetime.strptime(trans['date'], "%Y-%m-%d %H:%M:%S")
            transaction_history[transNumber]['date'] = dt_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            transNumber += 1

        # Close the database connection
        conn.close()

        # Emit the formatted transaction history as a JSON string
        self.sendTransHistory.emit(json.dumps(transaction_history))

        # Example format for transaction history:
        # transaction_history = [
        #     { "id": 0, "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
        #     { "id": 1, "name": "Target Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65 },
        #     { "id": 2, "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
        #     { "id": 3, "name": "Target Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65 }
        # ]