import struct
from MyPy.pdu.base import Packet
from MyPy.constants.commands import COM_QUERY


class QueryPacket(Packet):
    
    def __init__(self, sql):
        self.sql  = sql
        length    = len(sql)
        self.data = struct.pack('<IB%ds' % length, 1 + length, COM_QUERY, sql)