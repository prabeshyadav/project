// // Add Row
// document.getElementById('addRow').addEventListener('click', function() {
//     var tableBody = document.getElementById('tableBody');
//     var rowCount = tableBody.rows.length;
//     var row = tableBody.insertRow(rowCount);
//     var cell1 = row.insertCell(0);
//     var cell2 = row.insertCell(1);
//     var cell3 = row.insertCell(2);
//     var cell4 = row.insertCell(3);
//     var cell5 = row.insertCell(4);
//     cell1.innerHTML = rowCount + 1;  // Adjust row count for display
//     cell2.innerHTML = '<input type="text" name="medicine[]" required>';
//     cell3.innerHTML = '<input type="number" name="quantity[]" oninput="calculateTotal(this)" required>';
//     cell4.innerHTML = '<input type="number" name="price[]" step="0.01" oninput="calculateTotal(this)" required>';
//     cell5.innerHTML = '<input type="number" name="total[]" readonly>';
// });

// // Calculate Total
// function calculateTotal(element) {
//     var row = element.closest('tr');
//     var quantity = parseFloat(row.querySelector('input[name="quantity[]"]').value) || 0;
//     var price = parseFloat(row.querySelector('input[name="price[]"]').value) || 0;
//     var total = quantity * price;
//     row.querySelector('input[name="total[]"]').value = total.toFixed(2);
//     updateTotalAmount();
// }

// // Update Total Amount
// function updateTotalAmount() {
//     var totalAmount = 0;
//     var tableBody = document.getElementById('tableBody');
//     Array.from(tableBody.rows).forEach(function(row) {
//         totalAmount += parseFloat(row.querySelector('input[name="total[]"]').value) || 0;
//     });
//     document.getElementById('totalAmount').value = totalAmount.toFixed(2);
//     updateBalance();
// }

// // Update Balance
// function updateBalance() {
//     var totalAmount = parseFloat(document.getElementById('totalAmount').value) || 0;
//     var paidAmount = parseFloat(document.getElementById('paidAmount').value) || 0;
//     var balanceAmount = paidAmount - totalAmount;
//     document.getElementById('balanceAmount').value = balanceAmount.toFixed(2);
// }
