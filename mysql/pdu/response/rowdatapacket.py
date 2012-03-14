from mysql.pdu.base import Packet

class RowDataPacket(Packet):
    
    def from_data(self, data):
        self.data = data
        
        self.columns = []
        while len(data) > 0:
            length = ord(data[0])
            if length == 0xfb:
                column, data = None, data[1:]
            else:
                column, data = data[1:length+1], data[length+1:]
            self.columns.append(column)
        
        return self