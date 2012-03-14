import struct
from mysql.pdu.base import Packet
from mysql.constants.commands import COM_QUERY


class QueryPacket(Packet):
    
    def __init__(self, sql):
        self.sql  = sql
        length    = len(sql)
        self.data = struct.pack('<IB%ds' % length, 1 + length, COM_QUERY, sql)