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


def test_STA_DP_indexed_indirect_X():
    mem = MemoryMock([0x81, 0x02])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.X = 0x0004

    mem.write(0x000020, 0xFF)
    mem.write(0x000021, 0x00)
    mem.write(0x000022, 0xFF)
    mem.write(0x000023, 0x09)
    mem.write(0x000024, 0x33)
    mem.write(0x000025, 0x33)
    mem.write(0x000026, 0x09) # low pointer
    mem.write(0x000027, 0x88) # high pointer

    mem.write(0x000028, 0x08)
    mem.write(0x000029, 0x76)
    mem.write(0x00002A, 0x66)
    mem.write(0x00002B, 0x36)
    mem.write(0x00002C, 0xD7)
    mem.write(0x00002D, 0x23)
    mem.write(0x00002E, 0x99)
    mem.write(0x00002F, 0x00)

    mem.write(0x808808, 0x00) # empty before
    mem.write(0x808809, 0x00) # empty before
    mem.write(0x80880A, 0x00) # empty before
    mem.write(0x80880B, 0x00) # empty before
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert mem.read(0x808808) == 0x00 # still empty
    assert mem.read(0x808809) == 0xAB
    assert mem.read(0x80880A) == 0xCD
    assert mem.read(0x80880B) == 0x00 # still empty
    assert cpu.cycles in (6,7,8)
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indexed_indirect_X_8BIT():
    mem = MemoryMock([0x81, 0x02])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.X = 0x0004

    mem.write(0x000026, 0x09) # low pointer
    mem.write(0x000027, 0x88) # high pointer
    mem.write(0x808808, 0x00) # empty before
    mem.write(0x808809, 0x00) # empty before
    mem.write(0x80880A, 0x00) # empty before
    mem.write(0x80880B, 0x00) # empty before
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert mem.read(0x808808) == 0x00 # still empty
    assert mem.read(0x808809) == 0xAB
    assert mem.read(0x80880A) == 0x00 # still empty!!!
    assert mem.read(0x80880B) == 0x00 # still empty
    assert cpu.cycles in (6,7,8)
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indexed_indirect_X_wrapped():
    mem = MemoryMock([0x81, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.DP = 0xFF00
    cpu.X = 0x000A

    mem.write(0x000008, 0xFF) # wrapping: 0x010008 becomes 0x000008
    mem.write(0x000009, 0xFF)

    mem.write(0x120000, 0x00) # empty before
    mem.write(0x12FFFF, 0x00) # empty before
    mem.write(0x130000, 0x00) # empty before
    mem.write(0x130001, 0x00) # empty before
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6,7,8)
    assert mem.read(0x120000) == 0x00  # still empty, no wrapping!
    assert mem.read(0x12FFFF) == 0xAB
    assert mem.read(0x130000) == 0xCD
    assert mem.read(0x130001) == 0x00  # still empty
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indexed_indirect_X_wrapped_8BIT():
    mem = MemoryMock([0x81, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.DP = 0xFF00
    cpu.X = 0x000A

    mem.write(0x000008, 0xFF) # wrapping: 0x010008 becomes 0x000008
    mem.write(0x000009, 0xFF)

    mem.write(0x120000, 0x00) # empty before
    mem.write(0x12FFFF, 0x00) # empty before
    mem.write(0x130000, 0x00) # empty before
    mem.write(0x130001, 0x00) # empty before
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6,7,8)
    assert mem.read(0x120000) == 0x00  # still empty
    assert mem.read(0x12FFFF) == 0xAB
    assert mem.read(0x130000) == 0x00  # still empty !!!
    assert mem.read(0x130001) == 0x00  # still empty
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_stack_relative():
    mem = MemoryMock([0x83, 0x01])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0x1FF0

    mem.write(0x001FF1, 0x00) # empty before
    mem.write(0x001FF2, 0x00) # empty before
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x001FF1) == 0xAB
    assert mem.read(0x001FF2) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_stack_relative_8BIT():
    mem = MemoryMock([0x83, 0x01])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.SP = 0x1FF0

    mem.write(0x001FF1, 0x00) # empty before
    mem.write(0x001FF2, 0x00) # empty before
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x001FF1) == 0xAB
    assert mem.read(0x001FF2) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_stack_relative_wrapped():
    mem = MemoryMock([0x83, 0xFA])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0xFF10

    mem.write(0x00000A, 0x00) # empty before
    mem.write(0x00000B, 0x00) # empty before
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x00000A) == 0xAB # wrapping: SP+FA==0xA
    assert mem.read(0x00000B) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_stack_relative_wrapped_8BIT():
    mem = MemoryMock([0x83, 0xFA])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.SP = 0xFF10

    mem.write(0x00000A, 0x00) # empty before
    mem.write(0x00000B, 0x00) # empty before
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x00000A) == 0xAB # wrapping: SP+FA==0xA
    assert mem.read(0x00000B) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP():
    mem = MemoryMock([0x85, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x001234) == 0xAB
    assert mem.read(0x001235) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_8BIT():
    mem = MemoryMock([0x85, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x001234) == 0xAB
    assert mem.read(0x001235) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_wrapped():
    mem = MemoryMock([0x85, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    mem.write(0x000000, 0x00)
    mem.write(0x00FFFF, 0x00) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x000000) == 0xCD
    assert mem.read(0x00FFFF) == 0xAB # zero bank wrapping!
    assert mem.read(0x010000) == 0x00
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_wrapped_8BIT():
    mem = MemoryMock([0x85, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    mem.write(0x000000, 0x00)
    mem.write(0x00FFFF, 0x00) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x000000) == 0x00 # still empty !!!
    assert mem.read(0x00FFFF) == 0xAB # zero bank wrapping!
    assert mem.read(0x010000) == 0x00
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_long():
    mem = MemoryMock([0x87, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    mem.write(0x000030, 0x30) # pointer low
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)
    mem.write(0x234030, 0x00)
    mem.write(0x234031, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7, 8)
    assert mem.read(0x234030) == 0xAB
    assert mem.read(0x234031) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_long_8BIT():
    mem = MemoryMock([0x87, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    mem.write(0x000030, 0x30) # pointer low
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)
    mem.write(0x234030, 0x00)
    mem.write(0x234031, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7, 8)
    assert mem.read(0x234030) == 0xAB
    assert mem.read(0x234031) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_long_no_wrapping():
    mem = MemoryMock([0x87, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    mem.write(0x000000, 0x12) # pointer low
    mem.write(0x00FFFE, 0xFF)
    mem.write(0x00FFFF, 0xFF)
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7, 8)
    assert mem.read(0x12FFFF) == 0xAB
    assert mem.read(0x130000) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_long_no_wrapping_8BIT():
    mem = MemoryMock([0x87, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    mem.write(0x000000, 0x12) # pointer low
    mem.write(0x00FFFE, 0xFF)
    mem.write(0x00FFFF, 0xFF)
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7, 8)
    assert mem.read(0x12FFFF) == 0xAB
    assert mem.read(0x130000) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_absolute():
    mem = MemoryMock([0x8D, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x123456) == 0xAB
    assert mem.read(0x123457) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_absolute_8Bit():
    mem = MemoryMock([0x8D, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x123456) == 0xAB
    assert mem.read(0x123457) == 0x00  # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_absolute_no_wrapping():
    mem = MemoryMock([0x8D, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x12FFFF) == 0xAB # no wrapping
    assert mem.read(0x130000) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_absolute_no_wrapping_8BIT():
    mem = MemoryMock([0x8D, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x12FFFF) == 0xAB # no wrapping
    assert mem.read(0x130000) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_long():
    mem = MemoryMock([0x8F, 0x56, 0x34, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x123456) == 0xAB
    assert mem.read(0x123457) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_STA_long_8BIT():
    mem = MemoryMock([0x8F, 0x56, 0x34, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x123456) == 0xAB
    assert mem.read(0x123457) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_STA_long2_no_wrapping():
    mem = MemoryMock([0x8F, 0xFF, 0xFF, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x12FFFF) == 0xAB
    assert mem.read(0x130000) == 0xCD # no wrapping
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_STA_long2_no_wrapping_8BIT():
    mem = MemoryMock([0x8F, 0xFF, 0xFF, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x12FFFF) == 0xAB # no wrapping
    assert mem.read(0x130000) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_STA_DP_indirect_indexed_Y():
    mem = MemoryMock([0x91, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x804031, 0x00)
    mem.write(0x804032, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 5
    assert mem.read(0x804031) == 0xAB
    assert mem.read(0x804032) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_indexed_Y_8BIT():
    mem = MemoryMock([0x91, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x804031, 0x00)
    mem.write(0x804032, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 5
    assert mem.read(0x804031) == 0xAB
    assert mem.read(0x804032) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_indexed_Y_wrapped():
    mem = MemoryMock([0x91, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.DP = 0xFF00
    cpu.Y = 0x000A
    mem.write(0x000000, 0xFF)
    mem.write(0x00FFFF, 0xFE)
    mem.write(0x130008, 0x00)
    mem.write(0x130009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 5
    assert mem.read(0x130008) == 0xAB
    assert mem.read(0x130009) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_indexed_Y_wrapped_8BIT():
    mem = MemoryMock([0x91, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.DP = 0xFF00
    cpu.Y = 0x000A
    mem.write(0x000000, 0xFF)
    mem.write(0x00FFFF, 0xFE)
    mem.write(0x130008, 0x00)
    mem.write(0x130009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 5
    assert mem.read(0x130008) == 0xAB
    assert mem.read(0x130009) == 0x00  # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect():
    mem = MemoryMock([0x92, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x804030, 0x00)
    mem.write(0x804031, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7)
    assert mem.read(0x804030) == 0xAB
    assert mem.read(0x804031) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_8BIT():
    mem = MemoryMock([0x92, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x804030, 0x00)
    mem.write(0x804031, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x804030) == 0xAB
    assert mem.read(0x804031) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_wrapped():
    mem = MemoryMock([0x92, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.DP = 0xFF00
    cpu.Y = 0x0001 # should have no effect
    mem.write(0x000000, 0xFF)
    mem.write(0x00FFFF, 0xFF)
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7)
    assert mem.read(0x12FFFF) == 0xAB
    assert mem.read(0x130000) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_wrapped_8BIT():
    mem = MemoryMock([0x92, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.DP = 0xFF00
    cpu.Y = 0x0001 # should have no effect
    mem.write(0x000000, 0xFF)
    mem.write(0x00FFFF, 0xFF)
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x12FFFF) == 0xAB
    assert mem.read(0x130000) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_stack_relative_indirect_indexed_Y():
    mem = MemoryMock([0x93, 0xFA])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0xFF10
    cpu.Y = 0x50
    cpu.DBR = 0x12
    mem.write(0x00000A, 0xF0) # 0x1000A becomes 0x000A
    mem.write(0x00000B, 0xFF) # 0x1000B becomes 0x000B
    mem.write(0x130040, 0x00)
    mem.write(0x130041, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert mem.read(0x130040) == 0xAB
    assert mem.read(0x130041) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_stack_relative_indirect_indexed_Y_8BIT():
    mem = MemoryMock([0x93, 0xFA])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.SP = 0xFF10
    cpu.Y = 0x50
    cpu.DBR = 0x12
    mem.write(0x00000A, 0xF0) # 0x1000A becomes 0x000A
    mem.write(0x00000B, 0xFF) # 0x1000B becomes 0x000B
    mem.write(0x130040, 0x00)
    mem.write(0x130041, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 7
    assert mem.read(0x130040) == 0xAB
    assert mem.read(0x130041) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indexed_X():
    mem = MemoryMock([0x95, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0x00)
    mem.write(0x000055, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x000054) == 0xAB
    assert mem.read(0x000055) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indexed_X_8BIT():
    mem = MemoryMock([0x95, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0x00)
    mem.write(0x000055, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (4, 5)
    assert mem.read(0x000054) == 0xAB
    assert mem.read(0x000055) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indexed_X_wrapping():
    mem = MemoryMock([0x95, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.X = 0x000A
    mem.write(0x000008, 0x00)
    mem.write(0x000009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x000008) == 0xAB
    assert mem.read(0x000009) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indexed_X_wrapping_8BIT():
    mem = MemoryMock([0x95, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.X = 0x000A
    mem.write(0x000008, 0x00)
    mem.write(0x000009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (4, 5)
    assert mem.read(0x000008) == 0xAB
    assert mem.read(0x000009) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_long_indexed_Y():
    mem = MemoryMock([0x97, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)
    mem.write(0x234031, 0x00)
    mem.write(0x234032, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (7, 8)
    assert mem.read(0x234031) == 0xAB
    assert mem.read(0x234032) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_long_indexed_Y_8BIT():
    mem = MemoryMock([0x97, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)
    mem.write(0x234031, 0x00)
    mem.write(0x234032, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7)
    assert mem.read(0x234031) == 0xAB
    assert mem.read(0x234032) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_long_indexed_Y_wrapping():
    mem = MemoryMock([0x97, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.Y = 0x000A
    mem.write(0x000000, 0x12)
    mem.write(0x00FFFE, 0xFC)
    mem.write(0x00FFFF, 0xFF)
    mem.write(0x130006, 0x00)
    mem.write(0x130007, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (7, 8)
    assert mem.read(0x130006) == 0xAB
    assert mem.read(0x130007) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_DP_indirect_long_indexed_Y_wrapping_8BIT():
    mem = MemoryMock([0x97, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.Y = 0x000A
    mem.write(0x000000, 0x12)
    mem.write(0x00FFFE, 0xFC)
    mem.write(0x00FFFF, 0xFF)
    mem.write(0x130006, 0x00)
    mem.write(0x130007, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7)
    assert mem.read(0x130006) == 0xAB
    assert mem.read(0x130007) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STA_abs_indexed_Y():
    mem = MemoryMock([0x99, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.Y = 0x0001
    mem.write(0x808001, 0x00)
    mem.write(0x808002, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()
    assert cpu.cycles == 6
    assert mem.read(0x808001) == 0xAB # no wrapping
    assert mem.read(0x808002) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_abs_indexed_Y_8BIT():
    mem = MemoryMock([0x99, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.Y = 0x0001
    mem.write(0x808001, 0x00)
    mem.write(0x808002, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x808001) == 0xAB # no wrapping
    assert mem.read(0x808002) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_abs_indexed_Y_no_wrapping():
    mem = MemoryMock([0x99, 0xFE, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.Y = 0x000A
    mem.write(0x130008, 0x00)
    mem.write(0x130009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x130008) == 0xAB # no wrapping
    assert mem.read(0x130009) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_abs_indexed_Y_no_wrapping_8BIT():
    mem = MemoryMock([0x99, 0xFE, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.Y = 0x000A
    mem.write(0x130008, 0x00)
    mem.write(0x130009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x130008) == 0xAB # no wrapping
    assert mem.read(0x130009) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_abs_indexed_X():
    mem = MemoryMock([0x9D, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0x00)
    mem.write(0x808002, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x808001) == 0xAB # no wrapping
    assert mem.read(0x808002) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_abs_indexed_X_8BIT():
    mem = MemoryMock([0x9D, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0x00)
    mem.write(0x808002, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x808001) == 0xAB # no wrapping
    assert mem.read(0x808002) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_abs_indexed_X_no_wrapping():
    mem = MemoryMock([0x9D, 0xFE, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.X = 0x000A
    mem.write(0x130008, 0x00)
    mem.write(0x130009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x130008) == 0xAB # no wrapping
    assert mem.read(0x130009) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_abs_indexed_X_no_wrapping_8BIT():
    mem = MemoryMock([0x9D, 0xFE, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.X = 0x000A
    mem.write(0x130008, 0x00)
    mem.write(0x130009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x130008) == 0xAB # no wrapping
    assert mem.read(0x130009) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STA_long_indexed_X():
    mem = MemoryMock([0x9F, 0x00, 0x80, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.X = 0x0001

    mem.write(0x808001, 0x00)
    mem.write(0x808002, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x808001) == 0xAB
    assert mem.read(0x808002) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_STA_long_indexed_X_8BIT():
    mem = MemoryMock([0x9F, 0x00, 0x80, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.X = 0x0001

    mem.write(0x808001, 0x00)
    mem.write(0x808002, 0x00)
    cpu.A = 0xCDAB
    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x808001) == 0xAB
    assert mem.read(0x808002) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_STA_long_indexed_X2():
    mem = MemoryMock([0x9F, 0xFE, 0xFF, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.X = 0x000A
    mem.write(0x130008, 0x00)
    mem.write(0x130009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x130008) == 0xAB
    assert mem.read(0x130009) == 0xCD
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_STA_long_indexed_X2_8BIT():
    mem = MemoryMock([0x9F, 0xFE, 0xFF, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.X = 0x000A
    mem.write(0x130008, 0x00)
    mem.write(0x130009, 0x00)
    cpu.A = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x130008) == 0xAB
    assert mem.read(0x130009) == 0x00 # still empty !!!
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b00100000  # no change
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_STX_DP():
    mem = MemoryMock([0x86, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x001234) == 0xAB
    assert mem.read(0x001235) == 0xCD
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STX_DP_8BIT():
    mem = MemoryMock([0x86, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x001234) == 0xAB
    assert mem.read(0x001235) == 0x00 # still empty !!!
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STX_DP_wrapped():
    mem = MemoryMock([0x86, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    mem.write(0x000000, 0x00)
    mem.write(0x00FFFF, 0x00) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x000000) == 0xCD
    assert mem.read(0x00FFFF) == 0xAB # zero bank wrapping!
    assert mem.read(0x010000) == 0x00
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STX_DP_wrapped_8BIT():
    mem = MemoryMock([0x86, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    mem.write(0x000000, 0x00)
    mem.write(0x00FFFF, 0x00) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x000000) == 0x00 # still empty !!!
    assert mem.read(0x00FFFF) == 0xAB # zero bank wrapping!
    assert mem.read(0x010000) == 0x00
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STX_absolute():
    mem = MemoryMock([0x8E, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x123456) == 0xAB
    assert mem.read(0x123457) == 0xCD
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STX_absolute_8Bit():
    mem = MemoryMock([0x8E, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x123456) == 0xAB
    assert mem.read(0x123457) == 0x00  # still empty !!!
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STX_absolute_no_wrapping():
    mem = MemoryMock([0x8E, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()


    assert cpu.cycles == 5
    assert mem.read(0x12FFFF) == 0xAB # no wrapping
    assert mem.read(0x130000) == 0xCD
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STX_absolute_no_wrapping_8BIT():
    mem = MemoryMock([0x8E, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x12FFFF) == 0xAB # no wrapping
    assert mem.read(0x130000) == 0x00 # still empty !!!
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STX_DP_indexed_Y():
    mem = MemoryMock([0x96, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.Y = 0x0004
    mem.write(0x000054, 0x00)
    mem.write(0x000055, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x000054) == 0xAB
    assert mem.read(0x000055) == 0xCD
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STX_DP_indexed_Y_8BIT():
    mem = MemoryMock([0x96, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.Y = 0x0004
    mem.write(0x000054, 0x00)
    mem.write(0x000055, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (4, 5)
    assert mem.read(0x000054) == 0xAB
    assert mem.read(0x000055) == 0x00 # still empty !!!
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STX_DP_indexed_Y_wrapping():
    mem = MemoryMock([0x96, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.Y = 0x000A
    mem.write(0x000008, 0x00)
    mem.write(0x000009, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x000008) == 0xAB
    assert mem.read(0x000009) == 0xCD
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STX_DP_indexed_Y_wrapping_8BIT():
    mem = MemoryMock([0x96, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.Y = 0x000A
    mem.write(0x000008, 0x00)
    mem.write(0x000009, 0x00)
    cpu.X = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (4, 5)
    assert mem.read(0x000008) == 0xAB
    assert mem.read(0x000009) == 0x00 # still empty !!!
    assert cpu.X == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STY_DP():
    mem = MemoryMock([0x84, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x001234) == 0xAB
    assert mem.read(0x001235) == 0xCD
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STY_DP_8BIT():
    mem = MemoryMock([0x84, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x001234) == 0xAB
    assert mem.read(0x001235) == 0x00 # still empty !!!
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STY_DP_wrapped():
    mem = MemoryMock([0x84, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    mem.write(0x000000, 0x00)
    mem.write(0x00FFFF, 0x00) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x000000) == 0xCD
    assert mem.read(0x00FFFF) == 0xAB # zero bank wrapping!
    assert mem.read(0x010000) == 0x00
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STY_DP_wrapped_8BIT():
    mem = MemoryMock([0x84, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    mem.write(0x000000, 0x00)
    mem.write(0x00FFFF, 0x00) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4, 5)
    assert mem.read(0x000000) == 0x00 # still empty !!!
    assert mem.read(0x00FFFF) == 0xAB # zero bank wrapping!
    assert mem.read(0x010000) == 0x00
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STY_absolute():
    mem = MemoryMock([0x8C, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x123456) == 0xAB
    assert mem.read(0x123457) == 0xCD
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STY_absolute_8Bit():
    mem = MemoryMock([0x8C, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x123456) == 0xAB
    assert mem.read(0x123457) == 0x00  # still empty !!!
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STY_absolute_no_wrapping():
    mem = MemoryMock([0x8C, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x12FFFF) == 0xAB # no wrapping
    assert mem.read(0x130000) == 0xCD
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STY_absolute_no_wrapping_8BIT():
    mem = MemoryMock([0x8C, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x12FFFF) == 0xAB # no wrapping
    assert mem.read(0x130000) == 0x00 # still empty !!!
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STY_DP_indexed_X():
    mem = MemoryMock([0x94, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0x00)
    mem.write(0x000055, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x000054) == 0xAB
    assert mem.read(0x000055) == 0xCD
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STY_DP_indexed_X_8BIT():
    mem = MemoryMock([0x94, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0x00)
    mem.write(0x000055, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (4, 5)
    assert mem.read(0x000054) == 0xAB
    assert mem.read(0x000055) == 0x00 # still empty !!!
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STY_DP_indexed_X_wrapping():
    mem = MemoryMock([0x94, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.X = 0x000A
    mem.write(0x000008, 0x00)
    mem.write(0x000009, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x000008) == 0xAB
    assert mem.read(0x000009) == 0xCD
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00000000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STY_DP_indexed_X_wrapping_8BIT():
    mem = MemoryMock([0x94, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.X = 0x000A
    mem.write(0x000008, 0x00)
    mem.write(0x000009, 0x00)
    cpu.Y = 0xCDAB

    cpu.fetch_decode_execute()

    assert cpu.cycles in (4, 5)
    assert mem.read(0x000008) == 0xAB
    assert mem.read(0x000009) == 0x00 # still empty !!!
    assert cpu.Y == 0xCDAB
    assert cpu.P == 0b00010000 # no change
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STZ_DP():
    mem = MemoryMock([0x64, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    mem.write(0x001234, 0xAB)
    mem.write(0x001235, 0xCD)
    cpu.DP = 0x1200

    cpu.fetch_decode_execute()
    assert cpu.cycles in (4, 5)
    assert mem.read(0x001234) == 0x00
    assert mem.read(0x001235) == 0x00
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STZ_DP_8Bit():
    mem = MemoryMock([0x64, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    mem.write(0x001234, 0xAB)
    mem.write(0x001235, 0xCD)
    cpu.DP = 0x1200

    cpu.fetch_decode_execute()
    assert cpu.cycles in (3, 4)
    assert mem.read(0x001234) == 0x00
    assert mem.read(0x001235) == 0xCD
    assert cpu.P == 0b00100000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STZ_DP_wrapping():
    mem = MemoryMock([0x64, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    mem.write(0x000000, 0xCD)
    mem.write(0x00FFFF, 0xAB)
    mem.write(0x010000, 0xEF)
    cpu.DP = 0xFF00

    cpu.fetch_decode_execute()

    assert cpu.cycles in (4, 5)
    assert mem.read(0x000000) == 0x00
    assert mem.read(0x00FFFF) == 0x00 # zero bank wrapping!
    assert mem.read(0x010000) == 0xEF # Bug if this is zero
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STZ_DP_wrapping_8Bit():
    mem = MemoryMock([0x64, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    mem.write(0x000000, 0xCD)
    mem.write(0x00FFFF, 0xAB)
    mem.write(0x010000, 0xEF)
    cpu.DP = 0xFF00

    cpu.fetch_decode_execute()

    assert cpu.cycles in (3, 4)
    assert mem.read(0x000000) == 0xCD
    assert mem.read(0x00FFFF) == 0x00 # zero bank wrapping!
    assert mem.read(0x010000) == 0xEF # Bug if this is zero
    assert cpu.P == 0b00100000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STZ_DP_indexed_X():
    mem = MemoryMock([0x74, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004

    mem.write(0x000054, 0xAB)
    mem.write(0x000055, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x000054) == 0x00
    assert mem.read(0x000055) == 0x00
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STZ_DP_indexed_X_8BIT():
    mem = MemoryMock([0x74, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004

    mem.write(0x000054, 0xAB)
    mem.write(0x000055, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (4, 5)
    assert mem.read(0x000054) == 0x00
    assert mem.read(0x000055) == 0xCD
    assert cpu.P == 0b00100000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STZ_DP_indexed_X_wrapped():
    mem = MemoryMock([0x74, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.X = 0x000A

    mem.write(0x000008, 0xAB)
    mem.write(0x000009, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6)
    assert mem.read(0x000008) == 0x00
    assert mem.read(0x000009) == 0x00
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STZ_DP_indexed_X_wrapped_8Bit():
    mem = MemoryMock([0x74, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80 # should have no effect
    cpu.DP = 0xFF00
    cpu.X = 0x000A

    mem.write(0x000008, 0xAB)
    mem.write(0x000009, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (4, 5)
    assert mem.read(0x000008) == 0x00
    assert mem.read(0x000009) == 0xCD
    assert cpu.P == 0b00100000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_STZ_absolute():
    mem = MemoryMock([0x9C, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0xAB)
    mem.write(0x123457, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x123456) == 0x00
    assert mem.read(0x123457) == 0x00
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STZ_absolute_8Bit():
    mem = MemoryMock([0x9C, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0xAB)
    mem.write(0x123457, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x123456) == 0x00
    assert mem.read(0x123457) == 0xCD
    assert cpu.P == 0b00100000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STZ_absolute_no_wrapping():
    mem = MemoryMock([0x9C, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x12FFFF, 0xAB)
    mem.write(0x130000, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x12FFFF) == 0x00 # no wrapping
    assert mem.read(0x130000) == 0x00
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STZ_absolute_no_wrapping_8BIT():
    mem = MemoryMock([0x9C, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x12FFFF, 0xAB)
    mem.write(0x130000, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert mem.read(0x12FFFF) == 0x00  # no wrapping
    assert mem.read(0x130000) == 0xCD
    assert cpu.P == 0b00100000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STZ_abs_indexed_X():
    mem = MemoryMock([0x9E, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0xAB)
    mem.write(0x808002, 0xCD)

    cpu.fetch_decode_execute()
    assert cpu.cycles == 6
    assert mem.read(0x808001) == 0x00 # no wrapping
    assert mem.read(0x808002) == 0x00
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STZ_abs_indexed_X_8BIT():
    mem = MemoryMock([0x9E, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0xAB)
    mem.write(0x808002, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert mem.read(0x808001) == 0x00 # no wrapping
    assert mem.read(0x808002) == 0xCD
    assert cpu.P == 0b00100000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STZ_abs_indexed_X_no_wrapping():
    mem = MemoryMock([0x9E, 0xFE, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.X = 0x000A
    mem.write(0x130008, 0xAB)
    mem.write(0x130009, 0xCD)

    cpu.fetch_decode_execute()

    assert mem.read(0x130008) == 0x00 # no wrapping
    assert mem.read(0x130009) == 0x00
    assert cpu.cycles == 6
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_STZ_abs_indexed_X_no_wrapping_8BIT():
    mem = MemoryMock([0x9E, 0xFE, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.X = 0x000A
    mem.write(0x130008, 0xAB)
    mem.write(0x130009, 0xCD)

    cpu.fetch_decode_execute()

    assert mem.read(0x130008) == 0x00 # no wrapping
    assert mem.read(0x130009) == 0xCD
    assert cpu.cycles == 5
    assert cpu.P == 0b00100000
    assert cpu.PC == 3 + mem.header.reset_int_addr
