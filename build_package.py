# Imports
import PyInstaller.__main__
import shutil
import os

# All files need to manually be added along with what directory they reside in
# Keep views out on their own, files are weird
files = [
    # app directory
    ("app/__init__.py", "app"),
    ("app/graphGenerator.py", "app"),
    ("app/webviewer.py", "app"),

    # app/backend
    ("app/backend/backend.py", "backend"),
    ("app/backend/balanceData.py", "backend"),
    ("app/backend/deleteTransaction.py", "backend"),
    ("app/backend/editTransaction.py", "backend"),
    ("app/backend/receiveTransaction.py", "backend"),
    ("app/backend/sendTransHistory.py", "backend"),
    ("app/backend/updateGraph.py", "backend"),
    ("app/backend/pin.py", "backend"),

    # app/views
    ("app/views/index.html", "views"),
    ("app/views/styles.css", "views"),
    ("app/views/help.css", "views"),
    ("app/views/help.html", "views"),
    ("app/views/nopin.html", "views"),
    ("app/views/pin.html", "views"),

    # app/views/scripts
    ("app/views/scripts/blur.js", "views/scripts"),
    ("app/views/scripts/communication.js", "views/scripts"),
    ("app/views/scripts/qwebchannel.js", "views/scripts"),
    ("app/views/scripts/transactions.js", "views/scripts"),
    ("app/views/scripts/modal.js", "views/scripts"),
    ("app/views/scripts/pin.js", "views/scripts"),

    # app/views/graphs
    ("app/views/graphs/expense-pie.svg", "views/graphs"),
    ("app/views/graphs/income-pie.svg", "views/graphs"),
    ("app/views/graphs/incomevexpense.svg", "views/graphs"),
    ("app/views/graphs/placeholder.png", "views/graphs"),

    # app/views/icons
    ("app/views/icons/edit.svg", "views/icons"),
    ("app/views/icons/eye-slash.svg", "views/icons"),
    ("app/views/icons/eye.svg", "views/icons"),
    ("app/views/icons/piggybank.svg", "views/icons"),
    ("app/views/icons/trash.svg", "views/icons"),
    ("app/views/icons/add.svg", "views/icons"),

    # Root
    ("icon.ico", "./")
]

# Create the exe
PyInstaller.__main__.run([
    "app.py",
   "--onefile",
    "--noconsole",
    "--windowed",
    "--icon=icon.ico",
    "--hidden-import=matplotlib.backends.backend_svg",
    *[f"--add-data={src}:{dest}" for src, dest in files]
])
