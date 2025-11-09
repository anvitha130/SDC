# database.py
# Simple local SQLite database setup for career-app

import sqlite3

DB_NAME = "career.db"

def create_database():
    """Create the database and queries table if not exists."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            question TEXT,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_query(user, question, answer):
    """Insert a query record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO queries (user, question, answer) VALUES (?, ?, ?)",
                   (user, question, answer))
    conn.commit()
    conn.close()


def get_all_queries(user=None):
    """Fetch all saved queries, or only for a given user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if user:
        cursor.execute("SELECT * FROM queries WHERE user=?", (user,))
    else:
        cursor.execute("SELECT * FROM queries")
    rows = cursor.fetchall()
    conn.close()
    return rows
