from .backend import *


# For updating graphs in views/graphs
class updateGraph(QObject):
    updateGraphSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()

    @pyqtSlot(str)
    def updateGraph(self, date):
        '''
            When doing backend, please make sure that the date is properly applied and filtered
        '''
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
        cursor = conn.cursor()

        # Get income data
        cursor.execute("SELECT * FROM transactions WHERE type = 'income' AND date BETWEEN ? AND ?", (dateStart, now))
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            income_categories[row['category']] += float(row['amount'])
            total_income += float(row['amount'])
        

        # Get expenses data
        cursor.execute("SELECT * FROM transactions WHERE type = 'expense' AND date BETWEEN ? AND ?", (dateStart, now))
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            expense_categories[row['category']] += float(row['amount'])
            total_expense += float(row['amount'])


        graphs.incvexpGraph(total_income, total_expense) # Make sure function that pulls balance data happens here

        # Make sure these are properly formatted with the transaction list
        graphs.ExpenseCatPie(list(expense_categories.values()), list(expense_categories.keys()))

        # Make sure these are properly formatted with the transaction list
        graphs.IncomeCatPie(list(income_categories.values()), list(income_categories.keys()))
        self.updateGraphSignal.emit(True)