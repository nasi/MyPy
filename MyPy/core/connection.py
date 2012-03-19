from MyPy import pdu
from MyPy.core.cursor import Cursor
from MyPy.core.transport import Transport
from MyPy.constants import client


class Connection(object):
        
    def __init__(self, host='localhost', user='', passwd='', db=None, port=3306,
                 unix_socket=None, charset='', client_flag=0, cursorclass=Cursor,
                 connect_timeout=None):
        self.charset = 'utf8'
        self.charset_number = 33 # 'utf8'
        self.cursorclass = cursorclass

        self.username = user.encode(self.charset)
        self.password = passwd.encode(self.charset)
        self.db = db and db.encode(self.charset) or None
        
        self.client_flag = client_flag
        self.client_flag |= client.CLIENT_CAPABILITIES
        self.client_flag |= client.CLIENT_MULTI_STATEMENTS
        if db is not None:
            self.client_flag |= client.CLIENT_CONNECT_WITH_DB

        self.transport = Transport(host, port, unix_socket)
        self.transport.connect(connect_timeout, callback=self._handshake)
                
    def cursor(self, cursorclass=None):
        return (cursorclass or self.cursorclass)(self)
    
    def close(self):
        if self.transport.is_alive():
            self.transport.send(pdu.QuitPacket)
        self.transport.disconnect()
        
    def query(self, sql):
        self.transport.send(pdu.QueryPacket, self._encode(sql))
    
    def _encode(self, sql):
        if isinstance(sql, unicode):
            return sql.encode(self.charset)
        return sql
    
    def get_result(self):
        header_packet = self.transport.receive(pdu.ResultSetPacket)
        fields = []
        for _ in xrange(header_packet.field_count):
            field_packet = self.transport.receive(pdu.FieldPacket)
            fields.append((field_packet.name, field_packet.type))
        packet = self.transport.receive(pdu.ResultPacket)
        assert isinstance(packet, pdu.EofPacket)
        
        rows = []
        packet = self.transport.receive(pdu.ResultPacket)
        while not isinstance(packet, pdu.EofPacket):
            rows.append(tuple(packet.converted_columns(fields)))
            packet = self.transport.receive(pdu.ResultPacket)
        return rows
    
    def _handshake(self):
        packet0 = self.transport.receive(pdu.GreetingPacket)
        
        if packet0.server_version.startswith('5'):
            self.client_flag |= client.CLIENT_MULTI_RESULTS
        
        self.transport.send(pdu.LoginPacket, self.username, self.password,
                            self.db, self.charset_number, packet0.salt, self.client_flag)
        
        packet1 = self.transport.receive(pdu.ResultPacket)
        if isinstance(packet1, pdu.OkPacket):
            pass
        else:
            pass # error