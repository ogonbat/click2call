
"""Exception Module for Custome Errors"""

__author__ = 'cingusoft'


class GenericException(Exception):pass

class ObjectDoesNotExist(GenericException):
    """Exception used to except if the query return a value or not."""
    pass
class GrantNotAuthorized(GenericException):
    """Exception used to raise a grant error."""
    pass

class DBConnectionError(GenericException):
    """Exception used to raise a Database Connection Error."""
    pass
class DBCursorError(GenericException):
    """Exception used to raise a Cursor Connection Error."""
    pass
class DBQueryError(GenericException):
    """Exception used to raise a Query Connection Error."""
    pass

class RestMaxCallError(GenericException):
    """Exception used to raise the maximum ongoing call permitted."""
    pass