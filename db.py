import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "expenses.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    category TEXT DEFAULT 'uncategorized',
    note TEXT
);
"""

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    with conn:
        conn.executescript(SCHEMA)
    conn.close()

def add_expense(amount, date, category, note):
    conn = get_conn()
    with conn:
        conn.execute(
            "INSERT INTO expenses (amount,date,category,note) VALUES (?,?,?,?)",
            (amount, date, category, note),
        )
    conn.close()

def get_expenses():
    conn = get_conn()
    cur = conn.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_expense(expense_id, amount, date, category, note):
    conn = get_conn()
    with conn:
        conn.execute(
            "UPDATE expenses SET amount=?, date=?, category=?, note=? WHERE id=?",
            (amount, date, category, note, expense_id),
        )
    conn.close()

def delete_expense(expense_id):
    conn = get_conn()
    with conn:
        conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.close()

def total_spent():
    conn = get_conn()
    cur = conn.execute("SELECT SUM(amount) as total FROM expenses")
    total = cur.fetchone()["total"]
    conn.close()
    return round(total or 0.0, 2)

def group_by_category():
    conn = get_conn()
    cur = conn.execute(
        "SELECT category, SUM(amount) as total FROM expenses "
        "GROUP BY category ORDER BY total DESC"
    )
    data = [(r["category"], r["total"]) for r in cur.fetchall()]
    conn.close()
    return data

def group_by_month():
    conn = get_conn()
    cur = conn.execute(
        "SELECT substr(date,1,7) as month, SUM(amount) as total FROM expenses "
        "GROUP BY month ORDER BY month DESC"
    )
    data = [(r["month"], r["total"]) for r in cur.fetchall()]
    conn.close()
    return data
