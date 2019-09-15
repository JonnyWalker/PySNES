from pysnes.cpu import CPU65816

# .../PySNES/venv/$ py.test pysnes/test/
class HeaderMock():
    def __init__(self):
        self.reset_int_addr = 0x8000

class MemoryMock(object):
    def __init__(self, ROM):
        self.ram = {}
        self.ROM = ROM
        self.header = HeaderMock()
        pc = self.header.reset_int_addr
        for byte in ROM:
            self.ram[pc] = byte
            pc += 1

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value


def test_PEA():
    mem = MemoryMock([0xF4, 0x34, 0x12])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.P = 0b00000000  # M and X Flag have no effect on PEA

    cpu.fetch_decode_execute() # PEA #$1234

    assert mem.read(0x0001FF) == 0x12 # high
    assert mem.read(0x0001FE) == 0x34 # low
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 5
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_PEI():
    mem = MemoryMock([0xD4, 0x34])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.DP = 0x1200
    mem.write(0x001234, 0x78) # low: D + 0x34
    mem.write(0x001235, 0x56)
    cpu.P = 0b00000000  # M and X Flag have no effect on PEI

    cpu.fetch_decode_execute() # PEI ($34)

    assert mem.read(0x0001FF) == 0x56 # high
    assert mem.read(0x0001FE) == 0x78 # low
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 6 # DL=0 => w=0
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_PEI2():
    mem = MemoryMock([0xD4, 0x33])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.DP = 0x1201 # DH=12 DL=01
    mem.write(0x001234, 0x78) # low: D + 0x33
    mem.write(0x001235, 0x56)
    cpu.P = 0b00000000  # M and X Flag have no effect on PEI

    cpu.fetch_decode_execute() # PEI ($33)

    assert mem.read(0x0001FF) == 0x56 # high
    assert mem.read(0x0001FE) == 0x78 # low
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 7 # DL!=0 => w=1
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_PER():
    nops = [0xEA] * 0x20
    mem = MemoryMock(nops+[0x62, 0x34, 0x12])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.PC += 0x20
    cpu.P = 0b00000000  # M and X Flag have no effect on PER

    cpu.fetch_decode_execute() # PER #$1234

    assert mem.read(0x0001FF) == 0x92 # high
    assert mem.read(0x0001FE) == 0x57 # low (0x1234+PC+0x3 = 0x9257)
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 6
    assert cpu.PC == 0x23 + mem.header.reset_int_addr


def test_PER2():
    nops = [0xEA]*0x12
    mem = MemoryMock(nops+[0x62, 0x12, 0x00])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.PC += 0x12
    cpu.P = 0b00000000  # M and X Flag have no effect on PER

    cpu.fetch_decode_execute()  # PER #$0012

    assert mem.read(0x0001FF) == 0x80  # high
    assert mem.read(0x0001FE) == 0x27  # low (0012+PC+3 = 8027)
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 6
    assert cpu.PC == 0x15 + mem.header.reset_int_addr


def test_PHK():
    nops = [0xEA] * ((0x12 << 16))
    mem = MemoryMock(nops+[0x4B])
    cpu = CPU65816(mem)
    cpu.PBR = 0x12 # K
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.PBR == 0x12
    assert mem.read(0x0001FF) == 0x12
    assert cpu.SP == 0x01FE
    assert cpu.cycles == 3
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PHB():
    mem = MemoryMock([0x8B])
    cpu = CPU65816(mem)
    cpu.DBR = 0x12 # B
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.DBR == 0x12
    assert mem.read(0x0001FF) == 0x12
    assert cpu.SP == 0x01FE
    assert cpu.cycles == 3
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PHP():
    mem = MemoryMock([0x08])
    cpu = CPU65816(mem)
    cpu.P = 0b10101010 # P
    cpu.SP = 0x01FF

    cpu.fetch_decode_execute()

    assert cpu.P == 0b10101010
    assert mem.read(0x0001FF) == 0b10101010
    assert cpu.SP == 0x01FE
    assert cpu.cycles == 3
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PHD():
    mem = MemoryMock([0x0B])
    cpu = CPU65816(mem)
    cpu.DP = 0xAFFE # D
    cpu.P = 0b00000000
    cpu.SP = 0x01FF

    cpu.fetch_decode_execute()

    assert cpu.DP == 0xAFFE
    assert cpu.P == 0b00000000
    assert mem.read(0x0001FF) == 0xAF
    assert mem.read(0x0001FE) == 0xFE
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 4
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PHA_8_bit():
    mem = MemoryMock([0x48])
    cpu = CPU65816(mem)
    cpu.A = 0xAFFE
    cpu.SP = 0x01FF
    cpu.P = 0b00100000

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FE
    assert mem.read(0x0001FF) == 0xFE
    assert cpu.cycles == 3
    assert cpu.P == 0b00100000
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PHA_16_bit():
    mem = MemoryMock([0x48])
    cpu = CPU65816(mem)
    cpu.A = 0x1337
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FD
    assert mem.read(0x0001FF) == 0x13
    assert mem.read(0x0001FE) == 0x37
    assert cpu.cycles == 4
    assert cpu.P == 0b00000000
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PLA_8_bit():
    mem = MemoryMock([0x68])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    cpu.A = 0xFFFF
    mem.write(0x0001FF, 0x42)
    cpu.P = 0b00100000 # set m flag
    cpu.stack = [0x42]

    cpu.fetch_decode_execute()

    assert cpu.A == 0xFF42 # in 8 bit mode the high byte of the A register persists
    assert cpu.SP == 0x01FF
    assert cpu.cycles == 4
    assert cpu.P == 0b00100000
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PLA_16_bit():
    mem = MemoryMock([0x68])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FD
    cpu.P = 0b00000000
    cpu.A = 0xFFFF
    mem.write(0x0001FF, 0xCD)
    mem.write(0x0001FE, 0xAB)
    cpu.stack = [0xCD, 0xAB]
    
    cpu.fetch_decode_execute()

    assert cpu.A == 0xCDAB
    assert cpu.cycles == 5
    assert cpu.P == 0b10000000
    assert cpu.SP == 0x01FF
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PHX_8_bit():
    mem = MemoryMock([0xDA])
    cpu = CPU65816(mem)
    cpu.X = 0xAFFE
    cpu.SP = 0x01FF
    cpu.P = 0b00010000

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FE
    assert mem.read(0x0001FF) == 0xFE
    assert cpu.cycles == 3
    assert cpu.P == 0b00010000
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PHX_16_bit():
    mem = MemoryMock([0xDA])
    cpu = CPU65816(mem)
    cpu.X = 0xAFFE
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FD
    assert mem.read(0x0001FF) == 0xAF
    assert mem.read(0x0001FE) == 0xFE
    assert cpu.cycles == 4
    assert cpu.P == 0b00000000
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PLX_8_bit():
    mem = MemoryMock([0xFA])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    cpu.X = 0xFFFF
    cpu.P = 0b00010000 # set x flag
    mem.write(0x0001FF, 0xB7)
    cpu.stack = [0xB7]

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b10010000 # negative flag set
    assert cpu.cycles == 4
    assert cpu.X == 0x00B7 # in 8 bit mode the high byte of the X/Y registers is forced to 0
    assert cpu.PC == 1 + mem.header.reset_int_addr
    

def test_PLX_16_bit():
    mem = MemoryMock([0xFA])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FD
    cpu.X = 0xFFFF
    cpu.P = 0b00000000
    mem.write(0x0001FF, 0xB0)
    mem.write(0x0001FE, 0x0B)
    cpu.stack = [0xB0, 0x0B]

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b10000000 # negative flag set
    assert cpu.cycles == 5
    assert cpu.X == 0xB00B
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PLY_8_bit():
    mem = MemoryMock([0x7A])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    cpu.Y = 0xFFFF
    cpu.P = 0b00010000 # set x flag
    mem.write(0x0001FF, 0x00)
    cpu.stack = [0x00]

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b00010010 # zero flag set
    assert cpu.cycles == 4
    assert cpu.Y == 0x0000
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PLY_16_bit():
    mem = MemoryMock([0x7A])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FD
    cpu.Y = 0x1234
    cpu.P = 0b00000000
    mem.write(0x0001FF, 0x24)
    mem.write(0x0001FE, 0x68)
    cpu.stack = [0x24, 0x68]

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b00000000
    assert cpu.cycles == 5
    assert cpu.Y == 0x2468
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PHY_8_bit():
    mem = MemoryMock([0x5A])
    cpu = CPU65816(mem)
    cpu.Y = 0x9001
    cpu.SP = 0x01FF
    cpu.P = 0b00010000 # set x flag

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FE
    assert mem.read(0x0001FF) == 0x01
    assert cpu.cycles == 3
    assert cpu.P == 0b00010000
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PHY_16_bit():
    mem = MemoryMock([0x5A])
    cpu = CPU65816(mem)
    cpu.Y = 0x9001
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FD
    assert mem.read(0x0001FF) == 0x90
    assert mem.read(0x0001FE) == 0x01
    assert cpu.cycles == 4
    assert cpu.P == 0b00000000
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PLP_16_bit():
    mem = MemoryMock([0x28])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    cpu.e = 0
    mem.write(0x01FF, 0b10101010)
    cpu.stack = [0xb10101010]
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b10101010
    assert cpu.e == 0
    assert cpu.cycles == 4
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PLP_8_bit():
    mem = MemoryMock([0x28])
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    mem.write(0x01FF, 0b11001111)
    cpu.stack = [0xb11001111]
    cpu.P = 0b00000000
    cpu.e = 1

    cpu.fetch_decode_execute()

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b11111111
    assert cpu.e == 1
    assert cpu.cycles == 4
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PLD():
    mem = MemoryMock([0x2B])
    cpu = CPU65816(mem)
    cpu.P = 0b00000010
    cpu.SP = 0x01FD
    mem.write(0x01FF, 0xCD)
    mem.write(0x01FE, 0xAB)
    cpu.stack = [0xCD, 0xAB]
    cpu.DP = 0x0000

    cpu.fetch_decode_execute()

    assert cpu.DP == 0xCDAB
    assert cpu.P == 0b10000000 # n flag set and z flag not set
    assert cpu.SP == 0x01FF
    assert cpu.cycles == 5
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_PLB():
    mem = MemoryMock([0xAB])
    cpu = CPU65816(mem)
    cpu.DBR = 0
    cpu.P = 0b00000010
    cpu.SP = 0x01FE
    mem.write(0x01FF, 0xFF)
    cpu.stack = [0xFF]

    cpu.fetch_decode_execute()

    assert cpu.DBR == 0xFF
    assert cpu.P == 0b10000000
    assert cpu.SP == 0x01FF
    assert cpu.cycles == 4
    assert cpu.PC == 1 + mem.header.reset_int_addr
