import socket
import struct

from mysql import pdu
from mysql.core.exceptions import OperationalError, ProgrammingError
from mysql.constants import connectionerrors


class Transport(object):
    
    LOCALHOST = ('localhost', '127.0.0.1')
    DEBUG = True
    
    def __init__(self, host, port, unix_socket=None):
        self.host = host
        self.port = port
        self.unix_socket = unix_socket
        
        if unix_socket and host in self.LOCALHOST:
            self.family = socket.AF_UNIX
            self.address = self.unix_socket
        else:
            self.family = socket.AF_INET
            self.address = (self.host, self.port)
    
    def connect(self, timeout, callback=None):
        try:
            self._socket = socket.socket(self.family, socket.SOCK_STREAM)
            timeout0 = self._socket.gettimeout()
            self._socket.settimeout(timeout)
            self._socket.connect(self.address)
            self._socket.settimeout(timeout0)
            
            self._rfile = self._socket.makefile('rb')
            self._wfile = self._socket.makefile('wb')
            
            if callback is not None:
                callback()
        except socket.error, e:
            raise OperationalError(connectionerrors.CR_CONN_HOST_ERROR,
                                   "Can't connect to MySQL server on %r (%s)" % \
                                   (self.host, e.args[0]))

    def disconnect(self):
        if self._socket is not None:
            self.send(pdu.QuitPacket)
            
            for obj in (self._wfile, self._rfile, self._socket):
                obj.close()
            self._socket = self._rfile = self._wfile = None
        else:
            raise ProgrammingError("Closing a closed connection")
    
    def send(self, packetclass, *args, **kwargs):
        packet = packetclass(*args, **kwargs)
        self._wfile.write(packet.to_data())
        self._wfile.flush()
        if self.DEBUG:
            packet.hexdump()
    
    def receive(self, packetclass):
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