import struct

from MyPy.pdu.base import Packet
from MyPy.pdu.response.okpacket import OkPacket
from MyPy.pdu.response.errorpacket import ErrorPacket
from MyPy.pdu.response.eofpacket import EofPacket
from MyPy.pdu.response.rowdatapacket import RowDataPacket


class ResultPacket(Packet):
    
    def from_data(self, data):
        self.data = data
        first_byte = ord(data[0])

        if first_byte == 0x00:
            return OkPacket().from_data(data)
        elif first_byte == 0xff:
            return ErrorPacket().from_data(data)
        elif first_byte == 0xfe:
            return EofPacket().from_data(data)
        else:
            return RowDataPacket().from_data(data)
        
        return self