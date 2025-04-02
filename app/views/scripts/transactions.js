// Event listener for the transaction category filter
document.getElementById("trans-select").addEventListener("input", function (input) {
    /*
        When the select menu in the transaction filter is selected,
        filter through the transaction table and display only the 
        selected category.
    */
    input = input.target.value;

    let filter, table, tr, td, i, txtValue;
    filter = input.toUpperCase();
    table = document.getElementById("hist-table");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        // If 'sao' is selected, show all rows
        if (input == "sao") {
            tr[i].style.display = "";
            continue;
        }
        td = tr[i].getElementsByTagName("td")[4]; // Get the category cell
        if (td) {
            txtValue = td.textContent || td.innerText || td.innerHTML;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = ""; // Show row if category matches filter
            } else {
                tr[i].style.display = "none"; // Hide row if category doesn't match
            }
        }
    }
});

// Event listener for the search input in the transaction history
document.getElementById("trans-search").addEventListener("keyup", function (event) {
    let searchInput, filter, table, tr, td, i, txtValue;

    searchInput = event.target;
    filter = searchInput.value.toUpperCase();
    table = document.getElementById("hist-table");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0]; // Search by name (first column)
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = ""; // Show row if name matches search input
            } else {
                tr[i].style.display = "none"; // Hide row if name doesn't match
            }
        }
    }
});

/**
 * Handles click events for the transaction buttons (delete or edit)
 * @param {HTMLButtonElement} button - The button that was clicked (delete or edit)
 * @param {Object} deleteTransaction - The delete transaction function object
 * @param {Object} editTransaction - The edit transaction function object
 */
function transactionButtonClick(button, deleteTransaction, editTransaction) {
    let action = button.id.split("-")[0]; // Extract action (del or edit) from button id
    let transaction = button.id.split("-")[1]; // Extract transaction ID from button id

    // Loop through global transaction data to find the matching transaction
    globalData.forEach(async item => {
        if (transaction == item.id) {
            if (action == "del") {
                // If delete is clicked, delete the transaction and reload the page
                deleteTransaction.deleteTransaction(Number(item.id));
                window.location = window.location;
            } else if (action == "edit") {
                // If edit is clicked, allow editing the transaction's data
                const tableRow = document.getElementById(transaction);
                const cells = tableRow.getElementsByTagName("td");
                let changes = {};

                // Loop through the table row cells for editable fields
                for (let i = 0; i < cells.length - 1; i++) {
                    if (i === 2 || i === 3) continue; // Skip date and after fields

                    if (i === 5) { // Type selection (income or expense)
                        if (cells[i].getElementsByTagName("select").length > 0) {
                            let select = cells[i].getElementsByTagName("select")[0];
                            let newValue = select.value;
                            if (newValue !== item.type) {
                                changes["type"] = newValue;
                            }
                            cells[i].innerText = newValue;
                        } else {
                            // Create a select element for type (income/expense)
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
                    } else { // Other fields (name, category, amount)
                        if (cells[i].getElementsByTagName("input").length > 0) {
                            let input = cells[i].getElementsByTagName("input")[0];
                            let key = i === 0 ? "name" : i === 4 ? "category" : "amount";
                            let newValue;

                            if (key === "amount") {
                                // For amount field, apply regex to validate numeric input
                                let pattern = /\d+(\.\d+)?/g;
                                const matches = input.value.match(pattern);
                                if (matches && matches.length > 0) {
                                    newValue = Number(matches.join(''));
                                } else {
                                    newValue = item[key]; // Fallback to original value if invalid
                                }
                            } else {
                                // For other fields, use the input value directly
                                newValue = input.value.trim() || item[key];
                            }

                            if (newValue !== item[key]) {
                                changes[key] = newValue;
                            }
                            cells[i].innerText = newValue;
                        } else {
                            // If input element doesn't exist, create one for editing
                            let input = document.createElement("input");
                            input.type = "text";
                            input.style.width = "max-content";
                            input.value = cells[i].innerText;
                            cells[i].innerText = "";
                            cells[i].appendChild(input);
                        }
                    }
                }

                // If there were any changes, update the transaction and reload the page
                if (Object.keys(changes).length > 0) {
                    editTransaction.updateTransaction(JSON.stringify({ id: item.id, changes }));
                    window.location = window.location;
                }
            }
        }
    });
}