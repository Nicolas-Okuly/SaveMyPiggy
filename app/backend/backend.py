from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from ..graphGenerator import GraphGenerator

import os
import platform
import csv
import json
import sqlite3

from collections import defaultdict
from datetime import datetime, timedelta


# Backend class for testing communication between Python and JavaScript
class BackendTest(QObject):
    # Signal to send data to JavaScript
    sendDataToJs = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    # Slot to receive messages from JavaScript
    @pyqtSlot(str)
    def receiveFromJs(self, message):
        print(f"Received from JS: {message}")
        # Send a response back to JavaScript
        self.sendDataToJs.emit(f"Hello, {message}! This is Python.")


# Returns the path to the AppData folder based on the operating system
def get_appdata_folder():
    system = platform.system()
    if system == "Windows":
        return os.environ["APPDATA"]  # Windows: C:\Users\Username\AppData\Roaming
    elif system == "Darwin":  # macOS
        return os.path.join(os.environ["HOME"], "Library", "Application Support")
    elif system == "Linux":
        return os.path.join(os.environ["HOME"], ".local", "share")
    else:
        raise OSError("Unsupported operating system")  # Handle unknown OS cases


# Opens and creates a connection to the SQLite database file
def get_db_connection():
    db_path = os.path.join(get_appdata_folder(), "transactions.db")  # Define DB location
    conn = sqlite3.connect(db_path)  # Connect to SQLite database
    conn.row_factory = sqlite3.Row  # Allows accessing rows as dictionaries
    return conn


# Checks if the database file exists; if not, creates necessary tables
def create_file_if_absent():
    conn = get_db_connection()  # Connect to the database
    if conn is None:
        print("Failed to access database")
        return
    cursor = conn.cursor()

    # Create the 'transactions' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            after REAL NOT NULL
        )
    ''')

    # Create the 'pin' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pin (
            pin INTEGER
        )
    ''')

    # Ensure the 'pin' table has at least one record
    cursor.execute('SELECT COUNT(*) FROM pin')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO pin (pin) VALUES (0)')  # Default pin value

    conn.commit()  # Save changes
    conn.close()  # Close the database connection


# Returns the starting date for different time spans ('week', 'month', 'year')
def rangeStart(date):
    now = datetime.now()  # Get the current date and time

    if date == "week": 
        return now - timedelta(days=7)  # Subtract 7 days
    elif date == "month":
        return now - timedelta(days=30)  # Subtract 30 days
    elif date == "year":
        return now - timedelta(days=365)  # Subtract 365 days
    return datetime(1, 1, 1)  # Default: Return a very old date (Year 1)


# Updates the 'after' column in the transactions table to reflect running balances
def updateData():
    conn = get_db_connection()  # Connect to the database
    if conn is None:
        print("Failed to access database")
        return
    cursor = conn.cursor()

    # Fetch all transactions ordered by date (oldest first)
    cursor.execute("SELECT * FROM transactions ORDER BY date ASC")
    data = cursor.fetchall()

    currAfter = 0  # Variable to track the running balance

    # Loop through each transaction to update running balance
    for trans in data:
        currId = trans['id']  # Get transaction ID
        if trans['type'] == 'expense':
            currAfter -= trans['amount']  # Subtract expense from balance
        else:
            currAfter += trans['amount']  # Add income to balance

        # Update the 'after' column with the new running balance
        cursor.execute('UPDATE transactions SET after = ? WHERE id = ?', (round(currAfter, 2), currId))
    
    conn.commit()  # Save changes
    conn.close()  # Close the database connection