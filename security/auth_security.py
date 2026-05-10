import bcrypt
import jwt
import datetime

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

# =========================================================
# PASSWORD VERIFY
# =========================================================

def verify_password(
    password,
    hashed_password
):

    return bcrypt.checkpw(
        password.encode(),
        hashed_password
    )

# =========================================================
# JWT TOKEN
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
# VERIFY TOKEN
# =========================================================

def verify_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except:

        return None