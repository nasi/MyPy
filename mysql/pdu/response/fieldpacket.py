from mysql.pdu.base import Packet

class FieldPacket(Packet):
    
    def from_data(self, data):
        self.data = data
        return self