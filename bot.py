"""
Script for bot running
"""
from telegram.ext import Updater

from config import settings
from handlers.handlers import register_handlers


def main() -> None:
    """
    Start bot with polling
    """
    updater = Updater(token=settings.API_TOKEN)
    register_handlers(updater.dispatcher)
    updater.start_polling()


if __name__ == '__main__':
    main()
