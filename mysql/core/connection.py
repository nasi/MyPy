from mysql import pdu
from mysql.core.cursor import Cursor
from mysql.core.transport import Transport


class Connection(object):
        
    def __init__(self, host='localhost', user=None, passwd='', db=None, port=3306,
                 unix_socket=None, charset='', cursorclass=Cursor, connect_timeout=None):
        self.transport = Transport(host, port, unix_socket)
        self.transport.connect(connect_timeout, self._handshake)
        
        self.charset = 'utf8'
        self.cursorclass = cursorclass
    
    def cursor(self, cursorclass=None):
        return (cursorclass or self.cursorclass)(self)
    
    def close(self):
        self.transport.disconnect()
        
    def query(self, sql):
        self.transport.send(pdu.QueryPacket, self._encode(sql))
        self.affected_rows = self._get_result()
        return self.affected_rows
    
    def _encode(self, sql):
        if isinstance(sql, unicode):
            return sql.encode(self.charset)
        return sql
    
    def _get_result(self):
        pass
    
    def _handshake(self):
        self._greeting()         # From server to client during initial handshake
        self._authentication()   # From client to server during initial handshake
    
    def _greeting(self):
        packet = self.transport.receive(pdu.GreetingPacket)
    
    def _authentication(self):
        pass