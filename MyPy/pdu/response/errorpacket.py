from MyPy.pdu.base import Packet

class ErrorPacket(Packet):
    
    def from_data(self, data):
        self.data = data
        return self