import pandas as pd
import numpy as np
from database import get_connection


def get_expense_data():
    connection = get_connection()
    df = pd.read_sql_query(
        "SELECT amount, category, description, expense_date FROM expenses",
        connection
    )
    connection.close()

    if not df.empty:
        df["expense_date"] = pd.to_datetime(df["expense_date"])
        df["month"] = df["expense_date"].dt.to_period("M").astype(str)

    return df


def total_spending():
    df = get_expense_data()
    if df.empty:
        print("No expenses found.")
        return
    print(f"\nTotal Spending: ₹{np.sum(df['amount']):.2f}")


def category_analysis():
    df = get_expense_data()
    if df.empty:
        print("No expenses found.")
        return
    totals = df.groupby("category")["amount"].sum()
    print("\nCategory-wise Spending:")
    print(totals.sort_values(ascending=False).to_string())


def monthly_analysis():
    df = get_expense_data()
    if df.empty:
        print("No expenses found.")
        return
    totals = df.groupby("month")["amount"].sum()
    print("\nMonthly Spending:")
    print(totals.to_string())


def spending_insights():
    df = get_expense_data()
    if df.empty:
        print("No expenses found.")
        return

    totals = df.groupby("category")["amount"].sum()
    largest = df.loc[df["amount"].idxmax()]
    average = np.mean(df["amount"])

    print("\nSpending Insights:")
    print(f"Highest spending category: {totals.idxmax()}")
    print(f"Average transaction amount: ₹{average:.2f}")
    print(
        f"Largest expense: ₹{largest['amount']:.2f} "
        f"({largest['category']})"
    )