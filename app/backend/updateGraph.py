from .backend import *  # Import necessary backend functions

# Class for updating graphs in the view
class updateGraph(QObject):
    # Signal to notify the view when the graph update is done
    updateGraphSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()  # Ensure the database and necessary files exist

    @pyqtSlot(str)
    def updateGraph(self, date):
        '''
        This method updates the graphs based on the transactions
        within a specific date range.
        '''
        print(f"Updating graphs with {date}")

        # Create an instance of GraphGenerator (responsible for graph creation)
        graphs = GraphGenerator()

        # Initialize accumulators for income and expense categories
        income_categories = defaultdict(float)
        expense_categories = defaultdict(float)
        total_income = 0 
        total_expense = 0

        # Calculate the date range for the selected date
        dateStart = rangeStart(date)
        now = datetime.now()

        # Connect to the database
        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.updateGraphSignal.emit(False)  # Emit signal with failure if DB access fails
            return
        cursor = conn.cursor()

        # Fetch income data within the specified date range
        cursor.execute("SELECT * FROM transactions WHERE type = 'income' AND date BETWEEN ? AND ?", (dateStart, now))
        rows = cursor.fetchall()
        for row in rows:
            income_categories[row['category']] += float(row['amount'])
            total_income += float(row['amount'])

        # Fetch expense data within the specified date range
        cursor.execute("SELECT * FROM transactions WHERE type = 'expense' AND date BETWEEN ? AND ?", (dateStart, now))
        rows = cursor.fetchall()
        for row in rows:
            expense_categories[row['category']] += float(row['amount'])
            total_expense += float(row['amount'])

        # Update the income-expense graph
        graphs.incvexpGraph(total_income, total_expense)

        # Update the expense category pie chart
        graphs.ExpenseCatPie(list(expense_categories.values()), list(expense_categories.keys()))

        # Update the income category pie chart
        graphs.IncomeCatPie(list(income_categories.values()), list(income_categories.keys()))

        # Determine if there is no income or no expense
        noIncome = False
        noExpense = False
        if total_income <= 0:
            noIncome = True

        if total_expense <= 0:
            noExpense = True

        # Update any blank graphs if there are no income or expense data
        graphs.BlankGraphs(noIncome, noExpense)

        # Close the database connection
        conn.close()

        # Emit the success signal indicating the graph update is complete
        self.updateGraphSignal.emit(True)