from cartrige import ROMHeader
from helper import open_as_byte_array
from disassembler import Disassembler
import sys

ba = open_as_byte_array(sys.argv[1])
print(len(ba))
#print_hex_dump(ba)
header = ROMHeader(ba)
header.dump()
d = Disassembler()
d.print_assembler(ba, 0, 129)