"""
Callback functions for commands and messages
"""
from telegram.ext import CommandHandler, MessageHandler, Filters


def start(update, context):
    """
    Handler for `/start` command
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def echo(update, context):
    """
    Echo messages with no commands from user
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


def register_handlers(dispatcher):
    """
    Link handlers with corresponding commands
    """
    dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), echo)
    )
    dispatcher.add_handler(CommandHandler(['start', 'help'], start))
