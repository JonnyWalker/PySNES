from cartrige import ROMHeader
from helper import open_as_byte_array
from disassembler import Disassembler
import argparse

parser = argparse.ArgumentParser(description='SNES Emulator in RPython')
parser.add_argument('rom', help='SNES ROM File')
args = parser.parse_args()

ba = open_as_byte_array(args.rom)
#print_hex_dump(ba)
header = ROMHeader(ba)
header.dump()
d = Disassembler()
d.print_assembler(ba, 0, 32)