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
    debug = "{0:<16} A={1:6} X={2:6} Y={3:6} DP={4:6} SP={5:6} P={6:6} PC={7:6} e={8:6} Stack:{9}"
    debug = debug.format(instr_str, hex(c.A), hex(c.X), hex(c.Y), hex(c.DP),
                               hex(c.SP), hex(c.P), hex(c.PC), hex(c.e), c.stack)
    print(debug)
    # FIXME:
    if c.cycles > 100000:
        break
    c.fetch_decode_execute()

