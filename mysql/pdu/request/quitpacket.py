import struct
from mysql.constants.commands import COM_QUIT


class QuitPacket(object):
    
    def to_data(self):
        return struct.pack('<IB', 1, COM_QUIT)