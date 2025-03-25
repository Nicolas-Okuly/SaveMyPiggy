// Transaction History Scripts


document.getElementById("trans-select").addEventListener("input", function (input) {
    /*
        When the select menu in the transaction is selected,
        filter through the table and show only the selected
        category.
    */
    input = input.target.value;

    let filter, table, tr, td, i, txtValue;
    filter = input.toUpperCase();
    table = document.getElementById("hist-table");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        if (input == "sao") {
            tr[i].style.display = "";
            continue;
        }
        td = tr[i].getElementsByTagName("td")[4];
        if (td) {
            txtValue = td.textContent || td.innerText || td.innerHTML;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
});

document.getElementById("trans-search").addEventListener("keyup", function (event) {
    let searchInput, filter, table, tr, td, i, txtValue;

    searchInput = event.target;
    filter = searchInput.value.toUpperCase();
    table = document.getElementById("hist-table");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
});

/**
 * 
 * @param {HTMLButtonElement} button 
 */
function transactionButtonClick(button, deleteTransaction, editTransaction) {
    let action = button.id.split("-")[0];
    let transaction = button.id.split("-")[1];

    globalData.forEach(async item => {
        if (transaction == item.id) {
            if (action == "del") {
                deleteTransaction.deleteTransaction(Number(item.id));
                window.location = window.location;
            } else if (action == "edit") {
                const tableRow = document.getElementById(transaction);
                const cells = tableRow.getElementsByTagName("td");
                let changes = {};

                for (let i = 0; i < cells.length - 1; i++) {
                    if (i === 2 || i === 3) continue;
                    if (i === 5) { // Type selection
                        if (cells[i].getElementsByTagName("select").length > 0) {
                            let select = cells[i].getElementsByTagName("select")[0];
                            let newValue = select.value;
                            if (newValue !== item.type) {
                                changes["type"] = newValue;
                            }
                            cells[i].innerText = newValue;
                        } else {
                            let select = document.createElement("select");
                            let incomeOption = document.createElement("option");
                            incomeOption.value = "income";
                            incomeOption.text = "Income";
                            let expenseOption = document.createElement("option");
                            expenseOption.value = "expense";
                            expenseOption.text = "Expense";
                            
                            select.appendChild(incomeOption);
                            select.appendChild(expenseOption);

                            if (cells[i].innerText === "income") {
                                select.selectedIndex = 0;
                            } else {
                                select.selectedIndex = 1;
                            }

                            cells[i].innerText = "";
                            cells[i].appendChild(select);
                        }
                    } else { // Other input fields
                        if (cells[i].getElementsByTagName("input").length > 0) {
                            let input = cells[i].getElementsByTagName("input")[0];
                            let newValue = input.value.replace("$", "");
                            let key = i === 0 ? "name" : i === 4 ? "category" : "amount";
                            if (newValue !== item[key]) {
                                changes[key] = newValue;
                            }
                            cells[i].innerText = newValue;
                        } else {
                            let input = document.createElement("input");
                            input.type = "text";
                            input.style.width = "max-content";
                            input.value = cells[i].innerText;
                            cells[i].innerText = "";
                            cells[i].appendChild(input);
                        }
                    }
                }

                if (Object.keys(changes).length > 0) {
                    editTransaction.updateTransaction(JSON.stringify({ id: item.id, changes }));
                    window.location = window.location;
                }
            }
        }
    });
}
