from database import initialize_database
from expense_manager import add_expense, view_expenses

initialize_database()

add_expense(
    150,
    "Food",
    "Lunch",
    "2026-10-12"
)

add_expense(
    80,
    "Travel",
    "Bus fare",
    "2026-10-12"
)

add_expense(
    250,
    "Shopping",
    "Notebook and pens",
    "2026-10-12"
)

print("\nDisplaying all expenses:")
view_expenses()