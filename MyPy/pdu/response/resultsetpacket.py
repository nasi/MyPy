import struct
from mysql.pdu.base import Packet

class ResultSetPacket(Packet):
    
    def from_data(self, data):
        self.data = data
        
        self.field_count = struct.unpack('B', data[0])[0]
        
        return self