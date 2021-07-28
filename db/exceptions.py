"""
DB related exceptions
"""


class DBError(Exception):
    """
    Exception raised on any exception
    raised during sql query performing
    """


class DBUniqueViolation(Exception):
    """
    Exception raised on database unique violation error
    raised during sql query performing
    """
