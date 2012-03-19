from MyPy.pdu.base import Packet
from MyPy.core.conversion import conversions

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
    
    def converted_columns(self, fields):
        new_columns = []
        for column, field in zip(self.columns, fields):
            cast = conversions[field[1]]
            if column is None:
                new_columns.append(None)
            elif cast != unicode:
                new_columns.append(cast(column))
            else:
                new_columns.append(cast(column.decode('utf-8')))

        return new_columns