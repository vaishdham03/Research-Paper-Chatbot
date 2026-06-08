from src.database import create_connection


# ---------------- GET USERS ----------------

def get_all_users():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, role, blocked
    FROM users
    """)

    users = cursor.fetchall()

    conn.close()

    return users


# ---------------- GET CHATS ----------------

def get_all_chats():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, question, answer
    FROM chats
    """)

    chats = cursor.fetchall()

    conn.close()

    return chats


# ---------------- BLOCK USER ----------------

def block_user(username):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET blocked=1
    WHERE username=?
    """, (username,))

    conn.commit()

    conn.close()


# ---------------- UNBLOCK USER ----------------

def unblock_user(username):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET blocked=0
    WHERE username=?
    """, (username,))

    conn.commit()

    conn.close()


# ---------------- DELETE USER ----------------

def delete_user(username):

    conn = create_connection()

    cursor = conn.cursor()

    # DELETE CHATS FIRST
    cursor.execute("""
    DELETE FROM chats
    WHERE username=?
    """, (username,))

    # DELETE USER
    cursor.execute("""
    DELETE FROM users
    WHERE username=?
    """, (username,))

    conn.commit()

    conn.close()