from pysnes.cpu import CPU65816

class MemoryMock(object):
    def __init__(self):
        self.ram = {}

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value


def test_PHK():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.PBR = 0x12 # K
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    # opcode at 12:0000
    nops = [0xEA] * ((cpu.PBR << 16) + cpu.PC)
    cpu.fetch_decode_execute(nops + [0x4B])

    assert cpu.P == 0b00000000
    assert cpu.PBR == 0x12
    assert mem.read(0x0001FF) == 0x12
    assert cpu.SP == 0x01FE
    assert cpu.cycles == 3


def test_PHB():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.DBR = 0x12 # B
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    cpu.fetch_decode_execute([0x8B])

    assert cpu.P == 0b00000000
    assert cpu.DBR == 0x12
    assert mem.read(0x0001FF) == 0x12
    assert cpu.SP == 0x01FE
    assert cpu.cycles == 3


def test_PHP():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b10101010 # P
    cpu.SP = 0x01FF

    cpu.fetch_decode_execute([0x08])

    assert cpu.P == 0b10101010
    assert mem.read(0x0001FF) == 0b10101010
    assert cpu.SP == 0x01FE
    assert cpu.cycles == 3


def test_PHD():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.DP = 0xAFFE # D
    cpu.P = 0b00000000
    cpu.SP = 0x01FF

    cpu.fetch_decode_execute([0x0B])

    assert cpu.DP == 0xAFFE
    assert cpu.P == 0b00000000
    assert mem.read(0x0001FF) == 0xAF
    assert mem.read(0x0001FE) == 0xFE
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 4


def test_PHA_8_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.A = 0xAFFE
    cpu.SP = 0x01FF
    cpu.P = 0b00100000

    cpu.fetch_decode_execute([0x48])

    assert cpu.SP == 0x01FE
    assert mem.read(0x0001FF) == 0xFE
    assert cpu.cycles == 3
    assert cpu.P == 0b00100000


def test_PHA_16_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.A = 0x1337
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    cpu.fetch_decode_execute([0x48])

    assert cpu.SP == 0x01FD
    assert mem.read(0x0001FF) == 0x13
    assert mem.read(0x0001FE) == 0x37
    assert cpu.cycles == 4
    assert cpu.P == 0b00000000


def test_PLA_8_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    cpu.A = 0xFFFF
    mem.write(0x0001FF, 0x42)
    cpu.P = 0b00100000 # set m flag

    cpu.fetch_decode_execute([0x68])

    assert cpu.A == 0xFF42 # in 8 bit mode the high byte of the A register persists
    assert cpu.SP == 0x01FF
    assert cpu.cycles == 4
    assert cpu.P == 0b00100000


def test_PLA_16_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FD
    cpu.P = 0b00000000
    cpu.A = 0xFFFF
    mem.write(0x0001FF, 0xCD)
    mem.write(0x0001FE, 0xAB)
    
    cpu.fetch_decode_execute([0x68])

    assert cpu.A == 0xCDAB
    assert cpu.cycles == 5
    assert cpu.P == 0b10000000
    assert cpu.SP == 0x01FF


def test_PHX_8_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.X = 0xAFFE
    cpu.SP = 0x01FF
    cpu.P = 0b00010000

    cpu.fetch_decode_execute([0xDA])

    assert cpu.SP == 0x01FE
    assert mem.read(0x0001FF) == 0xFE
    assert cpu.cycles == 3
    assert cpu.P == 0b00010000


def test_PHX_16_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.X = 0xAFFE
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    cpu.fetch_decode_execute([0xDA])

    assert cpu.SP == 0x01FD
    assert mem.read(0x0001FF) == 0xAF
    assert mem.read(0x0001FE) == 0xFE
    assert cpu.cycles == 4
    assert cpu.P == 0b00000000


def test_PLX_8_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    cpu.X = 0xFFFF
    cpu.P = 0b00010000 # set x flag
    mem.write(0x0001FF, 0xB7)

    cpu.fetch_decode_execute([0xFA])

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b10010000 # negative flag set
    assert cpu.cycles == 4
    assert cpu.X == 0x00B7 # in 8 bit mode the high byte of the X/Y registers is forced to 0
    

def test_PLX_16_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FD
    cpu.X = 0xFFFF
    cpu.P = 0b00000000
    mem.write(0x0001FF, 0xB0)
    mem.write(0x0001FE, 0x0B)

    cpu.fetch_decode_execute([0xFA])

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b10000000 # negative flag set
    assert cpu.cycles == 5
    assert cpu.X == 0xB00B


def test_PLY_8_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    cpu.Y = 0xFFFF
    cpu.P = 0b00010000 # set x flag
    mem.write(0x0001FF, 0x00)

    cpu.fetch_decode_execute([0x7A])

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b00010010 # zero flag set
    assert cpu.cycles == 4
    assert cpu.Y == 0x0000


def test_PLY_16_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FD
    cpu.Y = 0x1234
    cpu.P = 0b00000000
    mem.write(0x0001FF, 0x24)
    mem.write(0x0001FE, 0x68)

    cpu.fetch_decode_execute([0x7A])

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b00000000
    assert cpu.cycles == 5
    assert cpu.Y == 0x2468


def test_PHY_8_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.Y = 0x9001
    cpu.SP = 0x01FF
    cpu.P = 0b00010000 # set x flag

    cpu.fetch_decode_execute([0x5A])

    assert cpu.SP == 0x01FE
    assert mem.read(0x0001FF) == 0x01
    assert cpu.cycles == 3
    assert cpu.P == 0b00010000


def test_PHY_16_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.Y = 0x9001
    cpu.SP = 0x01FF
    cpu.P = 0b00000000

    cpu.fetch_decode_execute([0x5A])

    assert cpu.SP == 0x01FD
    assert mem.read(0x0001FF) == 0x90
    assert mem.read(0x0001FE) == 0x01
    assert cpu.cycles == 4
    assert cpu.P == 0b00000000


def test_PLP_16_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    cpu.e = 0
    mem.write(0x01FF, 0b10101010)
    cpu.P = 0b00000000

    cpu.fetch_decode_execute([0x28])

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b10101010
    assert cpu.e == 0
    assert cpu.cycles == 4


def test_PLP_8_bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FE
    mem.write(0x01FF, 0b11001111)
    cpu.P = 0b00000000
    cpu.e = 1

    cpu.fetch_decode_execute([0x28])

    assert cpu.SP == 0x01FF
    assert cpu.P == 0b11111111
    assert cpu.e == 1
    assert cpu.cycles == 4


def test_PLD():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000010
    cpu.SP = 0x01FD
    mem.write(0x01FF, 0xCD)
    mem.write(0x01FE, 0xAB)
    cpu.DP = 0x0000

    cpu.fetch_decode_execute([0x2B])

    assert cpu.DP == 0xCDAB
    assert cpu.P == 0b10000000 # n flag set and z flag not set
    assert cpu.SP == 0x01FF
    assert cpu.cycles == 5


def test_PLB():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.DBR = 0
    cpu.P = 0b00000010
    cpu.SP = 0x01FE
    mem.write(0x01FF, 0xFF)

    cpu.fetch_decode_execute([0xAB])

    assert cpu.DBR == 0xFF
    assert cpu.P == 0b10000000
    assert cpu.SP == 0x01FF
    assert cpu.cycles == 4
