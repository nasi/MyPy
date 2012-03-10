import struct
from mysql.pdu.base import Packet
from mysql.constants.commands import COM_QUIT


class QuitPacket(Packet):
    
    def __init__(self):
        self.data = struct.pack('<IB', 1, COM_QUIT)