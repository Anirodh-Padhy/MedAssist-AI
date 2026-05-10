import sqlite3

DB_NAME = "medassist.db"

conn = sqlite3.connect(
    DB_NAME,
    check_same_thread=False
)

cursor = conn.cursor()

# =========================================================
# UPDATE APPOINTMENTS TABLE
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
# UPDATE APPOINTMENT STATUS
# =========================================================

def update_appointment_status(
    patient,
    status
):

    cursor.execute(
        """
        UPDATE appointments
        SET status=?
        WHERE patient=?
        """,
        (
            status,
            patient
        )
    )

    conn.commit()

# =========================================================
# SAVE DOCTOR NOTES
# =========================================================

def save_doctor_notes(
    patient,
    notes,
    prescription
):

    cursor.execute(
        """
        UPDATE appointments
        SET notes=?,
            prescription=?
        WHERE patient=?
        """,
        (
            notes,
            prescription,
            patient
        )
    )

    conn.commit()

# =========================================================
# LOAD APPOINTMENTS
# =========================================================

def load_doctor_appointments():

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