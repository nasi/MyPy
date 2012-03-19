from MyPy.pdu.base import Packet

class OkPacket(Packet):
    
    def from_data(self, data):
        self.data = data
        return self