from src.database import create_connection


def add_message(username, question, answer):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats(username,question,answer) VALUES(?,?,?)",
        (username, question, answer)
    )

    conn.commit()

    conn.close()


def get_history(username):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT question, answer FROM chats WHERE username=?",
        (username,)
    )

    history = cursor.fetchall()

    conn.close()

    return history