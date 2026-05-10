import streamlit as st
import sqlite3
import bcrypt
import jwt
import datetime
import re

# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect(
    "medassist.db",
    check_same_thread=False
)

cursor = conn.cursor()


# =========================================================
# USERS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password BLOB,
    role TEXT,
    approved INTEGER
)
""")

conn.commit()

# =========================================================
# SECRET KEY
# =========================================================

SECRET_KEY = "medassist_secret_key"

# =========================================================
# PASSWORD VALIDATION
# =========================================================

def validate_password(password):

    if len(password) < 8:

        return (
            False,
            "Password must be at least 8 characters long."
        )

    if not re.search(r"[A-Z]", password):

        return (
            False,
            "Password must contain one uppercase letter."
        )

    if not re.search(r"[a-z]", password):

        return (
            False,
            "Password must contain one lowercase letter."
        )

    if not re.search(r"[0-9]", password):

        return (
            False,
            "Password must contain one number."
        )

    return (
        True,
        "Valid Password"
    )

# =========================================================
# HASH PASSWORD
# =========================================================

def hash_password(password):

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

# =========================================================
# VERIFY PASSWORD
# =========================================================

def verify_password(
    password,
    hashed_password
):

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password
    )

# =========================================================
# CREATE TOKEN
# =========================================================

def create_token(
    username,
    role
):

    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=12)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token

# =========================================================
# LOGIN UI
# =========================================================

def login_ui():

    st.subheader("🔐 Login System")

    auth_mode = st.radio(
        "Select",
        [
            "Login",
            "Register"
        ]
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Role",
        [
            "Patient",
            "Doctor",
            "Admin"
        ]
    )

    # =====================================================
    # REGISTER
    # =====================================================

    if auth_mode == "Register":

        if st.button("Register"):

            if username == "" or password == "":

                st.error(
                    "Username and password required."
                )

                return

            is_valid, message = validate_password(
                password
            )

            if not is_valid:

                st.error(message)

                return

            cursor.execute(
                """
                SELECT * FROM users
                WHERE username=?
                """,
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                st.error(
                    "Username already exists."
                )

                return

            hashed_password = hash_password(
                password
            )

            approved = (
                0 if role == "Doctor" else 1
            )

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    password,
                    role,
                    approved
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    username,
                    hashed_password,
                    role,
                    approved
                )
            )

            conn.commit()

            if role == "Doctor":

                st.warning(
                    "Doctor account registered. Waiting for admin approval."
                )

            else:

                st.success(
                    "Registration successful!"
                )

    # =====================================================
    # LOGIN
    # =====================================================

    else:

        if st.button("Login"):

            cursor.execute(
                """
                SELECT password,
                       role,
                       approved
                FROM users
                WHERE username=?
                """,
                (username,)
            )

            result = cursor.fetchone()

            if result is None:

                st.error(
                    "User not found."
                )

                return

            stored_password, stored_role, approved = result

            if verify_password(
                password,
                stored_password
            ):

                # =========================================
                # DOCTOR APPROVAL CHECK
                # =========================================

                if (
                    stored_role == "Doctor"
                    and approved == 0
                ):

                    st.warning(
                        "Doctor account pending admin approval."
                    )

                    return

                token = create_token(
                    username,
                    stored_role
                )

                st.session_state.logged_in = True

                st.session_state.username = username

                st.session_state.role = stored_role

                st.session_state.token = token

                st.success(
                    "Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid password."
                )