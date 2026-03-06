import sqlite3

DB_NAME = "fraud_intelligence.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flagged_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()


def add_flagged_account(account_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO flagged_accounts (account_id) VALUES (?)",
            (account_id,)
        )
    except:
        pass

    conn.commit()
    conn.close()


def is_account_flagged(account_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM flagged_accounts WHERE account_id=?",
        (account_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None