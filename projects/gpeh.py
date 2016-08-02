import struct
import os

class Gpeh:
    data = []
    def parse_file(self, filename):
        with open(filename, 'rb') as f:
            f.read(1)
            size, = struct.unpack('b', f.read(1))
            size -= 1
            while True:
                pattern = 'b' * size
                data = f.read(size)
                try:
                    row = struct.unpack(pattern, data)
                except struct.error:
                    size = len(data)
                    pattern = 'b' * size
                    row = struct.unpack(pattern, data)
                self.data.append(row)
                size_data = f.read(1)
                if size_data:
                    size, = struct.unpack('b', size_data)
                    size -= 1
                else:
                    break
