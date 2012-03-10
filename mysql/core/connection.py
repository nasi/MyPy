import socket
import struct

from mysql import pdu
from mysql.core.cursor import Cursor
from mysql.core.exceptions import OperationalError, ProgrammingError
from mysql.constants import connectionerrors


class Connection(object):
    
    DEBUG = True
    
    def __init__(self, host='localhost', user=None, passwd='', db=None, port=3306,
                 unix_socket=None, charset='', cursorclass=Cursor, connect_timeout=None):
        self._connect(host, port, unix_socket, connect_timeout)
        self.charset = 'utf8'
        self.cursorclass = cursorclass
    
    def cursor(self, cursorclass=None):
        return (cursorclass or self.cursorclass)(self)
    
    def close(self):
        if self._socket is not None:
            self._send(pdu.QuitPacket)
            
            for obj in (self._wfile, self._rfile, self._socket):
                obj.close()
            self._socket = self._rfile = self._wfile = None
        else:
            raise ProgrammingError("Closing a closed connection")
        
    def query(self, sql):
        self._send(pdu.QueryPacket, self._encode(sql))
        self.affected_rows = self._get_result()
        return self.affected_rows
    
    def _encode(self, sql):
        if isinstance(sql, unicode):
            return sql.encode(self.charset)
        return sql
    
    def _send(self, packetclass, *args, **kwargs):
        packet = packetclass(*args, **kwargs)
        self._wfile.write(packet.to_data())
        self._wfile.flush()
        if self.DEBUG:
            packet.hexdump()
    
    def _recv(self, packetclass):
        header = self._rfile.read(4)
        if len(header) < 4:
            raise OperationalError(connectionerrors.CR_SERVER_LOST,
                                   "Lost connection to MySQL server during query")
        length = struct.unpack('<I', header[:3] + chr(0))[0]
        data = self._rfile.read(length)
        if len(data) < length:
            raise OperationalError(connectionerrors.CR_SERVER_LOST,
                                   "Lost connection to MySQL server during query")
        packet = packetclass().from_data(data)
        if self.DEBUG:
            packet.hexdump()
        return packet
    
    def _get_result(self):
        pass
    
    def _handshake(self):
        self._greeting()         # From server to client during initial handshake
        self._authentication()   # From client to server during initial handshake
    
    def _greeting(self):
        packet = self._recv(pdu.GreetingPacket)
    
    def _authentication(self):
        pass
    
    def _connect(self, host, port, unix_socket, connect_timeout):
        try:
            if unix_socket and host in ('localhost', '127.0.0.1'):
                family = socket.AF_UNIX
                address = unix_socket
            else:
                family = socket.AF_INET
                address = (host, port)
                
            self._socket = socket.socket(family, socket.SOCK_STREAM)
            timeout = self._socket.gettimeout()
            self._socket.settimeout(connect_timeout)
            self._socket.connect(address)
            self._socket.settimeout(timeout)
            
            self._rfile = self._socket.makefile('rb')
            self._wfile = self._socket.makefile('wb')
                
            self._handshake()
        except socket.error, e:
            raise OperationalError(connectionerrors.CR_CONN_HOST_ERROR,
                                   "Can't connect to MySQL server on %r (%s)" % (host, e.args[0]))