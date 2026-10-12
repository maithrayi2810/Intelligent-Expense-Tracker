import matplotlib.pyplot as plt
from analyzer import get_expense_data


def category_pie_chart():
    df = get_expense_data()

    if df.empty:
        print("No expenses available to visualize.")
        return

    category_totals = df.groupby("category")["amount"].sum()

    category_totals.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Expense Distribution by Category")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()


def monthly_expense_chart():
    df = get_expense_data()

    if df.empty:
        print("No expenses available to visualize.")
        return

    monthly_totals = df.groupby("month")["amount"].sum()

    monthly_totals.plot(kind="line", marker="o")
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def category_bar_chart():
    df = get_expense_data()

    if df.empty:
        print("No expenses available to visualize.")
        return

    category_totals = df.groupby("category")["amount"].sum()
    category_totals.sort_values(ascending=False).plot(kind="bar")

    plt.title("Category-wise Expense Analysis")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    category_pie_chart()
    monthly_expense_chart()
    category_bar_chart()