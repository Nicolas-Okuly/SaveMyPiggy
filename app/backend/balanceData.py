from .backend import *
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

class BalanceData(QObject):
    # Signal to send balance data to JavaScript/frontend
    sendBalanceData = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        create_file_if_absent()  # Ensure the database and required tables exist

    @pyqtSlot(str)
    def receiveBalanceData(self, date):
        print("Balance data was requested.")

        # Dictionaries to store categorized income and expenses
        income_categories = defaultdict(float)
        expense_categories = defaultdict(float)

        # Initialize total income, total expense, and balance variables
        total_income = 0
        total_expense = 0

        updateData()  # Ensure the 'after' column is correctly updated

        # Define the start and end dates for the query
        dateStart = rangeStart(date)
        now = datetime.now()

        # Establish database connection
        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.sendBalanceData.emit("")  # Send empty response on failure
            return

        cursor = conn.cursor()

        # Fetch and categorize income transactions within the date range
        cursor.execute("SELECT * FROM transactions WHERE type = 'income' AND date BETWEEN ? AND ?", (dateStart, now))
        rows = cursor.fetchall()
        for row in rows:
            income_categories[row['category']] += float(row['amount'])  # Accumulate income by category
            total_income += float(row['amount'])  # Add to total income

        # Fetch and categorize expense transactions within the date range
        cursor.execute("SELECT * FROM transactions WHERE type = 'expense' AND date BETWEEN ? AND ?", (dateStart, now))
        rows = cursor.fetchall()
        for row in rows:
            expense_categories[row['category']] += float(row['amount'])  # Accumulate expenses by category
            total_expense += float(row['amount'])  # Add to total expenses

        # Fetch the most recent balance from the last transaction
        cursor.execute("SELECT after FROM transactions ORDER BY date DESC LIMIT 1")
        total_balance = cursor.fetchone()
        total_balance = float(total_balance[0]) if total_balance else 0.0  # Convert balance to float, handle None

        # Compute percentage breakdown for income categories
        if total_income <= 0:
            income_category_data = []  # No income, empty list
        else:
            income_category_data = [
                {
                    "name": name, 
                    "value": value, 
                    "percentage": round((value / total_income) * 100, 2)  # Compute category percentage
                }
                for name, value in income_categories.items()
            ]

        # Compute percentage breakdown for expense categories
        if total_expense <= 0:
            expense_category_data = []  # No expenses, empty list
        else:
            expense_category_data = [
                {
                    "name": name, 
                    "value": value, 
                    "percentage": round((value / total_expense) * 100, 2)  # Compute category percentage
                }
                for name, value in expense_categories.items()
            ]

        # Prepare final balance data dictionary
        balance_data = {
            "balance": round(total_balance, 2),  # Round balance to 2 decimal places
            "income": round(total_income, 2),  # Round total income
            "expense": round(total_expense, 2),  # Round total expense
            "incomeCats": income_category_data,  # List of income categories
            "expenseCats": expense_category_data  # List of expense categories
        }

        conn.close()  # Close database connection

        # Convert balance data dictionary to JSON and emit to frontend
        self.sendBalanceData.emit(json.dumps(balance_data))

        # EXAMPLE RETURN STRUCTURE:
        # {
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
