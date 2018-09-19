from pysnes.cpu import CPU65816

class MemoryMock(object):
    def __init__(self):
        self.ram = {}

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value


def test_PEA():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.P = 0b00000000  # M and X Flag have no effect on PEA

    cpu.fetch_decode_execute([0xFA, 0x34, 0x12]) # PEA #$1234

    assert mem.read(0x0001FF) == 0x12 # high
    assert mem.read(0x0001FE) == 0x34 # low
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 5


def test_PEI():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.DP = 0x1200
    mem.write(0x001234, 0x78) # low: D + 0x34
    mem.write(0x001235, 0x56)
    cpu.P = 0b00000000  # M and X Flag have no effect on PEI

    cpu.fetch_decode_execute([0xD4, 0x34]) # PEI ($34)

    assert mem.read(0x0001FF) == 0x56 # high
    assert mem.read(0x0001FE) == 0x78 # low
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 6 # DL=0 => w=0


def test_PEI2():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.DP = 0x1201 # DH=12 DL=01
    mem.write(0x001234, 0x78) # low: D + 0x33
    mem.write(0x001235, 0x56)
    cpu.P = 0b00000000  # M and X Flag have no effect on PEI

    cpu.fetch_decode_execute([0xD4, 0x33]) # PEI ($33)

    assert mem.read(0x0001FF) == 0x56 # high
    assert mem.read(0x0001FE) == 0x78 # low
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 7 # DL!=0 => w=1


def test_PER():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.PC = 0x20
    cpu.P = 0b00000000  # M and X Flag have no effect on PER

    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x62, 0x34, 0x12]) # PER #$1234

    assert mem.read(0x0001FF) == 0x12 # high
    assert mem.read(0x0001FE) == 0x57 # low (1234+PC+3 = 1257)
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 6


def test_PER2():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.SP = 0x01FF
    cpu.PC = 0x12
    cpu.P = 0b00000000  # M and X Flag have no effect on PER

    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops + [0x62, 0x12, 0x00])  # PER #$0012

    assert mem.read(0x0001FF) == 0x00  # high
    assert mem.read(0x0001FE) == 0x27  # low (0012+PC+3 = 0027)
    assert cpu.SP == 0x01FD
    assert cpu.cycles == 6


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