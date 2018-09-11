from cartrige import ROMHeader
from helper import open_as_byte_array
from disassembler import Disassembler
from cpu import CPU65816
import sys

class MemoryMock(object):
    def __init__(self):
        self.ram = [0x00] * 16777216 # 2 ** 24

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value

def main(argv):
    ba = open_as_byte_array(argv[1])
    header = ROMHeader(ba)
    header.dump()
    c = CPU65816(MemoryMock())
    while True:
        # FIXME:
        if c.cycles > 10000:
            break
        c.fetch_decode_execute(ba)
    return 0

def target(*args):
    return main, None # returns the entry point

if __name__ == '__main__':
    import sys
    main(sys.argv)