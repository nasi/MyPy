"""
Base Class for Packets
"""
from MyPy.utils.hexdump import hexdump


class Packet(object):
    
    data = ''

    def to_data(self):
        return self.data
    
    def hexdump(self, data=None):
        if data is None:
            data = self.data
        print hexdump(data)