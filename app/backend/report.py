from .backend import *
from openpyxl import Workbook


# Class to handle the creation of a transaction report in Excel
class Report(QObject):
    # Signal to notify if the report creation was successful or not
    getReportSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        create_file_if_absent()  # Ensure the database exists and has the necessary tables

    @pyqtSlot()
    def getReport(self):
        '''
        This method creates a transaction report by fetching data from the database
        and exporting it to an Excel file.
        '''
        print(f"Creating Transaction Report")

        # Open the database connection
        conn = get_db_connection()
        if conn is None:
            print("Failed to access database")
            self.getReportSignal.emit(False)  # Emit failure signal if connection fails
            return
        
        cursor = conn.cursor()

        # Fetch all transaction data (name, type, category, amount, date, after balance)
        cursor.execute("SELECT name, type, category, amount, date, after FROM transactions")
        rows = cursor.fetchall()

        # Create a new Excel workbook and sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Transaction Report"  # Set the sheet title

        # Write headers in the first row (columns from the transaction data)
        # This assumes that `rows[0]` is a tuple with data, so it is converted to a list
        headers = rows[0].keys()  # Get the headers (keys)
        ws.append(list(headers))  # Add the headers to the Excel sheet

        # Write each row of transaction data into the sheet
        for row in rows:
            # Convert each row from a tuple to a list and append it to the Excel sheet
            ws.append(tuple(row))  # Use tuple(row) instead of list(row.values())

        # Define the path to save the Excel file
        excel_path = "transaction_report.xlsx"
        
        # Save the workbook to the specified path
        wb.save(excel_path)
        
        # Open the generated Excel file (for Windows, this works with os.startfile)
        os.startfile("transaction_report.xlsx")
        
        # Close the database connection
        conn.close()

        # Emit success signal to notify that the report was created
        self.getReportSignal.emit(True)