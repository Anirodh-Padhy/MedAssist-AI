import sqlite3

DB_NAME = "medassist.db"

conn = sqlite3.connect(
    DB_NAME,
    check_same_thread=False
)

cursor = conn.cursor()

# =========================================================
# LOAD USERS
# =========================================================

def load_users():

    cursor.execute(
        """
        SELECT username,
               role,
               approved
        FROM users
        """
    )

    return cursor.fetchall()

# =========================================================
# DELETE USER
# =========================================================

def delete_user(username):

    cursor.execute(
        """
        DELETE FROM users
        WHERE username=?
        """,
        (username,)
    )

    conn.commit()

# =========================================================
# LOAD ALL APPOINTMENTS
# =========================================================

def load_all_appointments():

    cursor.execute(
        """
        SELECT patient,
               doctor,
               date,
               time,
               reason,
               status
        FROM appointments
        """
    )

    return cursor.fetchall()

# =========================================================
# LOAD DOCTORS
# =========================================================

def load_doctors():

    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE role='Doctor'
        AND approved=1
        """
    )

    doctors = cursor.fetchall()

    return [
        f"Dr. {d[0]}"
        for d in doctors
    ]

# =========================================================
# LOAD PENDING DOCTORS
# =========================================================

def load_pending_doctors():

    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE role='Doctor'
        AND approved=0
        """
    )

    return cursor.fetchall()

# =========================================================
# APPROVE DOCTOR
# =========================================================

def approve_doctor(username):

    cursor.execute(
        """
        UPDATE users
        SET approved=1
        WHERE username=?
        """,
        (username,)
    )

    conn.commit()