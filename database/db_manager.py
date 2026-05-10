import sqlite3

DB_NAME = "medassist.db"

def connect_db():

    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )

conn = connect_db()

cursor = conn.cursor()

# ================= USERS =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ================= HISTORY =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    question TEXT,
    answer TEXT
)
""")

conn.commit()

# ================= CREATE USER =================
def create_user(username, password):

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, password)
            VALUES (?, ?)
            """,
            (username, password)
        )

        conn.commit()

        return True

    except:

        return False

# ================= VALIDATE =================
def validate_user(username, password):

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=? AND password=?
        """,
        (username, password)
    )

    return cursor.fetchone()

# ================= SAVE HISTORY =================
def save_history(
    username,
    question,
    answer
):

    cursor.execute(
        """
        INSERT INTO history
        (username, question, answer)
        VALUES (?, ?, ?)
        """,
        (username, question, answer)
    )

    conn.commit()

# ================= LOAD HISTORY =================
def load_history(username):

    cursor.execute(
        """
        SELECT question, answer
        FROM history
        WHERE username=?
        """,
        (username,)
    )

    return cursor.fetchall()