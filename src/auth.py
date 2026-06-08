import bcrypt
from src.database import create_connection

# ---------------- REGISTER ----------------


def register_user(username, password):

    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            """
        INSERT INTO users(username, password, role, blocked)
        VALUES(?, ?, 'user', 0)
        """,
            (username, hashed_password),
        )

        conn.commit()
        return True

    except Exception as e:
        print("Register error:", e)
        return False

    finally:
        conn.close()


# ---------------- LOGIN ----------------


def login_user(username, password):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT password, role, blocked
    FROM users
    WHERE username=?
    """,
        (username,),
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return "invalid"

    stored_password, role, blocked = user

    # blocked user check
    if blocked == 1:
        return "blocked"

    # bcrypt check (safe conversion)
    if isinstance(stored_password, str):
        stored_password = stored_password.encode()

    if bcrypt.checkpw(password.encode(), stored_password):
        return role

    return "invalid"
