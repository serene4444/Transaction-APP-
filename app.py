# Import libraries
from flask import Flask, redirect, request, render_template, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation: List all transactions
@app.route("/")
def get_transactions():
    total_balance = calculate_balance(transactions)
    return render_template("transactions.html", transactions=transactions, total_balance=total_balance)

# Route to display the total balance
@app.route("/balance")
def total_balance():
    balance = calculate_balance(transactions)
    return f"Total Balance: {balance}"


# Create operation: Display add transaction form
# Route to handle the creation of a new transaction
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # Check if the request method is POST
    if request.method == "POST":
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1, # Generate a new ID based on the length of the transactions list
            'date': request.form['date'], # Get the date from the form
            'amount': float(request.form['amount']) # Get the amount from the form and convert it to a float
        }

        # Append the new transaction to the transactions list
        transactions.append(transaction)

        # Redirect to the transactions page after adding the new transaction
        return redirect(url_for('get_transactions'))
    # If the request method is GET, render the add transaction form
    return render_template("form.html")

# Update operation
#Route to handle the update of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # Check if the request method is POST
    if request.method == "POST":
        #Extract the updated transaction details from the form
        date = request.form['date'] # Get the updated date from the form
        amount = float(request.form['amount']) # Get the updated amount from the form and convert it to a float

        # Find the transaction to be updated in the transactions list
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                # Update the transaction details
                transaction['date'] = date # Update the 'date' field of the transaction
                transaction['amount'] = amount # Update the 'amount' field of the transaction
                break # Exit the loop once the transaction is found and updated

        # Redirect to the transactions page after updating the transaction
        return redirect(url_for('get_transactions'))
    # If the request method is GET, find the transaction to be edited and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)
    
    #If the transaction with the given ID is not found, redirect to the transactions page
    return {"message": "Transaction not found"}, 404

# Delete operation: Delete a transaction
# Route to handle the deletion of a transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction to be deleted in the transactions list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction) # Remove the transaction from the list
            break # Exit the loop once the transaction is found and deleted

    # Redirect to the transactions page after deleting the transaction
    return redirect(url_for('get_transactions'))


# Search operation: Search transactions by amount range
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min_amount = float(request.form["min_amount"])
        max_amount = float(request.form["max_amount"])

        filtered_transactions = [
            transaction
            for transaction in transactions
            if min_amount <= transaction["amount"] <= max_amount
        ]

        total_balance = calculate_balance(filtered_transactions)

        return render_template(
            "transactions.html",
            transactions=filtered_transactions,
            total_balance=total_balance
        )
    return render_template("search.html")

    # Helper function to calculate the balance
    def calculate_balance(items):
        return sum(transaction["amount"] for transaction in items)

# Run the Flask app
if __name__ == "__main__":

    app.run(debug=True)
    