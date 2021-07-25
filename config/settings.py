"""
Project configurations such as bot configuration,
db configuration and etc.
"""
import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
ADMIN_CHATS = [
    int(chat_id) for chat_id in os.environ.get("ADMIN_CHATS", '').split(',')
    if chat_id
]

DB_CONNECTION = {
    'dbname': os.environ.get("DB_NAME"),
    'password': os.environ.get("DB_PASSWORD"),
    'user': os.environ.get("DB_USER"),
}
