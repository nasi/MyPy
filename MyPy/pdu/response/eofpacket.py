from MyPy.pdu.base import Packet

class EofPacket(Packet):
    
    def from_data(self, data):
        self.data = data
        return self