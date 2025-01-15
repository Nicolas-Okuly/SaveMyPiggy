# FBLA 2024 - Coding and Programming

## Creating Virual Environment
To create your virtual environment run the command below and then activate it.
```bash
$ python3 -m venv .venv
```
---

## Installing requirements
To install all the requirements run the command below.
```bash
$ pip install -r requirements.txt
```

---

## Compiling as an executable
To compile the application as an executable run the command below after ensuring all steps above have been completed.
```bash
$ python3 build_package.py
```
The exe will be in the new folder `dist`.

---

## Directory Structure

### Root Directory
- **`.gitignore`**  
  Specifies files and directories to ignore in version control.  

- **`app.py`**  
  The main entry point for running the application.  

- **`build_package.py`**  
  Script for building the application for deployment or distribution.

- **`icon.ico`**  
  The application icon used in the interface and installer.

- **`requirements.txt`**  
  Lists all Python dependencies required to run the application.  

---

### `app/`
This folder has the application logic and functionality:
- **`__init__.py`**  
  Marks the location as a Python package.  

- **`backend.py`**  
  Handles backend operations and application data.  

- **`graphGenerator.py`**  
  Contains functions for generating graphs.  

- **`webviewer.py`**  
  Renders the front-end.  

---

### `app/views/`
Contains the front-end of the webpage.
- **`graphs/`**  
  Contains the graphs.  

- **`icons/`**  
  Stores graphical icons for the website.  

- **`scripts/`**  
  Contains all the scripts for the document.

- **`/`**  
  - `help.css`: Stylesheet for the help page.  
  - `styles.css`: General styles for the application.  
  - `help.html`: Help or documentation page for users.  
  - `index.html`: The main HTML file for the application's interface.  

---

Big thanks to [SVG Repo](https://svgrepo.com) for miscellanous assets!