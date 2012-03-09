import struct
from mysql.constants.commands import COM_QUERY


class QueryPacket(object):
    
    def __init__(self, sql):
        self.sql = sql
        
    def to_data(self):
        length = len(self.sql)
        return struct.pack('<IB%ds' % length, 1 + length, COM_QUERY, self.sql)