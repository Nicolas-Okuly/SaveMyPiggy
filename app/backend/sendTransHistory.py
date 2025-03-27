from .backend import *

# For receiving transaction history
class sendTransHistory(QObject):
    sendTransHistory = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        create_file_if_absent()

    @pyqtSlot()
    def receiveTransHistory(self):
        print("Transaction history was requested.")

        # Send all of the users transaction history as a list of dictionaries

        updateData()

        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.sendTransHistory.emit("")
            return
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        transaction_history = cursor.fetchall()

        # Make modifications to data
        transNumber = 0
        for trans in transaction_history:
            # Convert Row object to a dictionary before modifying
            transaction_history[transNumber] = dict(transaction_history[transNumber])

            # Now modify the date
            dt_obj = datetime.strptime(trans['date'], "%Y-%m-%d %H:%M:%S")

            transaction_history[transNumber]['date'] = dt_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            transNumber += 1

        conn.close()
        self.sendTransHistory.emit(json.dumps(transaction_history))

        # # Transaction history needs to meet the template below
        # exampleHistory = [
        #     { "id": 0, "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
        #     { "id": 1, "name": "Taregt Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65},
        #     { "id": 2, "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
        #     { "id": 3, "name": "Taregt Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65},
        #     { "id": 4, "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
        #     { "id": 5, "name": "Taregt Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65}
        # ]