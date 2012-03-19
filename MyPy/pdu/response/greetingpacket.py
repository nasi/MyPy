import struct
from mysql.pdu.base import Packet


class GreetingPacket(Packet):
    
    def from_data(self, data):
        self.data = data
        
        self.protocol_version = struct.unpack('<B', data[0])[0]
        self.server_version, data = data[1:].split(chr(0), 1)
        
        fmt = '<I8sBHBH'
        length = 4 + 8 + 1 + 2 + 1 + 2
        self.thread_id, self.scramble_buff, _, self.server_capabilities, \
            self.server_language, self.server_status = struct.unpack(fmt, data[:length])
        self.salt = self.scramble_buff + data[length + 13:].split(chr(0), 1)[0]
        
        return self