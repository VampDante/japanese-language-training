import sqlite3

DB_PATH = "dbs/user_app.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_user_name():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM user_profile ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""

def save_user_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_profile (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def update_user_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM user_profile ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()

    if row:
        cur.execute("UPDATE user_profile SET name = ? WHERE id = ?", (name, row[0]))
    else:
        cur.execute("INSERT INTO user_profile (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()