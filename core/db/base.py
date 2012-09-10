
"""Module for the Base Database Model Class."""


from _sha512 import sha512
from uuid import uuid4
from psycopg2._psycopg import IntegrityError
import time
from app.settings import OAUTH2_ACCESS_TOKEN_LENGTH
from core.db.query import Query

from core.exceptions import DBQueryError, ObjectDoesNotExist

__author__ = 'cingusoft'

class ModelBase(object):
    """ModelBase Class.
    Offer basic method for generic queries."""
    _conn = None
    _where_string = None
    _where_value=[]

    def __init__(self,**kw):
        """charge the methos class"""
        for kname,kvalue in kw:
            if hasattr(self.columns,kname):
                self.columns[kname].val = kvalue

    def sql(self,sql,values,fetch=None,multiple=None):
        """Generic SQL Method.

        **ARGS**
        * *sql:* SQL String preformatted
        * *value:* dictionary with the values
        * *fetch:* if is not None the sql return One Row Result
        * *miltiple:* if is not None the sql return a Dictionary of Rows."""

        conn = Query()
        conn.setConnection()
        curr = conn.getCursor()
        results = None
        try:
            curr.execute(sql,values)
            if multiple is not None:
                results = curr.fetchall()
            conn.commit()
            if fetch is not None:
                results = curr.fetchone()
        except IntegrityError, e:
            raise DBQueryError(e)

            #check if have some result
        if curr.rowcount == 0:
            raise ObjectDoesNotExist()
        conn.closeCursor()
        return results


    def get(self,**kw):
        """Select Query.
        If the query don't return a value raise a ObjectDoesNotExist.
        THis method is used to obtain One RowSet."""
        conn = Query()
        conn.setConnection()

        dataValues = dict([(column, value) for column, value in kw.iteritems()])

        keys = dataValues.keys()
        values = [ dataValues[k] for k in keys]
        sqlString = 'SELECT * FROM "{table}" WHERE {where};'.format(
            table = self.__class__.__name__.lower(),
            where = " AND ".join(key+"=%s" for key in keys)
        )
        curr = conn.getCursor()
        try:
            curr.execute(sqlString,values)
            conn.commit()
            results = curr.fetchone()
        except IntegrityError, e:
            raise DBQueryError(e)
        #check if have some result
        if curr.rowcount == 0:
            raise ObjectDoesNotExist()
        conn.closeCursor()
        return results


    def where(self,**kw):
        """WHERE Query.
        Preformat a WHERE instance for the queries."""
        dataValues = dict([(column, value) for column, value in kw.iteritems()])
        keys = dataValues.keys()
        values = [ dataValues[k] for k in keys]
        whereString = 'WHERE {where}'.format(
            where = " AND ".join(key+"=%s" for key in keys)
        )
        self._where_string = whereString
        self._where_value = values

    def insert(self,**kw):
        """INSERT Query.
        The **kw correspind to the column name and instance the attributes automatically.
        Generate a correspondent INSERT Query without preconfigured SQL String."""
        conn = Query()
        conn.setConnection()
        dataValues = dict([(column, value) for column, value in kw.iteritems()])
        keys = dataValues.keys()
        values = [ dataValues[k] for k in keys]
        sqlString = 'INSERT INTO "{table}"({ins_key}) VALUES ({ins_values});'.format(
            table = self.__class__.__name__.lower(),
            ins_key = " , ".join(key for key in keys),
            ins_values = ",".join("%s" for key in keys)
        )
        curr = conn.getCursor()
        try:
            curr.execute(sqlString,values)
            conn.commit()
        except IntegrityError, e:
            raise DBQueryError(e)
            #check if have some result
        conn.closeCursor()

    def _update(self,**kw):
        """UPDATE Query.
        Like insert generate a preconfigured sql string and quote the values.
        Check if a preconfigured WHERE string is preformatted and charge it to the query update."""
        if self._where_string is None:
            raise DBQueryError(e)

        conn = Query()
        conn.setConnection()

        dataValues = dict([(column, value) for column, value in kw.iteritems()])
        keys = dataValues.keys()
        values = [ dataValues[k] for k in keys]
        sqlString = 'UPDATE "{table}" SET {set} {where};'.format(
            table = self.__class__.__name__.lower(),
            set = " , ".join(key+"=%s" for key in keys),
            where = self._where_string
        )
        final_values = sum([values, self._where_value], [])
        curr = conn.getCursor()
        try:
            curr.execute(sqlString,final_values)
            conn.commit()
        except IntegrityError, e:
            raise DBQueryError(e)
            #check if have some result
        conn.closeCursor()

    def _genHashString(self):
        """Method outside the Database to Genrate HashString for Code and Token values."""
        return sha512(uuid4().hex).hexdigest()[0:OAUTH2_ACCESS_TOKEN_LENGTH]