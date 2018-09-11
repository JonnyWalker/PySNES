from cartrige import ROMHeader
from helper import open_as_byte_array
from disassembler import Disassembler
from cpu import CPU65816
import sys

if len(sys.argv) <= 1:
    print("usage: python PySNES.py ROM_PATH [start] [end]")
    exit(0)

ba = open_as_byte_array(sys.argv[1])
#print_hex_dump(ba)[0:32]
header = ROMHeader(ba)
header.dump()
d = Disassembler()
start = 0
end = len(ba)-2
if len(sys.argv) > 2:
    start = int(sys.argv[2])
if len(sys.argv) > 3:
    end = int(sys.argv[3])
#d.print_assembler(ba, start, end)
class MemoryMock(object):
    def __init__(self):
        self.ram = [0x00] * 16777216 # 2 ** 24

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value

c = CPU65816(MemoryMock())
while True:
    # FIXME:
    if c.cycles > 10000:
        break
    c.fetch_decode_execute(ba)

