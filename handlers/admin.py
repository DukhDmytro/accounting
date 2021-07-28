"""
Callback functions for admin commands
"""
from telegram.ext import CommandHandler, CallbackContext, Dispatcher
from telegram.update import Update

from services import User, Category, CategoryError, user_required
from .filters import AdminFilter


@user_required
def admin_help(user: User, update: Update, context: CallbackContext):
    """
    Handler for `/admin_help` command. Send list of admin commands.
    """
    text = f"""Hello, {user.first_name}. Admin commands"""
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text
    )


@user_required
def admin_create_category(user: User, update: Update, context: CallbackContext):
    """
    Handler for `/create_category` command.
    Command example `/create_category <codename>|<title>|<description>|<type>`
    """
    try:
        category = Category.add_category(context.args)
    except CategoryError as error:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(error)
        )
        return

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f'Category added.\n{category}'
    )


@user_required
def admin_categories(user: User, update: Update, context: CallbackContext):
    """
    Handler for `/admin_categories` command. Sends message with categories list.
    Command example: `/admin_categories <category_type>`
    """
    try:
        category_type = context.args[0] if context.args else 'expense'
        categories = Category.get_all(category_type)
    except CategoryError as error:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(error)
        )
        return

    text = '\n'.join(category.admin_str() for category in categories)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=str(text)
    )


@user_required
def admin_update_category(user: User, update: Update, context: CallbackContext):
    """
    Handler for `/update_category` command.
    Command example: `/update_category <codename> <key>=<value> <key>=<value>`
    """
    if not context.args:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Invalid command. See `/admin_help`'
        )
        return

    try:
        category = Category.update(context_args=context.args)
    except CategoryError as error:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(error)
        )
        return

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f'Category updated\n{category.admin_str()}'
    )


@user_required
def admin_delete_category(user: User, update: Update, context: CallbackContext):
    """
    Handler for delete `/delete_category` command.
    Command example: `/delete_category <codename>`
    """
    codename = context.args[0] if context.args else ''

    try:
        Category.delete(codename)
    except CategoryError as error:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(error)
        )
        return

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f'Category {codename} deleted'
    )


def register_admin_handlers(dispatcher: Dispatcher) -> None:
    """
    Link handlers with corresponding commands
    """
    dispatcher.add_handler(
        CommandHandler(['admin_help'], admin_help, filters=AdminFilter())
    )
    dispatcher.add_handler(
        CommandHandler(['add_category'], admin_create_category, filters=AdminFilter())
    )
    dispatcher.add_handler(
        CommandHandler(['admin_categories'], admin_categories, filters=AdminFilter())
    )
    dispatcher.add_handler(
        CommandHandler(['update_category'], admin_update_category, filters=AdminFilter())
    )
    dispatcher.add_handler(
        CommandHandler(['delete_category'], admin_delete_category, filters=AdminFilter())
    )
