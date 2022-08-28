#IMPORT STUFF
from io import BufferedReader, BytesIO
import zlib

class Writer:
    def __init__(self, client, endian: str = 'big'):
        self.client = client
        self.endian = endian
        self.buffer = b''

    def writeint(self, data: int, length: int = 4):
        if data > 0:
            self.buffer += data.to_bytes(length, 'big', signed=False)
        else:
            self.buffer += data.to_bytes(length, 'big', signed=True)    
    def writeInt(self, data: int, length: int = 4):
        if data > 0:
            self.buffer += data.to_bytes(length, 'big', signed=False)
        else:
            self.buffer += data.to_bytes(length, 'big', signed=True)    
    def writeLong(self, high, low):
        self.buffer += high.to_bytes(4, 'big') + low.to_bytes(4, 'big')
    def writeDataReference(self, ClassID, InstanceID=0):
        if ClassID >= 1 and InstanceID >= 0:
            self.writeVInt(ClassID)
            self.writeVInt(InstanceID)
        else:
            self.writeVInt(0)
    def writeBoolean(self, *args):
        boolean = 0
        i = 0
        for value in args:
            if value:
                boolean |= 1 << i
            i += 1
        self.writeByte(boolean)       
    def writeString(self, string = None):
        if string is None:
            self.writeInt((2 ** 32) - 1)
        else:
            if type(string) == bytes:
                encoded = string
            else:
                encoded = string.encode('utf-8')
            self.writeInt(len(encoded))
            self.buffer += encoded

class Reader(BufferedReader):
    def __init__(self, header_bytes):
        super().__init__(BytesIO(header_bytes))
        self.bytes_of_packets = header_bytes


    def readInt(self):
        return int.from_bytes(self.read(4), "big")
    def readLong(self):
        high = self.readInt()
        low = self.readInt()
        return high, low
    def readBoolean(self):
        result = bool.from_bytes(bytes=self.read(1), byteorder='big', signed=False)
        if result == True:
            return True
        else:
            return False