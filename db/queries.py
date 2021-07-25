"""
Working with db related staff
"""
from typing import Any

from psycopg2 import connect

from config.settings import DB_CONNECTION
from .exceptions import DBError


class WhereInput:
    """
    Class representing where clause in sql query.
    """
    def __init__(self, data: dict) -> None:
        self.data = data

    @property
    def values(self) -> tuple[Any, ...]:
        """
        :return: tuple of passed values used separately in
        sql prepared statement.
        """
        return tuple(self.data.values())

    def __str__(self) -> str:
        """
        String representation of sql WHERE  clause
        :return: Example:
        `WHERE val1=%s, val2=%s`
        """
        if not self.data:
            return ''

        str_repr = 'WHERE'
        for key in self.data.keys():
            str_repr += f' {key}=%s,'

        return str_repr.strip(',')


class DBManager:
    """
    Class for working with db.
    """
    def __init__(self):
        self.connection = connect(**DB_CONNECTION)
        self.cursor = self.connection.cursor()

    def _execute_or_rollback(self, query: str, values: tuple = ()) -> None:
        """
        :param query: sql query
        :param values: values to fill placeholders in query.
        :raise DBException in case of any error during query
            performing.
        """
        try:
            self.cursor.execute(query, values)
        except Exception as error:
            raise DBError(str(error)) from error

    def insert(self, table_name: str, data: dict) -> None:
        """
        Insert data into specified table.
        :param table_name: table to perform query.
        :param data: data to insert in format `{col_name: col_value}`.
        """
        columns = ', '.join(key for key in data.keys())
        values = tuple(data.values())
        placeholders = ', '.join('%s' for _ in values)
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        self._execute_or_rollback(query, values)
        self.connection.commit()

    def select(self, table_name: str, cols: tuple, filters: dict
               ) -> list[tuple[Any]]:
        """
        Select data from specified table.
        :param table_name: table_name: table to perform query.
        :param cols: columns to select from table.
        :param filters: data to form WHERE clause.
        :return: list of tuples. Each tuple represent db row.
        """
        columns = ', '.join(cols)
        where = WhereInput(filters)
        query = f'SELECT {columns} FROM {table_name} {where}'
        self._execute_or_rollback(query, where.values)
        return self.cursor.fetchall()
