// Define communication objects
let sendBalance;
let sendTrans;
let updateGraphs;
let receiveTransaction;
let deleteTransaction;
let editTransaction;
var globalData;

// Create the web channel
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

    sendBalance.sendBalanceData.connect(function (message) {
        // Format the message to JSON and send it to the handler function.
        handleBalData(JSON.parse(message));
    });

    updateGraphs.updateGraphSignal.connect(function () {
        // Reload all images
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            const src = img.src;
            const timestamp = new Date().getTime();
            img.src = src.split('?')[0] + '?' + timestamp;
        });
    });

    sendTrans.sendTransHistory.connect(async function (message) {
        // Format the message to JSON and send it to the handler function.
        handleTransData(JSON.parse(message));

        await document.querySelectorAll("button").forEach(async (button) => {
            await button.addEventListener("click", async (event) => {
                transactionButtonClick(button, deleteTransaction, editTransaction); // Declared in transactions.js
            });
        });
    });

    sendBalance.receiveBalanceData("alltime");
    sendTrans.receiveTransHistory();
    updateGraphs.updateGraph("alltime");

    document.getElementById("income-filter").addEventListener("change", (change) => {
        updateGraphs.updateGraph(change.target.value);
        sendBalance.receiveBalanceData(change.target.value);
    });

    document.getElementById("transaction-form").addEventListener("submit", async (event) => {
        let element = event.target;
        let data = await processFormInput(element);
        receiveTransaction.receiveTransactionData(JSON.stringify(data));
    });
});

// Handles all balance data
/**
 * 
 * @param {JSON} data 
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
   
    incomeCats.innerHTML = ""
    expenseCats.innerHTML = ""

    data.incomeCats.forEach(cat => {
        incomeCats.innerHTML += `<li>${cat.name} - $${cat.value} - ${cat.percentage}%</li>`
    });

    data.expenseCats.forEach(cat => {
        expenseCats.innerHTML += `<li>${cat.name} - $${cat.value} - ${cat.percentage}%</li>`
    });

   balance.innerHTML = balInjection;
   income.innerHTML = `$${data.income}`;
   expense.innerHTML = `$${data.expense}`;
}

// Handles and parses transaction data.
/**
 * 
 * @param {JSON} data 
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
    await data.forEach(async (item) => {
        const newRow = table.insertRow(table.rows.span);

        let dateObj = new Date(item.date);
        let date = dateObj.toString().split(" G")[0];
        if (!categories.includes(item.category)) categories.push(item.category);

        if(!i) {
            document.getElementById("mrt-name").innerHTML = item.name;
            document.getElementById("mrt-amt").innerHTML = item.amount;
            document.getElementById("mrt-date").innerHTML = date;
            document.getElementById("mrt-cat").innerHTML = item.category;
            i = true;
        }

        newRow.insertCell(0).innerHTML = item.name;
        newRow.insertCell(1).innerHTML = `<span class="money ${item.amount < 0 ? 'red':''}">$${item.amount}</span>`;
        newRow.insertCell(2).innerHTML = `<span class="money ${item.after < 0 ? 'red':''}">$${item.after}</span>`;
        newRow.insertCell(3).innerHTML = date;
        newRow.insertCell(4).innerHTML = item.category;
        newRow.insertCell(5).innerHTML = item.type;
        newRow.insertCell(6).innerHTML = `<button id="del-${item.id}"><img width="25px" src="./icons/trash.svg" title="delete" alt="delete"></button><button id="edit-${item.id}"><img width="25px" src="./icons/edit.svg" title="edit" alt="edit"></button>`;
        newRow.id = item.id;
    });

    globalData = data;

    const select_menu = document.getElementById("trans-select");
    categories.forEach(category => {
        select_menu.innerHTML += `<option value="${category.toLowerCase()}">${category}</option>`
    });

    const transForm = document.getElementById("trans-category");
    categories.forEach(category => {
        transForm.innerHTML += `<option value="${category.toLowerCase()}">${category}</option>`
    });
}

/**
 * 
 * @param {HTMLFormElement} form 
 */
async function processFormInput(form) {
    let transactionName = form["name"].value;
    let transactionAmount = form["amount"].value;
    let transactionDate = form["date"].value;
    let transactionCategory;
    
    if (form['new-category'].value) transactionCategory = form['new-category'].value;
    else transactionCategory = form['category'].value;

    let transactionType = form["type"].value;

    return [
        transactionName,
        transactionAmount.replace("$", ""),
        transactionCategory,
        transactionType,
        new Date(transactionDate)
    ]
}