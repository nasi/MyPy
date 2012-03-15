from weakref import proxy


class Cursor(object):
    
    def __init__(self, connection):
        self.connection = proxy(connection)
        self._rows = []
        
    def close(self):
        self.connection = None
    
    def execute(self, query, args=None):
        self.connection.query(query)
        self._rows = self.connection.get_result()
        
    def fetchone(self):
        return tuple(self._rows.pop(0))
    
    def fetchall(self):
        result = tuple(self._rows)
        self._rows = []
        return result