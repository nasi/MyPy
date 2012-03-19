import struct
try:
    import hashlib
    sha1 = hashlib.sha1
except ImportError:
    import sha
    sha1 = sha.new
    
from MyPy.pdu.base import Packet
from MyPy.utils.crypto import scramble


class LoginPacket(Packet):
    
    def __init__(self, username, password, db, charset_number, salt, client_flag):
        max_packet_size = 1
        gap = chr(0) * 23
        
        payload = struct.pack('<2IB23s', client_flag, max_packet_size, charset_number, gap)
        payload += username + chr(0) + scramble(password, salt)
        if db is not None:
            payload += db + chr(0)
        
        length = len(payload)
        header = self._pack(length) + chr(1)
        self.data = header + payload
        
    def _pack(self, n):
        return struct.pack('3B', n & 0xff, (n>>8) & 0xff, (n>>16) & 0xff)
