from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from .graphGenerator import GraphGenerator

# For testing back to front communications
class BackendTest(QObject):
    sendDataToJs = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()

    # Receivable function
    @pyqtSlot(str)
    def receiveFromJs(self, message):
        print(f"Received from JS: {message}")
        self.sendDataToJs.emit(f"Hello, {message}! This is Python.")


class BalanceData(QObject):
    sendBalanceData = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def receiveBalanceData(self):
        print("Balance data was requested.")

        # Insert function to retrieve balance data
        # Formatted as suggested below
        # Income and expense categories should be the same as the graphs
        exampleBalance = {
            "balance": -141.87,
            "income": 2393.23,
            "expense": 2251.36,
            "incomeCats": [
                { "name": "Cat1", "value": 3231.32, "percentage": 34 },
                { "name": "Cat2", "value": 2321.23, "percentage": 66 }
            ],
            "expenseCats": [
                { "name": "Cat1", "value": 2312.29, "percentage": 35 },
                { "name": "Cat2", "value": 943.23, "percentage": 23 }
            ]
        }
        self.sendBalanceData.emit(f'{exampleBalance}')


# For receiving transaction history
class sendTransHistory(QObject):
    sendTransHistory = pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
    @pyqtSlot()
    def receiveTransHistory(self):
        print("Transaction history was requested.")

        # Insert function to send transaction history
        # Transaction history needs to meet the template below
        exampleHistory = [
            { "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
            { "name": "Taregt Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65},
            { "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
            { "name": "Taregt Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65},
            { "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
            { "name": "Taregt Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65}
        ]
        self.sendTransHistory.emit(f"{exampleHistory}")

class receiveTransaction(QObject):
    receiveTransaction = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str)
    def receiveTransactionData(self, data):
        print(f'Got {str(data)}')

        # Add a transaction to the users transactions

        self.receiveTransaction.emit(True)


# For updating graphs in views/graphs
class updateGraph(QObject):
    updateGraphSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str)
    def updateGraph(self, date):
        '''
            When doing backend, please make sure that the date is properly applied and filtered
        '''
        print(f"Updating graphs with {date}")

        # Insert functions that will update all the graphs
        graphs = GraphGenerator()

        graphs.incvexpGraph(2393.23, 2251.36) # Make sure function that pulls balance data happens here

        # Make sure these are properly formatted with the transaction list
        graphs.ExpenseCatPie([342, 546, 983.34], ["Automobile", "Food", "Shopping"])

        # Make sure these are properly formatted with the transaction list
        graphs.IncomeCatPie([1000, 120.12, 45.65], ["Paycheck", "Tax Return", "Refunds"])
        self.updateGraphSignal.emit(True)