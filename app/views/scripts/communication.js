// Define communication objects
let sendBalance;
let sendTrans;
let updateGraphs;
let receiveTransaction;
let deleteTransaction;
let editTransaction;
let report;
var globalData;

// Create the web channel for communication with the backend
new QWebChannel(qt.webChannelTransport, function (channel) {
    /*
        Set the communication objects, fetch responses, and send requests to the backend.
    */
    sendBalance = channel.objects.balance;
    sendTrans = channel.objects.sendTrans;
    updateGraphs = channel.objects.updateGraphs;
    receiveTransaction = channel.objects.receiveTransaction;
    deleteTransaction = channel.objects.deleteTransaction;
    editTransaction = channel.objects.editTransaction;
    report = channel.objects.report;

    // Connect the signal from backend for balance data
    sendBalance.sendBalanceData.connect(function (message) {
        // Format the message to JSON and send it to the handler function.
        handleBalData(JSON.parse(message));
    });

    // Connect the signal from backend for graph updates
    updateGraphs.updateGraphSignal.connect(function () {
        // Reload all images by appending a timestamp to force reloading
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            const src = img.src;
            const timestamp = new Date().getTime();
            img.src = src.split('?')[0] + '?' + timestamp;
        });
    });

    // Set up event listener for report button
    document.getElementById("report").onclick = function () {
        report.getReport()
    }

    // Connect the signal from backend for transaction history data
    sendTrans.sendTransHistory.connect(async function (message) {
        // Format the message to JSON and send it to the handler function.
        handleTransData(JSON.parse(message));

        // Set up event listeners for transaction buttons
        await document.querySelectorAll("button").forEach(async (button) => {
            await button.addEventListener("click", async (event) => {
                transactionButtonClick(button, deleteTransaction, editTransaction); // Handle delete/edit transactions
            });
        });
    });

    // Fetch initial data for balance, transaction history, and graphs
    sendBalance.receiveBalanceData("alltime");
    sendTrans.receiveTransHistory();
    updateGraphs.updateGraph("alltime");

    // Set up event listener for income/expense filter
    document.getElementById("income-filter").addEventListener("change", (change) => {
        updateGraphs.updateGraph(change.target.value); // Update graph with selected filter
        sendBalance.receiveBalanceData(change.target.value); // Update balance with selected filter
    });

    // Handle form submission for adding a transaction
    document.getElementById("transaction-form").addEventListener("submit", async (event) => {
        let element = event.target;
        let data = await processFormInput(element); // Process form input
        receiveTransaction.receiveTransactionData(JSON.stringify(data)); // Send data to backend
    });
});

// Handles and updates balance data
/**
 * @param {JSON} data - The balance data
 */
function handleBalData(data) {
    /*
        Fetch all the elements to update and then insert the values
    */
   const balance = document.getElementById("current_balance");
   const income = document.getElementById("income");
   const expense = document.getElementById("expense");
   const incomeCats = document.getElementById("income-cats");
   const expenseCats = document.getElementById("expense-cats")

   const balInjection = `<span class="money ${data.balance <= 0 ? 'red':'green'}">$${data.balance}</span>`;
   
    incomeCats.innerHTML = "" // Clear the income categories list
    expenseCats.innerHTML = "" // Clear the expense categories list

    // Loop through income categories and update the list
    data.incomeCats.forEach(cat => {
        incomeCats.innerHTML += `<li>${cat.name} - $${cat.value} - ${cat.percentage}%</li>`
    });

    // Loop through expense categories and update the list
    data.expenseCats.forEach(cat => {
        expenseCats.innerHTML += `<li>${cat.name} - $${cat.value} - ${cat.percentage}%</li>`
    });

   // Update balance, income, and expense on the page
   balance.innerHTML = balInjection;
   income.innerHTML = `$${data.income}`;
   expense.innerHTML = `$${data.expense}`;
}

// Handles and parses transaction history data
/**
 * @param {JSON} data - The transaction history data
 */
async function handleTransData(data) {
    /*
        Fetch the table, loop through
        the data, add rows, format the date,
        and then finally add the cells.

        Additionally, while adding rows and cells,
        setup the list of categories. After the table is
        completed, fill out the select menu to filter 
        categories.
    */

    const table = document.getElementById("hist-table");

    let categories = [];
    let i = false;

    // Loop through the transaction data and populate the table
    await data.forEach(async (item) => {
        const newRow = table.insertRow(table.rows.span); // Insert a new row in the table

        let dateObj = new Date(item.date);
        let date = dateObj.toString().split(" G")[0]; // Format the date to string
        if (!categories.includes(item.category)) categories.push(item.category); // Add category to list if not already present

        if(!i) {
            // Set up the first row with transaction details (this is for the most recent transaction)
            document.getElementById("mrt-name").innerHTML = item.name;
            document.getElementById("mrt-amt").innerHTML = item.amount;
            document.getElementById("mrt-date").innerHTML = date;
            document.getElementById("mrt-cat").innerHTML = item.category;
            i = true;
        }

        // Insert the transaction details into the row
        newRow.insertCell(0).innerHTML = item.name;
        newRow.insertCell(1).innerHTML = `<span class="money ${item.amount < 0 ? 'red':''}">$${item.amount}</span>`;
        newRow.insertCell(2).innerHTML = `<span class="money ${item.after < 0 ? 'red':''}">$${item.after}</span>`;
        newRow.insertCell(3).innerHTML = date;
        newRow.insertCell(4).innerHTML = item.category;
        newRow.insertCell(5).innerHTML = item.type;
        newRow.insertCell(6).innerHTML = `<button id="del-${item.id}"><img width="25px" src="./icons/trash.svg" title="delete" alt="delete"></button><button id="edit-${item.id}"><img width="25px" src="./icons/edit.svg" title="edit" alt="edit"></button>`;
        newRow.id = item.id;
    });

    globalData = data; // Save the transaction data globally

    // Fill out the select menu for filtering transactions by category
    const select_menu = document.getElementById("trans-select");
    categories.forEach(category => {
        select_menu.innerHTML += `<option value="${category.toLowerCase()}">${category}</option>`
    });

    // Fill out the form select menu for selecting categories for new transactions
    const transForm = document.getElementById("trans-category");
    categories.forEach(category => {
        transForm.innerHTML += `<option value="${category.toLowerCase()}">${category}</option>`
    });
}

/**
 * Process the form input and return the data in an appropriate format
 * @param {HTMLFormElement} form - The form element containing the transaction data
 */
async function processFormInput(form) {
    let transactionName = form["name"].value;
    let transactionAmount = form["amount"].value;
    let transactionDate = form["date"].value;
    let transactionCategory;
    
    // Check if the user entered a new category or selected an existing one
    if (form['new-category'].value) transactionCategory = form['new-category'].value;
    else transactionCategory = form['category'].value;

    let transactionType = form["type"].value;

    // Return the processed data
    return [
        transactionName,
        transactionAmount.replace("$", ""), // Remove dollar sign from the amount
        transactionCategory,
        transactionType,
        new Date(transactionDate) // Convert the date to a Date object
    ]
}