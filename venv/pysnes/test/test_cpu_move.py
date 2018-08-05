from tool.cpu import CPU65816

class MemoryMock(object):
    def __init__(self):
        self.ram = [0x00] * 0x123458

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value

def test_LDA_long():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 1
    mem.write(0x123456, 0xAB)
    mem.write(0x123457, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xAF, 0x56, 0x34, 0x12])
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000

def test_LDA_const16Bit():
    cpu = CPU65816(None)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 1
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xA9, 0x34, 0x12])
    assert cpu.A == 0x1234
    assert cpu.P == 0b00000000

def test_LDA_const8Bit():
    cpu = CPU65816(None)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 1
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xA9, 0x34])
    assert cpu.A == 0x34
    assert cpu.P == 0b00100000

def test_LDA_DP():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    mem.write(0x001234, 0xAB)
    cpu.DP = 0x1200
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xA5, 0x34])
    assert cpu.A == 0x00AB
    assert cpu.P == 0b00000000


