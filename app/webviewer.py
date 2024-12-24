# app/webviewer.py
# Imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys, os

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
        html_folder = os.path.abspath("app/views")
        start_page = os.path.join(html_folder, "index.html")
        webview.setUrl(QUrl(f"file:///{start_page}"))

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