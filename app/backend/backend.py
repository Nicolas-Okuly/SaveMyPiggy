from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from ..graphGenerator import GraphGenerator

import os
import platform
import csv
import json
import sqlite3

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


# Opens and creates a connection with db file, return the connection
def get_db_connection():
   db_path = os.path.join(get_appdata_folder(), "transactions.db")
   conn = sqlite3.connect(db_path)
   conn.row_factory = sqlite3.Row  # Allows accessing rows as dicts
   return conn


# Check if the SQL file exists; if not, create an empty one
def create_file_if_absent():
   conn = get_db_connection()
   cursor = conn.cursor()
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
   cursor.execute('''
           CREATE TABLE IF NOT EXISTS pin (
               pin INTEGER
           )
       ''')
   cursor.execute('SELECT COUNT(*) FROM pin')
   if cursor.fetchone()[0] == 0:
       cursor.execute('INSERT INTO pin (pin) VALUES (0)')
   conn.commit()
   conn.close()


# Returns the starting day of each time span
def rangeStart(date):
    now = datetime.now()

    if (date == "week"): 
        return now - timedelta(days = 7)
    elif (date == "month"):
        return now - timedelta(days = 30)
    elif(date == "year"):
        return now - timedelta(days = 365)
    return datetime(1, 1, 1)


# Updates the 'after' amounts after any change in transactions
def updateData():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    data = cursor.fetchall()

    currAfter = 0

    for trans in data:
        currId = trans['id']
        if trans['type'] == 'expense':
            currAfter -= trans['amount']
        else:
            currAfter += trans['amount']
        cursor.execute('UPDATE transactions SET after = ? WHERE id = ?', (currAfter, currId))
    
    conn.commit()
    conn.close()
    