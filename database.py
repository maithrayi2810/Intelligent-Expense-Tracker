import os
import sqlite3
from pathlib import Path

import psycopg


DATABASE_URL = os.environ.get("DATABASE_URL")


class PostgresCursor:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=()):
        query = query.replace("?", "%s")
        self.cursor.execute(query, params)
        return self

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()


class PostgresConnection:
    def __init__(self, connection):
        self.connection = connection

    def cursor(self):
        return PostgresCursor(self.connection.cursor())

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


def get_connection():
    if DATABASE_URL:
        connection = psycopg.connect(DATABASE_URL)
        return PostgresConnection(connection)

    database_path = Path(__file__).resolve().parent / "expenses.db"
    return sqlite3.connect(database_path)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    if DATABASE_URL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                amount DOUBLE PRECISION NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                expense_date TEXT NOT NULL
            )
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                expense_date TEXT NOT NULL
            )
        """)

    connection.commit()
    connection.close()