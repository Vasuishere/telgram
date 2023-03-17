import os
import logging
import sqlite3

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

DB_NAME = 'RegisteredUser.db'
TABLE_NAME = 'users'
TABLE_COLUMNS = ['chat_id', 'branch', 'username']


def create_database():
    if not os.path.isfile(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(f"CREATE TABLE {TABLE_NAME} ({TABLE_COLUMNS[0]} INTEGER PRIMARY KEY, "
                  f"{TABLE_COLUMNS[1]} TEXT, {TABLE_COLUMNS[2]} TEXT)")
        conn.commit()
        conn.close()
        logger.info(f"Database {DB_NAME} created successfully")


def register_user(chat_id: int, branch: str, username: str) -> str:
    if not os.path.isfile(DB_NAME):
        create_database()
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(f"INSERT INTO {TABLE_NAME} ({TABLE_COLUMNS[0]}, {TABLE_COLUMNS[1]}, {TABLE_COLUMNS[2]}) "
                  f"VALUES (?, ?, ?)", (chat_id, branch, username))
        conn.commit()
        conn.close()
        logger.info(f"User {username} registered successfully")
        return "You are now registered."
    except Exception as e:
        logger.error(f"Error registering user {username}: {e}")
        return "An error occurred while registering. Please try again later."


def is_user_registered(chat_id: int) -> bool:
    if not os.path.isfile(DB_NAME):
        create_database()
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(f"SELECT * FROM {TABLE_NAME} WHERE {TABLE_COLUMNS[0]}=?", (chat_id,))
        result = c.fetchone()
        conn.close()
        return bool(result)
    except Exception as e:
        logger.error(f"Error checking if user is registered: {e}")
        return False

def get_user_branch(chat_id):
    conn = sqlite3.connect("RegisteredUser.db")
    cursor = conn.cursor()
    query = "SELECT branch FROM users WHERE chat_id = ?"
    cursor.execute(query, (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None