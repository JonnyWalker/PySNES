from cartrige import ROMHeader
from helper import open_as_byte_array
from disassembler import Disassembler
from cpu import CPU65816
from opcodes import opcode_map
import sys

if len(sys.argv) <= 1:
    print("usage: python PySNES.py ROM_PATH [start] [end]")
    exit(0)

ba = open_as_byte_array(sys.argv[1])
#print_hex_dump(ba)[0:32]
header = ROMHeader(ba)
header.dump()
d = Disassembler()

class MemoryMock(object):
    def __init__(self):
        self.ram = [0x00] * 16777216 # 2 ** 24

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value

c = CPU65816(MemoryMock())
while True:
    instr_str = d.disassemble_single_opcode(ba, c.PC, add_new_line=False,
                                  add_descr=False, add_addr=False, M=c.isM(), X=c.isX())
    cpu_status = "\t A:"+hex(c.A)+" X:"+hex(c.X)+" Y:"+hex(c.Y)+" DP:"+hex(c.DP)+ \
                 " SP:"+hex(c.SP)+" P:"+bin(c.P)+" e:"+bin(c.e)
    print(instr_str+cpu_status)
    # FIXME:
    if c.cycles > 10000:
        break
    c.fetch_decode_execute(ba)

