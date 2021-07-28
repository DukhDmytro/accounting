"""
Business logic connected to category
"""
from collections import namedtuple

from db.queries import DBManager, DBError, DBUniqueViolation
from .exceptions import CategoryError


CategoryInput = namedtuple(
    'CategoryInput', 'codename title description category_type'
)


class Category:
    """
    Class representing income/expense category
    """

    _table_name = 'category'
    _table_cols = (
        'codename',
        'title',
        'description',
        'type',
    )

    def __init__(self, codename: str, title: str, description: str, type: str):
        self.codename = codename
        self.title = title
        self.description = description
        self.type = type

    def save(self) -> 'Category':
        """
        Save category instance to database.
        :raise: CategoryError exception in case of any exception
                raised during sql query execution.
        :return: Category instance.
        """
        try:
            DBManager().insert(self._table_name, self.__dict__)
        except DBUniqueViolation as error:
            raise CategoryError(
                f'Category with codename {self.codename} or title {self.title} already exists'
            ) from error
        except DBError as error:
            raise CategoryError(str(error)) from error

        return self

    @classmethod
    def add_category(cls, context_args: list[str, ]) -> 'Category':
        """
        Create category instance from data specified in user telegram
        message. Save instance to db.
        :param context_args: list of arguments passed as args after command.
        Example: `/add_category test`, where /add_category - command, test - arguments.
        :raise: CategoryError in case of invalid context_args or errors while
                saving category to db.
        :return: Category instance
        """
        category_input = cls._parse_text(context_args)
        category = cls(*category_input)
        return category.save()

    @classmethod
    def get_all(cls, category_type: str = 'expense') -> list['Category', ]:
        """
        Get categories with specified type from db.
        :param category_type: type of category, `expense` by default.
        :raise: CategoryError in case of invalid category type or other errors.
        :return: list of Category instances.
        """
        try:
            categories = DBManager().select(
                cls._table_name, cls._table_cols, {'type': category_type}
            )
        except DBError as error:
            raise CategoryError(str(error)) from error
        return [cls(*category) for category in categories]

    @classmethod
    def get(cls, codename: str) -> 'Category':
        """
        Get category from db by codename.
        :param codename: category codename.
        :raise: CategoryError in category with given codename does not
                exist in db and in case of other errors.
        :return: Category instance.
        """
        try:
            category = DBManager().select(cls._table_name, cls._table_cols, {'codename': codename})
        except DBError as error:
            raise CategoryError(str(error)) from error

        if category:
            return cls(*category[0])
        raise CategoryError(f'Category with codename {codename} does not exist')

    @classmethod
    def update(cls, codename: str = None, data: dict = None,
               context_args: list[str, ] = None) -> 'Category':
        """
        Update category by given codename and data or by given context args.
        :param codename: category codename.
        :param data: dict with keys - category attribute and value - its value.
        :param context_args: text passed by user in telegram message after command.
        :raise CategoryError in case of any exception raised during db updates or
                in case of invalid input data or invalid context_args.
        :return: update Category instance.
        """

        if not (codename and data) and not context_args:
            raise CategoryError('Pass codename and data or context_args')

        if not (data and codename):
            try:
                codename = context_args[0]
                args = context_args[1:]
            except IndexError as error:
                raise CategoryError('Invalid command. See `/admin_help`') from error

            data = {}
            for arg in args:
                try:
                    key, value = arg.split('=')
                except ValueError as error:
                    raise CategoryError('Invalid command. See `/admin_help`') from error

                data[key] = value

        category = cls.get(codename)

        for key, value in data.items():
            if hasattr(category, key):
                setattr(category, key, value)

        try:
            DBManager().update(cls._table_name, data, {'codename': codename})
        except DBError as error:
            raise CategoryError(str(error)) from error
        except DBUniqueViolation as error:
            raise CategoryError(str(error)) from error

        return category

    @staticmethod
    def _parse_text(context_args: list[str, ]) -> CategoryInput:
        """
        Function used to parse `/add_category` command argument.
        Process context_args passed as text ofter command in telegram message.
        `/command context_arg_1 context_arg_2`.
        Arguments are splitted by space. Join arguments to one string, then
        split this string by `|`. Pack splitted values in named tuple and use tham
        to crate Category instance.
        :param context_args: text passed by user as command arguments.
        :raise CategoryError in case of invalid context_args.
        :return: CategoryInput named tuple.

        """
        original_text = ''.join(context_args)
        if not original_text:
            raise CategoryError('Invalid command. See `/admin_help`')

        try:
            text = [item.strip() for item in original_text.split('|')]
            return CategoryInput(*text)
        except (ValueError, TypeError) as error:
            raise CategoryError('Invalid command. See `/admin_help`') from error

    @classmethod
    def delete(cls, codename: str) -> None:
        """
        Delete category with given codename from db.
        :param codename: category codename.
        :raise CategoryError on any exception raised during
               sql query performing.
        :return: None
        """
        db_manager = DBManager()
        if not db_manager.exists(cls._table_name, {'codename': codename}):
            raise CategoryError(f'Category with codename {codename} does not exist')
        try:
            db_manager.delete(cls._table_name, {'codename': codename})
        except DBError as error:
            raise CategoryError(str(error)) from error

    def admin_str(self) -> str:
        """
        :return: String representation of category. Used by admin handlers.
        """
        return f'Codename: {self.codename}. Title: {self.title}.' \
               f'Type: {self.type}. Description: {self.description}'

    def __str__(self) -> str:
        return f'{self.codename}: {self.title}'
