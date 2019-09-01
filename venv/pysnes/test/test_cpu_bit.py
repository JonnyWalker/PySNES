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


def test_BIT_DP_16bit():
    mem = MemoryMock([0x24, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b11000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x0FAB

    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert cpu.A == 0x0FAB
    assert cpu.P == 0b00000010
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_BIT_DP_8bit():
    mem = MemoryMock([0x24, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b11100000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x0F

    mem.write(0x001234, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x0F
    assert cpu.P == 0b00100010
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_BIT_absolute_16bit():
    mem = MemoryMock([0x2C, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b11000010 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0xFFFF

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_BIT_absolute_8bit():
    mem = MemoryMock([0x2C, 0xCD, 0xAB])
    cpu = CPU65816(mem)
    cpu.P = 0b11100010 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0x43

    mem.write(0x12ABCD, 0x9C)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert cpu.A == 0x43
    assert cpu.P == 0b10100010
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_BIT_DP_indexed_X_16bit():
    mem = MemoryMock([0x34, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b11000010 # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0x0F0F

    mem.write(0x000054, 0xF0)
    mem.write(0x000055, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert cpu.A == 0x0F0F
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_BIT_DP_indexed_X_8bit():
    mem = MemoryMock([0x34, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b11100010 # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0x0F

    mem.write(0x000054, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0x0F
    assert cpu.P == 0b00100000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_BIT_abs_indexed_X_16bit():
    mem = MemoryMock([0x3C, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    cpu.A = 0x0F0F

    mem.write(0x808001, 0xFF) # no wrapping
    mem.write(0x808002, 0xF0)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 6
    assert cpu.A == 0x0F0F
    assert cpu.P == 0b11000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_BIT_abs_indexed_X_8bit():
    mem = MemoryMock([0x3C, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b11100010 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    cpu.A = 0x0F

    mem.write(0x808001, 0xFF) # no wrapping

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 5
    assert cpu.A == 0x0F
    assert cpu.P == 0b11100000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_BIT_imm_16bit():
    mem = MemoryMock([0x89, 0xFF, 0x00])
    cpu = CPU65816(mem)
    cpu.P = 0b00000010  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0xFFFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_BIT_imm_8bit():
    mem = MemoryMock([0x89, 0x00])
    cpu = CPU65816(mem)
    cpu.P = 0b11100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0xFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0xFF
    assert cpu.P == 0b11100010
    assert cpu.PC == 2 + mem.header.reset_int_addr