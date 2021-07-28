"""
Custom filters
"""
from telegram.ext import MessageFilter
from telegram.message import Message

from config.settings import ADMIN_CHATS


class AdminFilter(MessageFilter):
    """
    Admin command filter.
    """

    def filter(self, message: Message) -> bool:
        """
        Allow to use admin commands only for chats
        specified in ADMIN_CHATS environ variable.
        """
        return message.chat_id in ADMIN_CHATS
