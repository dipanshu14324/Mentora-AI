import sqlite3
import os
from datetime import datetime



# =====================================================
# DATABASE PATH
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)


DB_PATH = os.path.join(
    BASE_DIR,
    "chat_history.db"
)


print("\n==============================")
print("CHAT DATABASE PATH:")
print(DB_PATH)
print("==============================\n")





# =====================================================
# CONNECTION
# =====================================================

def get_connection():

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn






# =====================================================
# CREATE TABLES
# =====================================================

def create_tables():

    conn=get_connection()

    cursor=conn.cursor()


    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS chats(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id TEXT NOT NULL,

        session_id TEXT UNIQUE NOT NULL,

        title TEXT DEFAULT 'New Chat',

        created_at TEXT,

        updated_at TEXT

    )
    """
    )


    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS messages(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        session_id TEXT NOT NULL,

        role TEXT NOT NULL,

        content TEXT,

        created_at TEXT,


        FOREIGN KEY(session_id)

        REFERENCES chats(session_id)

        ON DELETE CASCADE

    )
    """
    )


    conn.commit()
    conn.close()



create_tables()







# =====================================================
# CREATE CHAT
# =====================================================

def create_chat(
        user_id,
        session_id,
        question=None
):

    title = "New Chat"

    if question:
        title = question[:40]


    conn = get_connection()

    cursor = conn.cursor()


    try:

        cursor.execute(
            """
            INSERT INTO chats
            (
            user_id,
            session_id,
            title,
            created_at,
            updated_at
            )

            VALUES
            (?,?,?,?,?)

            """,

            (
                user_id,
                session_id,
                title,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            )
        )


        conn.commit()


        print(
            "CHAT CREATED:",
            session_id
        )


    except Exception as e:

        conn.rollback()

        print(
            "CREATE CHAT ERROR:",
            e
        )


    finally:

        conn.close()







# =====================================================
# CHECK CHAT
# =====================================================


def chat_exists(session_id):


    conn=get_connection()

    cursor=conn.cursor()


    cursor.execute(
    """
    SELECT session_id

    FROM chats

    WHERE session_id=?

    """,

    (
        session_id,
    )
    )


    result=cursor.fetchone()


    conn.close()


    return result is not None







# =====================================================
# SAVE MESSAGE
# =====================================================


def save_message(
        session_id,
        role,
        content,
        user_id=None
):


    conn=get_connection()

    cursor=conn.cursor()



    try:


        if not chat_exists(session_id):

            print(
                "CHAT NOT FOUND. CREATING..."
            )


            create_chat(
                "student1",
                session_id
            )




        cursor.execute(
        """
        INSERT INTO messages
        (
            session_id,
            role,
            content,
            created_at
        )

        VALUES
        (?,?,?,?)

        """,

        (

            session_id,

            role,

            content,

            datetime.now().isoformat()

        )
        )




        cursor.execute(
        """
        UPDATE chats

        SET updated_at=?

        WHERE session_id=?

        """,

        (

        datetime.now().isoformat(),

        session_id

        )
        )


        conn.commit()


        print(
            "MESSAGE SAVED:",
            role
        )


    except Exception as e:


        conn.rollback()

        print(
            "SAVE MESSAGE ERROR:",
            e
        )

        raise e



    finally:

        conn.close()







# =====================================================
# GET CHATS
# =====================================================


def get_chats(user_id):


    conn=get_connection()

    cursor=conn.cursor()



    cursor.execute(
    """
    SELECT

    session_id,

    title,

    created_at,

    updated_at


    FROM chats


    WHERE user_id=?


    ORDER BY updated_at DESC

    """,

    (
        user_id,
    )

    )


    rows=cursor.fetchall()



    print(
        "HISTORY RESULT:",
        rows
    )



    conn.close()



    return [

    {

    "session_id":row[0],

    "title":row[1],

    "created_at":row[2],

    "updated_at":row[3]

    }

    for row in rows

    ]








# =====================================================
# GET MESSAGES
# =====================================================


def get_messages(session_id):


    conn=get_connection()

    cursor=conn.cursor()


    cursor.execute(
    """
    SELECT

    role,

    content,

    created_at


    FROM messages


    WHERE session_id=?


    ORDER BY id ASC

    """,

    (
        session_id,
    )
    )


    rows=cursor.fetchall()


    conn.close()


    return [

    {

    "role":row[0],

    "content":row[1],

    "created_at":row[2]

    }

    for row in rows

    ]







# =====================================================
# RENAME
# =====================================================


def rename_chat(
        session_id,
        title
):


    conn=get_connection()

    cursor=conn.cursor()


    cursor.execute(
    """
    UPDATE chats

    SET title=?

    WHERE session_id=?

    """,

    (
        title,
        session_id
    )

    )


    conn.commit()

    conn.close()







# =====================================================
# DELETE
# =====================================================


def delete_chat(session_id):


    conn=get_connection()

    cursor=conn.cursor()


    cursor.execute(
    """
    DELETE FROM chats

    WHERE session_id=?

    """,

    (
        session_id,
    )

    )


    conn.commit()

    conn.close()







# =====================================================
# TITLE GENERATOR
# =====================================================


def generate_title(question):


    q=question.lower()


    keywords={

    "cnn":"CNN Explanation",

    "transformer":"Transformer Explanation",

    "attention":"Attention Mechanism",

    "neural":"Neural Network Basics",

    "gradient":"Gradient Descent",

    "backprop":"Backpropagation"

    }



    for key,value in keywords.items():

        if key in q:

            return value



    return question[:35]