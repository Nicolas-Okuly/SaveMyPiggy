// Define communication objects
let sendBalance;
let sendTrans;
let updateGraphs;
let receiveTransaction;
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

    sendTrans.sendTransHistory.connect(function (message) {
        // Format the message to JSON and send it to the handler function.
        handleTransData(JSON.parse(message));
    });

    sendBalance.receiveBalanceData("alltime");
    sendTrans.receiveTransHistory();
    updateGraphs.updateGraph("alltime");

    document.getElementById("income-filter").addEventListener("change", (change) => {
        updateGraphs.updateGraph(change.target.value);
    });

    document.getElementById("transaction-form").addEventListener("submit", (event) => {
        let element = event.target;
        let data = processFormInput(element);
        receiveTransaction.receiveTransactionData(data);
    })
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

   const balInjection = `<span class="money ${data.balance < 0 ? 'red':''}">$${data.balance}</span>`;


    data.incomeCats.forEach(cat => {
        incomeCats.innerHTML += `<li>${cat.name} - $${cat.value} - %${cat.percentage}</li>`
    });

    data.expenseCats.forEach(cat => {
        expenseCats.innerHTML += `<li>${cat.name} - $${cat.value} - %${cat.percentage}</li>`
    });

   balance.innerHTML += balInjection;
   income.innerHTML += `${data.income}`;
   expense.innerHTML += `${data.expense}`;
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
    await data.forEach(async (item) => {
        const newRow = table.insertRow(table.rows.span);

        let dateObj = new Date(item.date);
        let date = `${dateObj.getMonth() + 1}/${dateObj.getDay()}/${dateObj.getFullYear()}`;

        if (!categories.includes(item.category)) categories.push(item.category);

        newRow.insertCell(0).innerHTML = item.name;
        newRow.insertCell(1).innerHTML = `<span class="money ${item.cost < 0 ? 'red':''}">$${item.cost}</span>`;
        newRow.insertCell(2).innerHTML = `<span class="money ${item.after < 0 ? 'red':''}">$${item.after}</span>`;
        newRow.insertCell(3).innerHTML = date;
        newRow.insertCell(4).innerHTML = item.category;
        newRow.insertCell(5).innerHTML = item.type;
        newRow.insertCell(6).innerHTML = `<button id="del-${dateObj.getTime()}"><img width="25px" src="./icons/trash.svg" title="delete" alt="delete"></button><button id="edit-${dateObj.getTime()}"><img width="25px" src="./icons/edit.svg" title="edit" alt="edit"></button>`;
    });

    globalData = data;

    const select_menu = document.getElementById("trans-select");
    categories.forEach(category => {
        select_menu.innerHTML += `<option value="${category.toLowerCase()}">${category}</option>`
    });

    await document.querySelectorAll("button").forEach(async (button) => {
        await button.addEventListener("click", async (event) => {
            transactionButtonClick(button); // Declared in transactions.js
        });
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

    return {
        name: transactionName,
        amount: transactionAmount,
        date: transactionDate,
        category: transactionCategory,
        type: transactionType
    }
}