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
function transactionButtonClick(button) {
    let transaction = button.id;
    
}