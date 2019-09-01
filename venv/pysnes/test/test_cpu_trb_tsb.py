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


def test_TRB_DP_16bit():
    mem = MemoryMock([0x14, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000010  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x0FAB

    mem.write(0x001234, 0xAB)
    mem.write(0x001235, 0x0F)

    cpu.fetch_decode_execute()

    assert mem.read(0x001234) == 0x00
    assert mem.read(0x001235) == 0x00
    assert cpu.cycles == 7
    assert cpu.A == 0x0FAB
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_TRB_DP_8bit():
    mem = MemoryMock([0x14, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x9A

    mem.write(0x001234, 0x65)

    cpu.fetch_decode_execute()

    assert mem.read(0x001234) == 0x65
    assert cpu.cycles == 5
    assert cpu.A == 0x9A
    assert cpu.P == 0b00100010
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_TRB_absolute_16bit():
    mem = MemoryMock([0x1C, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000010 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0xFFFF

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x0F)

    cpu.fetch_decode_execute()

    assert mem.read(0x123456) == 0x00
    assert mem.read(0x123457) == 0x00
    assert cpu.cycles == 8
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_TRB_absolute_8bit():
    mem = MemoryMock([0x1C, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0x66

    mem.write(0x123456, 0x77)

    cpu.fetch_decode_execute()

    assert mem.read(0x123456) == 0x11
    assert cpu.cycles == 6
    assert cpu.A == 0x66
    assert cpu.P == 0b00100000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_TSB_DP_16bit():
    mem = MemoryMock([0x04, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x6666

    mem.write(0x001234, 0x99)
    mem.write(0x001235, 0x99)

    cpu.fetch_decode_execute()

    assert mem.read(0x001234) == 0xFF
    assert mem.read(0x001235) == 0xFF
    assert cpu.cycles == 7
    assert cpu.A == 0x6666
    assert cpu.P == 0b00000010
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_TSB_DP_8bit():
    mem = MemoryMock([0x04, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x9A

    mem.write(0x001234, 0x65)

    cpu.fetch_decode_execute()

    assert mem.read(0x001234) == 0xFF
    assert cpu.cycles == 5
    assert cpu.A == 0x9A
    assert cpu.P == 0b00100010
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_TSB_absolute_16bit():
    mem = MemoryMock([0x0C, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000010 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0xFFFF

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x0F)

    cpu.fetch_decode_execute()

    assert mem.read(0x123456) == 0xFF
    assert mem.read(0x123457) == 0xFF
    assert cpu.cycles == 8
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_TSB_absolute_8bit():
    mem = MemoryMock([0x0C, 0xCD, 0xAB])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0x43

    mem.write(0x12ABCD, 0x9C)

    cpu.fetch_decode_execute()

    assert mem.read(0x12ABCD) == 0xDF
    assert cpu.cycles == 6
    assert cpu.A == 0x43
    assert cpu.P == 0b00100010
    assert cpu.PC == 3 + mem.header.reset_int_addr