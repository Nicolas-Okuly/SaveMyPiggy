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

# SaveMyPiggy Project Documentation

## Overview
SaveMyPiggy is a financial management application designed to help users track their expenses and savings. It features a user-friendly UI with a secure PIN authentication system.

## Features
- **Secure PIN Entry**: Users can create and confirm a 4-digit PIN for secure access.
- **Expense Tracking**: Track transactions, view balance history, and generate reports.
- **Data Visualization**: Interactive graphs to analyze spending trends.
- **Cross-Platform Support**: Runs on Windows, Mac, and Linux using PyQt5.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript (UI Design)
- **Backend**: Python (PyQt5, Flask, WebChannel API)
- **Database**: SQLite (For storing transactions and PINs)
- **Logging**: Python logging module for error handling

## Installation
### Prerequisites
- Python 3.x
- PyQt5 (`pip install PyQt5`)
- Flask (`pip install Flask`)

### Steps
1. Create Virtual Environment:
   ```sh
   python -m venv .venv
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app/main.py
   ```

## File Structure
```
SaveMyPiggy/
│── app/
│   ├── __init__.py
│   ├── graphGenerator.py           # Generate Graphs
│   ├── webviewer.py      # Handles UI rendering with PyQt5
│   ├── backend/
│   │   ├── backend.py
│   │   ├── balanceData.py
│   │   ├── deleteTransaction.py
│   │   ├── editTransaction.py
│   │   ├── pin.py
│   │   ├── receiveTransaction.py
│   │   ├── report.py
│   │   ├── sendTransHistory.py
│   │   ├── updateGraph.py
│── views/
│   ├── graphs/
│   │   ├── expense-pie.svg
│   │   ├── income-pie.svg
│   │   ├── incomevexpense.svg
│   │   ├── placeholder.png
│   ├── icons/
│   │   ├── add.svg
│   │   ├── edit.svg
│   │   ├── eye-slash.svg
│   │   ├── eye.svg
│   │   ├── piggybank.svg
│   │   ├── report.svg
│   │   ├── trash.svg
│   ├── scripts/
│   │   ├── blur.js
│   │   ├── communication.js
│   │   ├── debug.js
│   │   ├── modal.js
│   │   ├── pin.js
│   │   ├── qwebchannel.js
│   │   ├── transactions.js
│   ├── help.css
│   ├── help.html 
│   ├── index.html
│   ├── nopin.html
│   ├── pin.html
│   ├── styles.css 
│── app.py
│── build_package.py
│── icon.ico
│── README.md
│── requirements.txt
│── transaction_report.xlsx
```

## Usage
1. **Set a PIN**: Upon first launch, users must create a 4-digit PIN.
2. **Navigate Dashboard**: View balance and recent transactions.
3. **Edit Transactions**: Modify, delete, or add new transactions.
4. **Generate Reports**: Get detailed spending insights.


Big thanks to [SVG Repo](https://svgrepo.com) for miscellanous assets!