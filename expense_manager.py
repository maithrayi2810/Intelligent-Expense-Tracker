from datetime import datetime
from database import get_connection


def add_expense(amount, category, description, expense_date):
    """Add a new expense to the database."""

    try:
        amount = float(amount)

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        expense_date = datetime.strptime(
            expense_date, "%Y-%m-%d"
        ).date().isoformat()

        if not category.strip():
            print("Category cannot be empty.")
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO expenses
            (amount, category, description, expense_date)
            VALUES (?, ?, ?, ?)
        """, (
            amount,
            category.strip().title(),
            description.strip(),
            expense_date
        ))

        connection.commit()
        connection.close()

        print("Expense added successfully!")

    except ValueError:
        print("Enter a valid amount and date (YYYY-MM-DD).")


def view_expenses():
    """Display all recorded expenses."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, expense_date
        FROM expenses
        ORDER BY expense_date DESC, id DESC
    """)

    expenses = cursor.fetchall()
    connection.close()

    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\nID | Amount | Category | Description | Date")
    print("-" * 65)

    for expense in expenses:
        print(
            f"{expense[0]} | ₹{expense[1]:.2f} | "
            f"{expense[2]} | {expense[3]} | {expense[4]}"
        )


def search_expenses(category=None, start_date=None, end_date=None):
    """Search expenses by category and/or date range."""

    query = """
        SELECT id, amount, category, description, expense_date
        FROM expenses
        WHERE 1 = 1
    """

    parameters = []

    if category:
        query += " AND category = ?"
        parameters.append(category.strip().title())

    if start_date:
        query += " AND expense_date >= ?"
        parameters.append(start_date)

    if end_date:
        query += " AND expense_date <= ?"
        parameters.append(end_date)

    query += " ORDER BY expense_date DESC"

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, parameters)
    results = cursor.fetchall()
    connection.close()

    if results:
        for expense in results:
            print(expense)
    else:
        print("No matching expenses found.")


def update_expense(expense_id, amount, category, description, expense_date):
    """Update an existing expense."""

    try:
        amount = float(amount)

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        expense_date = datetime.strptime(
            expense_date, "%Y-%m-%d"
        ).date().isoformat()

        if not category.strip():
            print("Category cannot be empty.")
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE expenses
            SET amount = ?,
                category = ?,
                description = ?,
                expense_date = ?
            WHERE id = ?
        """, (
            amount,
            category.strip().title(),
            description.strip(),
            expense_date,
            expense_id
        ))

        connection.commit()

        if cursor.rowcount > 0:
            print("Expense updated successfully!")
        else:
            print("Expense ID not found.")

        connection.close()

    except ValueError:
        print("Enter a valid amount and date (YYYY-MM-DD).")


def delete_expense(expense_id):
    """Delete an expense using its ID."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()

    if cursor.rowcount > 0:
        print("Expense deleted successfully!")
    else:
        print("Expense ID not found.")

    connection.close()