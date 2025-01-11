from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from .graphGenerator import GraphGenerator

import os
import platform
import csv
import json
import pytz

from collections import defaultdict
from datetime import datetime, timedelta

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
def create_file_if_absent(csv_file_path):
    if not os.path.exists(csv_file_path):
        print(f"File {csv_file_path} not found. Creating a new one.")
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "type", "category", "amount", "date", "after"])
            writer.writeheader()  # Write header if file is created


# Sorts the list of transactions by date
def get_chronological_transactions(transactions):
    if len(transactions) > 0:
        for i in range(0, len(transactions)):
            earliestTransaction = transactions[i]
            for j in range(i+1, len(transactions)):
                if earliestTransaction["date"] > transactions[j]["date"]:
                    earliestTransaction = transactions[j]
            transactions[i] = earliestTransaction
    return transactions


def get_transaction_data(transactions, date, categories):
    total = 0
    now = datetime.now().replace(tzinfo=pytz.utc)

    for transaction in transactions:
            transactionDate = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S%z")

            if (date == "week" and now - timedelta(days = 7) <= transactionDate) or (date == "month" and now - timedelta(days = 30) <= transactionDate) or (date == "year" and now - timedelta(days = 365) <= transactionDate) or (date == "alltime"):

                category = transaction["category"]
                amount = float(transaction["amount"])

                total += amount
                categories[category] += amount

    return total


class BalanceData(QObject):
    sendBalanceData = pyqtSignal(str)
    csv_file_path = os.path.join(get_appdata_folder(), "transactionData.csv")

    def __init__(self):
        super().__init__()

        create_file_if_absent(self.csv_file_path)

    @pyqtSlot(str)
    def receiveBalanceData(self, date):
        print("Balance data was requested.")

        # Insert function to retrieve balance data

        # Initialize accumulators
        total_balance = 0
        total_income = 0
        total_expense = 0
        income_transactions = []
        expense_transactions = []
        income_categories = defaultdict(float)
        expense_categories = defaultdict(float)

        # Read data from the CSV file
        try:
            with open(self.csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['type'] == 'income':
                        income_transactions.append(row)
                    elif row['type'] == 'expense':
                        expense_transactions.append(row)
                total_balance = float(reader[-1]["after"])

        except Exception as e:
            print(f"Error reading the file {self.csv_file_path}: {e}")
            return
        

        total_income = get_transaction_data(income_transactions, date, income_categories)
        total_expense = get_transaction_data(expense_transactions, date, expense_categories)

        # Calculate percentages for categories
        income_category_data = [
            {"name": name, "value": value, "percentage": round((value / total_income) * 100, 2)}
            for name, value in income_categories.items()
        ]
        expense_category_data = [
            {"name": name, "value": value, "percentage": round((value / total_expense) * 100, 2)}
            for name, value in expense_categories.items()
        ]

        # Format the data
        balance_data = {
            "balance": total_balance,
            "income": total_income,
            "expense": total_expense,
            "incomeCats": income_category_data,
            "expenseCats": expense_category_data
        }

        # Emit the balance data as a JSON string
        self.sendBalanceData.emit(f"{balance_data}") 

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

        create_file_if_absent(self.csv_file_path)

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
                        # after_balance = float(row["after"]) if "after" in row and row["after"] else running_balance
                        if (row["type"] == "expense"): after_balance = float(row["amount"]) - float(row["amount"])*2
                        else: after_balance = row["amount"]

                        # after_balance = float(row["after"]) if "after" in row and row["after"] else running_balance

                        transaction = {
                            "name": row["name"],
                            "cost": cost,
                            "category": row["category"],
                            "type": row["type"],
                            "date": date,
                            "after": row["after"],
                        }

                        transaction_history.append(transaction)
                    except (ValueError, KeyError) as e:
                        print(f"Skipping invalid row: {row}, error: {e}")

            # Emit the transaction history as a JSON string
            self.sendTransHistory.emit(json.dumps(transaction_history))
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

        create_file_if_absent(self.csv_file_path)

    @pyqtSlot(str)
    def receiveTransactionData(self, data):
        print(f'Got {str(data)}')

        # Add a transaction to the users transactions

        try:
            with open(self.csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                last_balance = reader[-1]["after"]
                transaction = {
                    "name": data[0],
                    "amount": data[1],
                    "category": data[2],
                    "type": data[3],
                    "date": data[4],
                    "after": last_balance + data[1],
                }
        except Exception as e:
            print(f"Error reading the file {self.csv_file_path}: {e}")

        with open(self.csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file)
            writer.writerow(transaction)

        self.receiveTransaction.emit(True)


# For updating graphs in views/graphs
class updateGraph(QObject):
    updateGraphSignal = pyqtSignal(bool)
    csv_file_path = os.path.join(get_appdata_folder(), "transactionData.csv")

    def __init__(self):
        super().__init__()
        create_file_if_absent(self.csv_file_path)

    @pyqtSlot(str)
    def updateGraph(self, date):
        '''
            When doing backend, please make sure that the date is properly applied and filtered
        '''
        print(f"Updating graphs with {date}")

        # Insert functions that will update all the graphs
        graphs = GraphGenerator()

        income_transactions = []
        expense_transactions = []

        try:
            with open(self.csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["type"] == "income":
                        income_transactions.append(row)
                    elif row["type"] == "expense":
                        expense_transactions.append(row)
        except Exception as e:
            print(f"Error reading the file {self.csv_file_path}: {e}")
            self.updateGraphSignal.emit(False)

        # Initialize accumulators
        # total_income = 0.0
        # total_expense = 0.0

        income_categories = defaultdict(float)
        expense_categories = defaultdict(float)

        income_transactions = get_chronological_transactions(income_transactions)
        expense_transactions = get_chronological_transactions(expense_transactions)

        total_income = get_transaction_data(income_transactions, date, income_categories)
        total_expense = get_transaction_data(expense_transactions, date, expense_categories)

        # now = datetime.now().replace(tzinfo=pytz.utc)

        # for transaction in income_transactions:
        #     transactionDate = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S%z")

        #     if (date == "week" and now - timedelta(days = 7) <= transactionDate) or (date == "month" and now - timedelta(days = 30) <= transactionDate) or (date == "year" and now - timedelta(days = 365) <= transactionDate) or (date == "alltime"):

        #         category = transaction["category"]
        #         amount = float(transaction["amount"])

        #         total_income += amount
        #         income_categories[category] += amount

        # for transaction in expense_transactions:
        #     transactionDate = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S%z")

        #     if (date == "week" and now - timedelta(days = 7) <= transactionDate) or (date == "month" and now - timedelta(days = 30) <= transactionDate) or (date == "year" and now - timedelta(days = 365) <= transactionDate) or (date == "alltime"):
        #         category = transaction["category"]
        #         amount = float(transaction["amount"])

        #         total_expense += amount
        #         expense_categories[category] += amount


        graphs.incvexpGraph(total_income, total_expense) # Make sure function that pulls balance data happens here

        # Make sure these are properly formatted with the transaction list
        graphs.ExpenseCatPie(list(expense_categories.values()), list(expense_categories.keys()))

        # Make sure these are properly formatted with the transaction list
        graphs.IncomeCatPie(list(income_categories.values()), list(income_categories.keys()))
        self.updateGraphSignal.emit(True)


# For editing a transaction from the list of transactions
class editTransaction(QObject):
    editTransactionSignal = pyqtSignal(bool)
    csv_file_path = os.path.join(get_appdata_folder(), "transactionData.csv")


    def __init__(self):
        super().__init__()
        create_file_if_absent(self.csv_file_path)

    @pyqtSlot(str)
    def updateTransaction(self, old_data, new_data):
        '''
            data will look roughly like this:
            [ "Transaction Name", "Transaction Amount", "Transaction Category", "Transaction Type", "Transaction Date" ]

            idk how you want to find it but I gave you the info
        '''
        beforeData = []
        afterData = []
        rowIsFound = False
        try:
            with open(self.csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row == old_data:
                        rowIsFound = True
                    elif rowIsFound:
                        afterData += row
                    else:
                        previousData += row    
        except Exception as e:
            print(f"Error reading the file {self.csv_file_path}: {e}")
            self.editTransactionSignal.emit(False)

        try:
            with open(self.csv_file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file)
                for row in beforeData:
                    writer.writerow(row)
                writer.writerow(new_data)
                for row in afterData:
                    writer.writerow(row)
        except Exception as e:
            print(f"Error writing the file {self.csv_file_path}: {e}")
            self.editTransactionSignal.emit(False)

        self.editTransactionSignal.emit(True)


# For deleting a specific transaction from the list of transactions
class deleteTransaction(QObject):
    deleteTransactionSignal = pyqtSignal(bool)
    csv_file_path = os.path.join(get_appdata_folder(), "transactionData.csv")


    def __init__(self):
        super().__init__()
        create_file_if_absent(self.csv_file_path)


    @pyqtSlot(str)
    def deleteTransaction(self, data):
        '''
            data will look roughly like this:
            [ "Transaction Name", "Transaction Amount", "Transaction Category", "Transaction Type", "Transaction Date" ]

            idk how you want to find it but I gave you the info
        '''
        beforeData = []
        afterData = []
        rowIsFound = False
        try:
            with open(self.csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row == data:
                        rowIsFound = True
                    elif rowIsFound:
                        afterData += row
                    else:
                        previousData += row    
        except Exception as e:
            print(f"Error reading the file {self.csv_file_path}: {e}")
            self.deleteTransactionSignal.emit(False)

        try:
            with open(self.csv_file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file)
                for row in beforeData:
                    writer.writerow(row)
                for row in afterData:
                    writer.writerow(row)
        except Exception as e:
            print(f"Error writing the file {self.csv_file_path}: {e}")
            self.deleteTransactionSignal.emit(False)

        self.deleteTransactionSignal.emit(True)