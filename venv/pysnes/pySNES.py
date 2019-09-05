from cartrige import ROMHeader
from helper import open_as_byte_array
from disassembler import Disassembler
from cpu import CPU65816
from graphics import PictureProcessingUnit
from memory import MemoryMapper
import sys

if len(sys.argv) <= 1:
    print("usage: python PySNES.py ROM_PATH [start] [end]")
    exit(0)

ROM = open_as_byte_array(sys.argv[1])
#print_hex_dump(ba)[0:32]
header = ROMHeader(ROM)
header.dump()
d = Disassembler()
RAM  = [0] * (2 ** 17 - 1)  # 128 KB
SRAM = [0] * 0x7FFF         # 32 KB

memory = MemoryMapper(header, RAM, ROM, SRAM, False, 0x7FFF)
c = CPU65816(memory)
ppu = PictureProcessingUnit()
ppu.init()
while True:
    instr_str = d.disassemble_single_opcode(memory, c.PC, add_new_line=False,
                                  add_descr=False, add_addr=False, M=c.isM(), X=c.isX())
    cpu_status = "\t A:"+hex(c.A)+" X:"+hex(c.X)+" Y:"+hex(c.Y)+" DP:"+hex(c.DP)+ \
                 " SP:"+hex(c.SP)+" P:"+bin(c.P)+ " PC:"+hex(c.PC) + " e:"+bin(c.e)
    print(instr_str+cpu_status)
    # FIXME:
    if c.cycles > 100000:
        break
    c.fetch_decode_execute()

