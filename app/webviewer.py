# app/webviewer.py
# Imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from .backend import Backend
import sys, os

# Get the absolute path to the resource, for PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# WebApp Class
class WebApp(QMainWindow):
    # Init function
    def __init__(self):
        # Set window title and window geometry
        super().__init__()
        self.setWindowTitle("Hello World!")
        self.setGeometry(100, 100, 800, 600)

        # Initialize the webview and load the html files
        webview = QWebEngineView()
        start_page = resource_path("views/index.html")
        webview.setUrl(QUrl(f"file:///{start_page}"))

        # Set up the web channel
        self.channel = QWebChannel()
        self.backend = Backend()

        # Connect the backend object to the channel
        self.channel.registerObject("backend", self.backend)
        webview.page().setWebChannel(self.channel)

        # Load the layout of the page
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(webview)
        container.setLayout(layout)
        self.setCentralWidget(container)

# Declare the startup app
def RunApp():
    # Initalize and application and start it
    app = QApplication(sys.argv)
    main_window = WebApp()
    main_window.show()
    sys.exit(app.exec_())