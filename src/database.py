import sqlite3

DB_PATH = "database/users.db"


def create_connection():

    conn = sqlite3.connect(DB_PATH)

    return conn


# ---------------- USERS TABLE ----------------


def create_users_table():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB,
        role TEXT DEFAULT 'user',
        blocked INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    for row in cursor.fetchall():
        print(row)
    conn.close()


# ---------------- CHATS TABLE ----------------


def create_chat_table():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        question TEXT,
        answer TEXT
    )
    """)

    conn.commit()

    conn.close()
