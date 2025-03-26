# app/webviewer.py
# Imports

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel

from .backend.balanceData import BalanceData
from .backend.receiveTransaction import receiveTransaction
from .backend.sendTransHistory import sendTransHistory
from .backend.editTransaction import editTransaction
from .backend.deleteTransaction import deleteTransaction
from .backend.updateGraph import updateGraph
from .backend.backend import *

import sys, os

# Get the absolute path to the resource, for PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    system = platform.system()
    if system == "Windows":
        return os.path.join(base_path, relative_path).replace("%5C", "/")
    return os.path.join(base_path, relative_path)


# WebApp Class
class WebApp(QMainWindow):
    # Init function
    def __init__(self):
        # Set window title and window geometry
        super().__init__()
        self.setWindowTitle("Finance Tracker")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()
        self.setWindowIcon(QIcon("icon.ico"))

        # Initialize the webview and load the html files
        webview = QWebEngineView()
        # webview.setContextMenuPolicy(False)
        start_page = resource_path("views\pin.html").replace('\\', '/')
        webview.setUrl(QUrl(f"{start_page}"))

        # Enable CORs
        settings = webview.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)

        # Set up the web channel
        self.channel = QWebChannel()

        # Link objects to WebApp
        self.testBackend = BackendTest()
        self.balance = BalanceData()
        self.sendTrans = sendTransHistory()
        self.updateGraphs = updateGraph()
        self.receiveTransaction = receiveTransaction()
        self.deleteTransaction = deleteTransaction()
        self.editTransaction = editTransaction()

        # Register the objects for use in the backend
        self.channel.registerObject("testBackend", self.testBackend)
        self.channel.registerObject("balance", self.balance)
        self.channel.registerObject("sendTrans", self.sendTrans)
        self.channel.registerObject("updateGraphs", self.updateGraphs)
        self.channel.registerObject("receiveTransaction", self.receiveTransaction)
        self.channel.registerObject("deleteTransaction", self.deleteTransaction)
        self.channel.registerObject("editTransaction", self.editTransaction)

        # Set the channel to the page
        webview.page().setWebChannel(self.channel)

        # Load the layout of the page
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0) # Destroy the margins
        layout.addWidget(webview)
        container.setLayout(layout)
        self.setCentralWidget(container)


# Declare the startup app
def RunApp():
    # Initialize and application and start it
    app = QApplication(sys.argv)
    main_window = WebApp()
    main_window.show()
    sys.exit(app.exec_())