import unittest   
import inspect
from datetime import date, time, datetime
import time as _time

import MyPy
from MyPy.core.connection import Connection
from MyPy.core.cursor import Cursor
from MyPy.constants import fieldtypes


class DatabaseApi2SpecTests(unittest.TestCase):
    
    DATABASE_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'db': 'mypy_test',
    }
     
    def test_module_interface(self):
        self.assertTrue(inspect.isfunction(MyPy.connect))
        conn = MyPy.connect(**self.DATABASE_CONFIG)
        self.assertTrue(isinstance(conn, Connection))
        conn.close()

        self.assertTrue(hasattr(MyPy, 'apilevel'))
        self.assertEquals('2.0', MyPy.apilevel)
        
        self.assertTrue(hasattr(MyPy, 'threadsafety'))
        self.assertTrue(MyPy.threadsafety in range(4))
        self.assertEquals(1, MyPy.threadsafety)
        
        self.assertTrue(hasattr(MyPy, 'paramstyle'))
        expected = ('qmark', 'numeric', 'named', 'format', 'pyformat')
        self.assertTrue(MyPy.paramstyle in expected)
        self.assertEquals('format', MyPy.paramstyle)
        
    def test_exceptions(self):
        self.assertTrue(issubclass(MyPy.Warning, StandardError))
        self.assertTrue(issubclass(MyPy.Error, StandardError))
        
        self.assertTrue(issubclass(MyPy.InterfaceError, MyPy.Error))
        self.assertTrue(issubclass(MyPy.DatabaseError, MyPy.Error))

        self.assertTrue(issubclass(MyPy.DataError, MyPy.DatabaseError))
        self.assertTrue(issubclass(MyPy.OperationalError, MyPy.DatabaseError))
        self.assertTrue(issubclass(MyPy.IntegrityError, MyPy.DatabaseError))
        self.assertTrue(issubclass(MyPy.InternalError, MyPy.DatabaseError))
        self.assertTrue(issubclass(MyPy.ProgrammingError, MyPy.DatabaseError))
        self.assertTrue(issubclass(MyPy.NotSupportedError, MyPy.DatabaseError))

    def test_connection_objects(self):
        conn = MyPy.connect(**self.DATABASE_CONFIG)
    
        self.assertTrue(hasattr(conn, 'close'))
        self.assertTrue(inspect.ismethod(conn.close))
    
        self.assertTrue(hasattr(conn, 'commit'))
        self.assertTrue(inspect.ismethod(conn.commit))
    
        self.assertTrue(hasattr(conn, 'rollback'))
        self.assertTrue(inspect.ismethod(conn.rollback))
    
        self.assertTrue(hasattr(conn, 'cursor'))
        self.assertTrue(inspect.ismethod(conn.cursor))
        self.assertTrue(isinstance(conn.cursor(), Cursor))
        
        conn.close()
        
    def test_cursor_objects(self):
        pass

    def test_type_objects_and_constructors(self):
        self.assertEquals(MyPy.Date(2012, 12, 23), date(2012, 12, 23))
        self.assertEquals(MyPy.Time(16, 23, 45), time(16, 23, 45))
        self.assertEquals(MyPy.Timestamp(2012, 12, 23, 16, 23, 45), 
                          datetime(2012, 12, 23, 16, 23, 45))
        self.assertEquals(MyPy.DateFromTicks(1), date(*_time.localtime(1)[:3]))
        self.assertEquals(MyPy.TimeFromTicks(1), time(*_time.localtime(1)[3:6]))
        self.assertEquals(MyPy.TimestampFromTicks(1), datetime(*_time.localtime(1)[:6]))

        self.assertEquals(MyPy.Binary(u'\u65e5'.encode('utf-8')), 
                          str(u'\u65e5'.encode('utf-8')))
        self.assertTrue(hasattr(MyPy, 'STRING'))
        self.assertTrue(hasattr(MyPy, 'BINARY'))
        self.assertTrue(hasattr(MyPy, 'NUMBER'))
        self.assertTrue(hasattr(MyPy, 'DATETIME'))
        self.assertTrue(hasattr(MyPy, 'ROWID'))
        
        self.assertEquals(MyPy.STRING, MyPy.STRING)
        self.assertNotEquals(MyPy.STRING, MyPy.NUMBER)
        self.assertEquals(fieldtypes.FIELD_TYPE_VAR_STRING, MyPy.STRING)
        self.assertNotEquals(fieldtypes.FIELD_TYPE_DATE, MyPy.NUMBER)


if __name__ == "__main__":
    unittest.main()