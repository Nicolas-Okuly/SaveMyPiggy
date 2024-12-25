# Imports
import PyInstaller.__main__
import shutil
import os

# All files need to manually be added along with what directory they reside in
# Keep views out on their own, files are weird
files = [
    ("app/__init__.py", "app"),
    ("app/backend.py", "app"),
    ("app/webviewer.py", "app"),
    ("app/views/index.html", "views"),
    ("app/views/scripts/qwebchannel.js", "views/scripts"),
]

# Create the exe
PyInstaller.__main__.run([
    "app.py",
    "--onefile",
    "--noconsole",
    *[f"--add-data={src}:{dest}" for src, dest in files]
])

# Clean up
shutil.rmtree("build")
os.remove("app.spec")