"""
Base Class for Packets
"""
from mysql.utils.hexdump import hexdump


class Packet(object):
    
    data = ''

    def to_data(self):
        return self.data
    
    def hexdump(self):
        print hexdump(self.data)