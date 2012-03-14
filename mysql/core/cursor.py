from weakref import proxy


class Cursor(object):
    
    def __init__(self, connection):
        self.connection = proxy(connection)
        
    def close(self):
        self.connection = None
    
    def execute(self, query, args=None):
        self.connection.query(query)