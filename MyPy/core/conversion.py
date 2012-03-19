from MyPy.constants import fieldtypes
from MyPy.utils.times import mysql_timestamp_converter, Date_or_None, DateTime_or_None, TimeDelta_or_None

str2set = lambda s: set([i for i in s.split(',') if i])

conversions = {
               
    fieldtypes.FIELD_TYPE_DECIMAL: float,
    fieldtypes.FIELD_TYPE_TINY: int,
    fieldtypes.FIELD_TYPE_SHORT: int,
    fieldtypes.FIELD_TYPE_LONG: long,
    fieldtypes.FIELD_TYPE_FLOAT: float,
    fieldtypes.FIELD_TYPE_DOUBLE: float,
    #fieldtypes.FIELD_TYPE_NULL: ???,
    fieldtypes.FIELD_TYPE_TIMESTAMP: mysql_timestamp_converter,
    fieldtypes.FIELD_TYPE_LONGLONG: long,
    fieldtypes.FIELD_TYPE_INT24: int,
    fieldtypes.FIELD_TYPE_DATE: Date_or_None,
    fieldtypes.FIELD_TYPE_TIME: TimeDelta_or_None,
    fieldtypes.FIELD_TYPE_DATETIME: DateTime_or_None,
    fieldtypes.FIELD_TYPE_YEAR: int,
    #fieldtypes.FIELD_TYPE_NEWDATE: ???,
    fieldtypes.FIELD_TYPE_VARCHAR: unicode,
    fieldtypes.FIELD_TYPE_BIT: int,
    fieldtypes.FIELD_TYPE_NEWDECIMAL: float,
    fieldtypes.FIELD_TYPE_ENUM: unicode,
    fieldtypes.FIELD_TYPE_SET: str2set,
    fieldtypes.FIELD_TYPE_TINY_BLOB: unicode,
    fieldtypes.FIELD_TYPE_MEDIUM_BLOB: unicode,
    fieldtypes.FIELD_TYPE_LONG_BLOB: unicode,
    fieldtypes.FIELD_TYPE_BLOB: unicode,
    fieldtypes.FIELD_TYPE_VAR_STRING: unicode,
    fieldtypes.FIELD_TYPE_STRING: unicode,
    fieldtypes.FIELD_TYPE_GEOMETRY: unicode,       
}


try:
    from decimal import Decimal
    conversions[fieldtypes.FIELD_TYPE_DECIMAL] = Decimal
    conversions[fieldtypes.FIELD_TYPE_NEWDECIMAL] = Decimal
except ImportError:
    pass
