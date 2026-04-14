import sqlite3
from datetime import datetime

def save_history(username, expression, result):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            expression TEXT,
            result TEXT,
            time TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO history (username, expression, result, time)
        VALUES (?, ?, ?, ?)
    """, (username, expression, str(result), str(datetime.now())))

    conn.commit()
    conn.close()