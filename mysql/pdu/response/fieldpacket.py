import struct
from mysql.pdu.base import Packet

def length_coded(data):
    length = ord(data[0])
    return data[1:length+1], data[length+1:]

class FieldPacket(Packet):
    
    def from_data(self, data):
        self.data = data
        
        self.catalog, data = length_coded(data)
        self.db, data = length_coded(data)
        self.table, data = length_coded(data)
        self.org_table, data = length_coded(data)
        self.name, data = length_coded(data)
        self.org_name, data = length_coded(data)
        
        data = data[1:] # Skip filter
        self.charsetnr, data = struct.unpack('<h', data[:2])[0], data[2:]
        self.length, data = struct.unpack('<I', data[:4])[0], data[4:]
        self.type, data = struct.unpack('<B', data[:1])[0], data[1:]
        self.flags, data = struct.unpack('<H', data[:2])[0], data[2:]
        self.decimals, data = struct.unpack('<B', data[:1])[0], data[1:]
                
        data = data[2:] # Skip filter
        
        if len(data) > 0:
            self.default, data = length_coded(data)
        else:
            self.default = None
        
        return self