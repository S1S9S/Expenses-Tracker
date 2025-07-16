import sqlite3
from datetime import datetime

DB_NAME="expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT
    )
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_expense(amount, category, description=""):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cur.execute(
        "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
        (amount,category,today,description)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Добавлен расход: {amount} руб на {category}")

def show_expenses():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, amount, category, date, description FROM expenses ORDER BY date DESC")
    rows = cur.fetchall()
    print("ID | Сумма | Категория | Дата | Описание")
    print("--------------------------------------------")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
    cur.close()
    conn.close()

def report_by_day(date_str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT SUM(amount) FROM expenses WHERE date=?", (date_str,)
    )
    total = cur.fetchone()[0] or 0
    print(f"Всего потрачено за {date_str}: {total} руб")
    cur.close()
    conn.close()

def report_by_month(year, month):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    pattern = f"{year}-{month:02d}-%"
    cur.execute(
        "SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (pattern,)
    )
    total = cur.fetchone()[0] or 0
    print(f"Всего за {year}-{month:02d}: {total} руб")
    cur.close()
    conn.close()

if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) < 2:
        print("Использование")
        print(" python main.py add 500 еда 'обед'")
        print(" python main.py show")
        print(" python main.py day 2025-07-16")
        print(" python main.py month 2025 07")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "add":
        amount = float(sys.argv[2])
        category = sys.argv[3]
        description = sys.argv[4] if len(sys.argv) > 4 else ""
        add_expense(amount, category, description)
    elif cmd == "show":
        show_expenses()
    elif cmd == "day":
        date_str = sys.argv[2]
        report_by_day(date_str)
    elif cmd == "month":
        year = int(sys.argv[2])
        month = int(sys.argv[3])
        report_by_month(year, month)
    else:
        print("Неизвестная команда")