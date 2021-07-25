"""
Business logic connected to user
"""
from telegram.message import Message

from db.queries import DBManager
from db.exceptions import DBError
from .exceptions import UserError


class User:
    """
    Class representing telegram user.
    """
    _table_name = 'telegram_user'
    _table_cols = (
        'chat_id',
        'is_bot',
        'first_name',
        'last_name',
        'username',
        'language_code',
    )

    def __init__(self, chat_id: int, is_bot: bool, first_name: str,
                 last_name: str = None, username: str = None,
                 language_code: str = None
                 ) -> None:
        self.chat_id = chat_id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code

    @property
    def name(self) -> str:
        """
        :return: Users full name.
        """
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.first_name

    def save(self) -> 'User':
        """
        Save user instance to db
        """
        try:
            DBManager().insert(self._table_name, self.__dict__)
        except DBError as error:
            raise UserError('Please try again later.') from error
        return self

    @classmethod
    def get_or_create(cls, message: Message) -> 'User':
        """
        Try to find user in db. If user does not exists
        create new user in db.
        :param message: Telegram message from user.
        :return: User instance.
        """
        try:
            user_rows = DBManager().select(
                cls._table_name, cls._table_cols, {'chat_id': message.chat_id}
            )
        except DBError as error:
            raise UserError('Please try again later.') from error
        if user_rows:
            return User(*user_rows[0])

        message_user = message.from_user
        user = cls(
            chat_id=message_user.id,
            is_bot=message_user.is_bot,
            first_name=message_user.first_name,
            last_name=message_user.last_name,
            username=message_user.username,
            language_code=message_user.language_code,
        ).save()

        return user

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.chat_id} {self.name}'
