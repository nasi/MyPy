
class Cursor(object):
    
    def __init__(self, connection):
        self.connection = connection
        
    def close(self):
        pass
    
    def execute(self, query, args=None):
        pass