from pysnes.cpu import CPU65816

# .../PySNES/venv/$ py.test pysnes/test/


class MemoryMock(object):
    def __init__(self):
        self.ram = {}

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value


def test_BIT_DP_16bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b11000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x0FAB

    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)

    cpu.fetch_decode_execute([0x24, 0x34])

    assert cpu.cycles == 4
    assert cpu.A == 0x0FAB
    assert cpu.P == 0b00000010


def test_BIT_DP_8bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b11100000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x0F

    mem.write(0x001234, 0x00)

    cpu.fetch_decode_execute([0x24, 0x34])

    assert cpu.cycles == 3
    assert cpu.A == 0x0F
    assert cpu.P == 0b00100010


def test_BIT_absolute_16bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b11000010 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0xFFFF

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x0F)

    cpu.fetch_decode_execute([0x2C, 0x56, 0x34])

    assert cpu.cycles == 5
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b00000000


def test_BIT_absolute_8bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b11100010 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0x43

    mem.write(0x12ABCD, 0x9C)

    cpu.fetch_decode_execute([0x2C, 0xCD, 0xAB])

    assert cpu.cycles == 4
    assert cpu.A == 0x43
    assert cpu.P == 0b10100010


def test_BIT_DP_indexed_X_16bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b11000010 # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0x0F0F

    mem.write(0x000054, 0xF0)
    mem.write(0x000055, 0x0F)

    cpu.fetch_decode_execute([0x34, 0x30])

    assert cpu.cycles == 6
    assert cpu.A == 0x0F0F
    assert cpu.P == 0b00000000


def test_BIT_DP_indexed_X_8bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b11100010 # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0x0F

    mem.write(0x000054, 0x0F)

    cpu.fetch_decode_execute([0x34, 0x30])

    assert cpu.cycles == 5
    assert cpu.A == 0x0F
    assert cpu.P == 0b00100000


def test_BIT_abs_indexed_X_16bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    cpu.A = 0x0F0F

    mem.write(0x808001, 0xFF) # no wrapping
    mem.write(0x808002, 0xF0)

    cpu.fetch_decode_execute([0x3C, 0x00, 0x80])

    assert cpu.cycles >= 6
    assert cpu.A == 0x0F0F
    assert cpu.P == 0b11000000


def test_BIT_abs_indexed_X_8bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b11100010 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    cpu.A = 0x0F

    mem.write(0x808001, 0xFF) # no wrapping

    cpu.fetch_decode_execute([0x3C, 0x00, 0x80])

    assert cpu.cycles >= 5
    assert cpu.A == 0x0F
    assert cpu.P == 0b11100000


def test_BIT_imm_16bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000010  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0xFFFF

    cpu.fetch_decode_execute([0x89, 0xFF, 0x00])

    assert cpu.cycles == 3
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b00000000


def test_BIT_imm_8bit():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b11100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0xFF

    cpu.fetch_decode_execute([0x89, 0x00])

    assert cpu.cycles == 2
    assert cpu.A == 0xFF
    assert cpu.P == 0b11100010