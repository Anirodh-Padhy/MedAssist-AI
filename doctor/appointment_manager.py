import sqlite3

DB_NAME = "medassist.db"

# =========================================================
# DATABASE CONNECTION
# =========================================================

conn = sqlite3.connect(
    DB_NAME,
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute(
    "DROP TABLE IF EXISTS appointments"
)
# =========================================================
# APPOINTMENTS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient TEXT,
    doctor TEXT,
    date TEXT,
    time TEXT,
    reason TEXT,
    status TEXT,
    notes TEXT,
    prescription TEXT
)
""")

conn.commit()

# =========================================================
# BOOK APPOINTMENT
# =========================================================

def book_appointment(
    patient,
    doctor,
    date,
    time,
    reason
):

    cursor.execute(
        """
        INSERT INTO appointments
        (
            patient,
            doctor,
            date,
            time,
            reason,
            status,
            notes,
            prescription
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient,
            doctor,
            date,
            time,
            reason,
            "Pending",
            "",
            ""
        )
    )

    conn.commit()

# =========================================================
# LOAD APPOINTMENTS
# =========================================================

def load_appointments():

    cursor.execute(
        """
        SELECT patient,
               doctor,
               date,
               time,
               reason,
               status,
               notes,
               prescription
        FROM appointments
        """
    )

    return cursor.fetchall()