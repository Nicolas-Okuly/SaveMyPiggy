from .backend import *


# For updating graphs in views/graphs
class updateGraph(QObject):
    updateGraphSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()

    @pyqtSlot(str)
    def updateGraph(self, date):
        print(f"Updating graphs with {date}")

        # Insert functions that will update all the graphs
        graphs = GraphGenerator()

        income_categories = defaultdict(float)
        expense_categories = defaultdict(float)
        total_income = 0 
        total_expense = 0

        dateStart = rangeStart(date)
        now = datetime.now()

        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.updateGraphSignal.emit(False)
            return
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
            expense_categories[row['category']] += float(row['amount'])
            total_expense += float(row['amount'])

        graphs.incvexpGraph(total_income, total_expense) # Make sure function that pulls balance data happens here

        # Make sure these are properly formatted with the transaction list
        graphs.ExpenseCatPie(list(expense_categories.values()), list(expense_categories.keys()))

        # Make sure these are properly formatted with the transaction list
        graphs.IncomeCatPie(list(income_categories.values()), list(income_categories.keys()))

        noIncome = False
        noExpense = False
        if total_income <= 0:
            noIncome = True

        if total_expense <= 0:
            noExpense = True

        graphs.BlankGraphs(noIncome, noExpense)
        
        conn.close()
        self.updateGraphSignal.emit(True)