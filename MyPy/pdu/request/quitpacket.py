import struct
from MyPy.pdu.base import Packet
from MyPy.constants.commands import COM_QUIT


class QuitPacket(Packet):
    
    def __init__(self):
        self.data = struct.pack('<IB', 1, COM_QUIT)