"""
Project decorators
"""
from typing import Callable

from telegram.update import Update
from telegram.ext import CallbackContext

from .user import User, UserError


def user_required(handler: Callable) -> Callable:
    """
    Every handler must have user as argument.
    Get user from database if it exists else create.
    """
    def decorator(update: Update, context: CallbackContext,
                  *args, **kwargs
                  ):
        try:
            user = User.get_or_create(update.message or update.edited_message)
        except UserError as error:
            return context.bot.send_message(
                chat_id=update.effective_chat.id, text=str(error)
            )
        return handler(user, update, context, *args, **kwargs)
    return decorator
