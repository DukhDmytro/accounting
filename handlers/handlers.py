"""
Callback functions for commands and messages
"""
from telegram.ext import CommandHandler, CallbackContext, Dispatcher
from telegram.update import Update

from services import User, user_required


@user_required
def start(user: User, update: Update, context: CallbackContext) -> None:
    """
    Handler for `/start` command
    """
    text = f'Hello, {user.first_name}. I am your accounting bot.'
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text
    )


def register_handlers(dispatcher: Dispatcher) -> None:
    """
    Link handlers with corresponding commands
    """
    dispatcher.add_handler(CommandHandler(['start', 'help'], start))
