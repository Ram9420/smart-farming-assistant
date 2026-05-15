import sqlite3
import bcrypt
import re

# =========================
# DATABASE CONNECTION
# =========================
conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# CREATE TABLE
# =========================
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

conn.commit()

# =========================
# USERNAME VALIDATION
# =========================
def validate_username(username):

    # Minimum length
    if len(username) < 5:
        return False, (
            "Username must be at least 5 characters"
        )

    # Allowed characters
    if not re.match(
        r"^[A-Za-z0-9_]+$",
        username
    ):

        return False, (
            "Username can only contain letters, numbers and underscore"
        )

    return True, "Valid"

# =========================
# PASSWORD VALIDATION
# =========================
def validate_password(password):

    # Minimum length
    if len(password) < 8:

        return False, (
            "Password must be at least 8 characters"
        )

    # Uppercase
    if not re.search(r"[A-Z]", password):

        return False, (
            "Password must contain one uppercase letter"
        )

    # Lowercase
    if not re.search(r"[a-z]", password):

        return False, (
            "Password must contain one lowercase letter"
        )

    # Number
    if not re.search(r"[0-9]", password):

        return False, (
            "Password must contain one number"
        )

    # Special character
    if not re.search(r"[@$!%*?&_#]", password):

        return False, (
            "Password must contain one special character"
        )

    return True, "Valid"

# =========================
# REGISTER USER
# =========================
def register_user(username, password):

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()

        return True

    except:
        return False

# =========================
# LOGIN USER
# =========================
def login_user(username, password):

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    data = cursor.fetchone()

    if data:

        stored_password = data[0]

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        ):

            return True

    return False

# =========================
# CREATE PREDICTION TABLE
# =========================
cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    city TEXT,
    crop TEXT,
    confidence REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

# =========================
# SAVE PREDICTION
# =========================
def save_prediction(username, city, crop, confidence):

    cursor.execute(
        '''
        INSERT INTO predictions
        (username, city, crop, confidence)
        VALUES (?, ?, ?, ?)
        ''',
        (username, city, crop, confidence)
    )

    conn.commit()

# =========================
# GET USER HISTORY
# =========================
def get_user_predictions(username):

    cursor.execute(
        '''
        SELECT city, crop, confidence, timestamp
        FROM predictions
        WHERE username=?
        ORDER BY timestamp DESC
        ''',
        (username,)
    )

    return cursor.fetchall()