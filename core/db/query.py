
"""Query Module.

Contain the class to launch the connection, obtain the database cursor and finally close the DB connection."""

import psycopg2
import psycopg2.extras
from app import settings
from core.exceptions import DBConnectionError, DBCursorError
from psycopg2.extensions import register_adapter

__author__ = 'cingusoft'


class Query(object):
    """This class prepare the connection with the database.
    is outside the Model class to avoid the python "recursion exceed" problem"."""

    _conn = None
    _curr = None

    def setConnection(self):
        """Launch the pool PostgreSQL connection."""
        if self._conn is None:
            if self._conn is None:
                try:
                    STRINGSTRIP = psycopg2.extensions.new_type(
                            psycopg2.STRING.values,
                        'STRINGSTRIP',
                        lambda value, curs: value.strip())
                    psycopg2.extensions.register_type(STRINGSTRIP)
                    self._conn=psycopg2.connect(database=settings.DATABASE['name'],user=settings.DATABASE['user'],password=settings.DATABASE['password'],host=settings.DATABASE['host'],port=settings.DATABASE['port'])
                except Exception, e:
                    raise DBConnectionError(e)

    def commit(self):
        """Commit to the database."""
        self._conn.commit()

    def getCursor(self):
        """Return the databse cursor."""
        if self._curr is None:
            try:
                self._curr = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            except Exception, e:
                raise DBCursorError(e)
        return self._curr

    def closeCursor(self):
        """Close the Cursors."""
        if self._curr is None:
            try:
                self._curr.close()
                self._curr = None
            except Exception,  e:
                raise DBCursorError(e.pgerror)

    def __del__(self):
        """Class Desctructor"""
        self._conn.close()