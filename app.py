from flask import Flask, render_template, request, redirect, url_for, flash
from database import initialize_database, get_connection
from datetime import datetime

app = Flask(__name__)
app.secret_key = "expense_tracker_secret_key"

initialize_database()


@app.route("/")
def index():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, expense_date
        FROM expenses
        ORDER BY expense_date DESC, id DESC
    """)
    expenses = cursor.fetchall()

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    total_spending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM expenses")
    total_transactions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)
    category_totals = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total_spending=total_spending,
        total_transactions=total_transactions,
        category_totals=category_totals
    )


@app.route("/add", methods=["POST"])
def add():
    try:
        amount = float(request.form["amount"])
        category = request.form["category"].strip()
        description = request.form.get("description", "").strip()
        expense_date = request.form["expense_date"]

        if amount <= 0:
            flash("Amount must be greater than zero.")
            return redirect(url_for("index"))

        if not category:
            flash("Please enter a category.")
            return redirect(url_for("index"))

        datetime.strptime(expense_date, "%Y-%m-%d")

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO expenses
            (amount, category, description, expense_date)
            VALUES (?, ?, ?, ?)
        """, (amount, category.title(), description, expense_date))

        connection.commit()
        connection.close()

        flash("Expense added successfully!")

    except ValueError:
        flash("Please enter a valid amount and date.")

    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    connection.commit()
    connection.close()

    flash("Expense deleted successfully!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)