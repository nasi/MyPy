import time
import datetime

from MyPy.core.exceptions import (
    Warning, Error, InterfaceError, DatabaseError, DataError, OperationalError,
    IntegrityError, InternalError, ProgrammingError, NotSupportedError
)
from MyPy.constants import fieldtypes


apilevel = '2.0'
threadsafety = 1
paramstyle = 'format'

def Connect(*args, **kwargs):
    from MyPy.core.connection import Connection
    return Connection(*args, **kwargs)

connect = Connection = Connect

Date = datetime.date
Time = datetime.time
Timestamp = datetime.datetime

def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])

def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])

def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])

Binary = str

class DBAPITypeObject:

    def __init__(self, *values):
        self.values = values
        
    def __cmp__(self, other):
        if other in self.values:
            return 0
        if other < self.values:
            return 1
        else:
            return -1
        
STRING   = DBAPITypeObject(fieldtypes.FIELD_TYPE_ENUM, fieldtypes.FIELD_TYPE_STRING,
                           fieldtypes.FIELD_TYPE_VAR_STRING)
BINARY   = DBAPITypeObject(fieldtypes.FIELD_TYPE_BLOB, fieldtypes.FIELD_TYPE_LONG_BLOB,
                           fieldtypes.FIELD_TYPE_MEDIUM_BLOB, fieldtypes.FIELD_TYPE_TINY_BLOB)
NUMBER   = DBAPITypeObject(fieldtypes.FIELD_TYPE_DECIMAL, fieldtypes.FIELD_TYPE_DOUBLE,
                           fieldtypes.FIELD_TYPE_FLOAT, fieldtypes.FIELD_TYPE_INT24,
                           fieldtypes.FIELD_TYPE_LONG, fieldtypes.FIELD_TYPE_LONGLONG,
                           fieldtypes.FIELD_TYPE_TINY, fieldtypes.FIELD_TYPE_YEAR)
DATETIME = DBAPITypeObject(fieldtypes.FIELD_TYPE_DATETIME, fieldtypes.FIELD_TYPE_TIMESTAMP)
ROWID    = DBAPITypeObject()   


__all__ = [
    'Connect', 'Connection', 'connect', 'apilevel', 'threadsafety', 'paramstyle',
    'Error', 'Warning', 'InterfaceError', 'DatabaseError', 'DataError',
    'OperationalError', 'IntegrityError', 'InternalError', 'ProgrammingError',
    'NotSupportedError', 'Date', 'Time', 'Timestamp', 'Binary', 'DateFromTicks',
    'DateFromTicks', 'TimestampFromTicks', 'STRING', 'BINARY', 'NUMBER',
    'DATETIME', 'ROWID',
]
