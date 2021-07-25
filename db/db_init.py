"""
DB initialization module. Run this module to crate database.
db_init.sql contains sql code which will be executed
"""
# pylint: disable=no-member
from psycopg2 import connect, errors

from config.settings import DB_CONNECTION

if __name__ == '__main__':
    with connect(**DB_CONNECTION) as conn, open('db_init.sql') as sql_commands:
        sql_commands = sql_commands.read().split(';')
        cursor = conn.cursor()
        for command in sql_commands:
            if cleaned_command := command.replace('/n', '').strip():
                print(cleaned_command)
                try:
                    conn.cursor().execute(f'{cleaned_command};')
                except errors.DuplicateObject as err:
                    print('Skipping DuplicateObject exception:', str(err))
                    conn.cursor().execute("ROLLBACK")
