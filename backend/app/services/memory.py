import sqlite3
import os
from datetime import datetime



# =====================================
# Database Path
# =====================================

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)


DB_PATH = os.path.join(
    BASE_DIR,
    "chat_history.db"
)



# =====================================
# Create Database
# =====================================

def create_table():


    conn = sqlite3.connect(
        DB_PATH
    )


    cursor = conn.cursor()



    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_history
        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT,

            session_id TEXT,

            role TEXT,

            message TEXT,

            timestamp TEXT

        )
        """
    )


    conn.commit()

    conn.close()



create_table()





# =====================================
# Message Object
# =====================================

class Message:


    def __init__(
            self,
            msg_type,
            content
    ):

        self.type = msg_type

        self.content = content






# =====================================
# Chat Memory
# =====================================

class ChatMemory:


    def __init__(
            self,
            session_id,
            user_id
    ):

        self.session_id = session_id

        self.user_id = user_id


        self.messages = []


        self.load_history()





    # ------------------------------
    # Load Previous Chat
    # ------------------------------

    def load_history(self):


        conn = sqlite3.connect(
            DB_PATH
        )


        cursor = conn.cursor()



        cursor.execute(

            """
            SELECT role,message
            FROM chat_history

            WHERE user_id=?
            AND session_id=?

            ORDER BY id DESC

            LIMIT 20

            """,

            (
                self.user_id,
                self.session_id
            )

        )


        rows = cursor.fetchall()

        rows.reverse()



        for role,message in rows:


            self.messages.append(

                Message(
                    role,
                    message
                )

            )


        conn.close()






    # ------------------------------
    # Save User Message
    # ------------------------------

    def add_user_message(
            self,
            content
    ):


        self.messages.append(

            Message(
                "user",
                content
            )

        )
        # Keep only recent memory
        if len(self.messages) > 20:

            self.messages = self.messages[-20:]

        





    # ------------------------------
    # Save AI Message
    # ------------------------------

    def add_ai_message(
            self,
            content
    ):


        self.messages.append(

            Message(
                "assistant",
                content
            )

        )
        if len(self.messages) > 20:

            self.messages = self.messages[-20:]

        






    # ------------------------------
    # Insert Database
    # ------------------------------

    def save_message(
            self,
            role,
            message
    ):


        conn = sqlite3.connect(
            DB_PATH
        )


        cursor = conn.cursor()



        cursor.execute(

            """
            INSERT INTO chat_history
            (
                user_id,
                session_id,
                role,
                message,
                timestamp
            )

            VALUES (?,?,?,?,?)

            """,

            (

                self.user_id,

                self.session_id,

                role,

                message,

                datetime.now().isoformat()

            )

        )


        conn.commit()

        conn.close()






# =====================================
# Session Storage
# =====================================

memory_store = {}






def get_history(
        session_id,
        user_id
):


    key = f"{user_id}_{session_id}"



    if key not in memory_store:


        memory_store[key] = ChatMemory(

            session_id,

            user_id

        )



    return memory_store[key]