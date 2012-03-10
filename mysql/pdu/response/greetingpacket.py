from mysql.utils.hexdump import hexdump


class GreetingPacket(object):
    
    def from_data(self, data):
        self.data = data
        
        return self
    
    def hexdump(self):
        print hexdump(self.data)