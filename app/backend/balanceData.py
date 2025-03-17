from .backend import *


class BalanceData(QObject):
    sendBalanceData = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        create_file_if_absent()

    @pyqtSlot(str)
    def receiveBalanceData(self, date):
        print("Balance data was requested.")

        # Initialize accumulators
        income_categories = defaultdict(float)
        expense_categories = defaultdict(float)
        total_income = 0 
        total_expense = 0

        dateStart = rangeStart(date)
        now = datetime.now()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get income data
        cursor.execute("SELECT * FROM transactions WHERE type = 'income' AND date BETWEEN ? AND ?", (dateStart, now))
        rows = cursor.fetchall()
        for row in rows:
            income_categories[row['category']] += float(row['amount'])
            total_income += float(row['amount'])

        # Get expenses data
        cursor.execute("SELECT * FROM transactions WHERE type = 'expense' AND date BETWEEN ? AND ?", (dateStart, now))
        rows = cursor.fetchall()
        for row in rows:
            income_categories[row['category']] += float(row['amount'])
            total_expense += float(row['amount'])

        # Get balance after
        cursor.execute("SELECT after FROM transactions ORDER BY id DESC LIMIT 1")
        total_balance = cursor.fetchone()[0]

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

        conn.close()

        # Emit the balance data as a JSON string
        self.sendBalanceData.emit(f"{json.dumps(balance_data)}")

        # EXAMPLE RETURN
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