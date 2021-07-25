"""
Script for bot running
"""
from telegram.ext import Updater
from config import settings
from . import register_handlers


def main() -> None:
    """
    Start bot with polling
    """
    updater = Updater(token=settings.API_TOKEN)
    dispatcher = updater.dispatcher
    register_handlers(dispatcher)
    updater.start_polling()


if __name__ == '__main__':
    main()
