from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from .graphGenerator import GraphGenerator

import os
import platform
import csv
from collections import defaultdict
from datetime import datetime

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


# Returns the path to the AppData folder based on the operating system.
def get_appdata_folder():
    system = platform.system()
    if system == "Windows":
        return os.environ["APPDATA"]
    elif system == "Darwin":  # macOS
        return os.path.join(os.environ["HOME"], "Library", "Application Support")
    elif system == "Linux":
        return os.path.join(os.environ["HOME"], ".local", "share")
    else:
        raise OSError("Unsupported operating system")


# Check if the CSV file exists; if not, create an empty one
def create_file_if_absent(self, csv_file_path):
    if not os.path.exists(self.csv_file_path):
        print(f"File {self.csv_file_path} not found. Creating a new one.")
        with open(self.csv_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "type", "category", "amount", "date", "after"])
            writer.writeheader()  # Write header if file is created


class BalanceData(QObject):
    sendBalanceData = pyqtSignal(str)
    csv_file_path = os.path.join(get_appdata_folder(), "transactionData.csv")

    def __init__(self):
        super().__init__()

        create_file_if_absent(self, self.csv_file_path)

    @pyqtSlot()
    def receiveBalanceData(self):
        print("Balance data was requested.")

        # Insert function to retrieve balance data

        # Initialize accumulators
        total_income = 0
        total_expense = 0
        income_categories = defaultdict(float)
        expense_categories = defaultdict(float)

        # Check if the file exists before reading
        if not os.path.exists(self.csv_file_path):
            print(f"Error: The file {self.csv_file_path} is missing.")
            return

        # Read data from the CSV file
        try:
            with open(self.csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    amount = float(row['amount'])
                    category = row['category']
                    if row['type'] == 'income':
                        total_income += amount
                        income_categories[category] += amount
                    elif row['type'] == 'expense':
                        total_expense += amount
                        expense_categories[category] += amount
        except Exception as e:
            print(f"Error reading the file {self.csv_file_path}: {e}")
            return

        # Calculate percentages for categories
        income_category_data = [
            {"name": name, "value": value, "percentage": round((value / total_income) * 100, 2)}
            for name, value in income_categories.items()
        ]
        expense_category_data = [
            {"name": name, "value": value, "percentage": round((value / total_expense) * 100, 2)}
            for name, value in expense_categories.items()
        ]

        # Calculate total balance
        total_balance = total_income - total_expense

        # Format the data
        balance_data = {
            "balance": total_balance,
            "income": total_income,
            "expense": total_expense,
            "incomeCats": income_category_data,
            "expenseCats": expense_category_data
        }

        # Emit the balance data as a JSON string
        self.sendBalanceData.emit(f'{balance_data}')

        # # Formatted as suggested below
        # # Income and expense categories should be the same as the graphs
        # exampleBalance = {
        #     "balance": -141.87,
        #     "income": 2393.23,
        #     "expense": 2251.36,
        #     "incomeCats": [
        #         { "name": "Cat1", "value": 3231.32, "percentage": 34 },
        #         { "name": "Cat2", "value": 2321.23, "percentage": 66 }
        #     ],
        #     "expenseCats": [
        #         { "name": "Cat1", "value": 2312.29, "percentage": 35 },
        #         { "name": "Cat2", "value": 943.23, "percentage": 23 }
        #     ]
        # }
        # self.sendBalanceData.emit(f'{exampleBalance}')


# For receiving transaction history
class sendTransHistory(QObject):
    sendTransHistory = pyqtSignal(str)
    csv_file_path = os.path.join(get_appdata_folder(), "transactionData.csv")

    def __init__(self):
        super().__init__()

        create_file_if_absent(self, self.csv_file_path)

    @pyqtSlot()
    def receiveTransHistory(self):
        print("Transaction history was requested.")

        # Insert function to send transaction history

        if not os.path.exists(self.csv_file_path):
            print(f"Error: The file {self.csv_file_path} is missing.")
            self.sendTransHistory.emit("[]")
            return

        transaction_history = []
        running_balance = 0.0  # To calculate the 'after' balance dynamically

        # Read data from the CSV file
        try:
            with open(self.csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        cost = float(row["amount"])
                        date = datetime.strptime(row["date"], "%Y-%m-%dT%H:%M:%S%z").isoformat()

                        # Calculate running balance
                        running_balance += cost

                        # Use the existing 'after' value if valid, otherwise calculate dynamically
                        after_balance = float(row["after"]) if "after" in row and row["after"] else running_balance

                        transaction = {
                            "name": row["name"],
                            "cost": cost,
                            "category": row["category"],
                            "type": row["type"],
                            "date": date,
                            "after": after_balance,
                        }

                        transaction_history.append(transaction)
                    except (ValueError, KeyError) as e:
                        print(f"Skipping invalid row: {row}, error: {e}")

            # Emit the transaction history as a JSON string
            self.sendTransHistory.emit(f"{str(transaction_history)}")
        except Exception as e:
            print(f"Error reading the file {self.csv_file_path}: {e}")
            self.sendTransHistory.emit([])

        # # Transaction history needs to meet the template below
        # exampleHistory = [
        #     { "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
        #     { "name": "Taregt Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65},
        #     { "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
        #     { "name": "Taregt Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65},
        #     { "name": "Gas", "cost": -56.78, "category": "Automobile", "type": "expense", "date": "2024-01-06T19:20:34-07:00", "after": 141.87 },
        #     { "name": "Taregt Refund", "cost": 198.65, "category": "Shopping", "type": "income", "date": "2024-06-06T09:12:23-07:00", "after": 198.65}
        # ]
        # self.sendTransHistory.emit(f"{exampleHistory}")


# For adding a new transaction
class receiveTransaction(QObject):
    receiveTransaction = pyqtSignal(bool)
    csv_file_path = os.path.join(get_appdata_folder(), "transactionData.csv")

    def __init__(self):
        super().__init__()

        create_file_if_absent(self, self.csv_file_path)

    @pyqtSlot(str)
    def receiveTransactionData(self, data):
        print(f'Got {str(data)}')

        # Add a transaction to the users transactions

        transaction = {
            "name": data[0],
            "amount": data[1],
            "category": data[2],
            "type": data[3],
            "date": data[4],
        }

        with open(self.csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file)
            writer.writerow(transaction)

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