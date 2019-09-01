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


# assumes that the high byte of A remains untouched in 8 bit mode
def test_ORA_8bit_affect_16bit_zero():
    mem = MemoryMock([0x09, 0x00])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0xFF00

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0xFF00
    assert cpu.P == 0b00100010  # zero flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_8Bit_affect16bit_negative():
    mem = MemoryMock([0x09, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0xFF7F

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b10100000  # negative flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_16Bit_constant_zero():
    mem = MemoryMock([0x09, 0x00, 0x00])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0000

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x0000
    assert cpu.P == 0b00000010  # zero flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ORA_16Bit_constant_negative():
    mem = MemoryMock([0x09, 0xAB, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0xFFBA

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    # 1111 1111 1011 1010 | 1000 0000 1010 1011 = 1111 1111 1011 1011
    assert cpu.A == 0xFFBB
    assert cpu.P == 0b10000000  # negative flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ORA_8Bit_constant_zero():
    mem = MemoryMock([0x09, 0x00])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x00

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x00
    assert cpu.P == 0b00100010 # zero flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_8Bit_constant_negative():
    mem = MemoryMock([0x09, 0xFB])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x1A

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    # 0001 1010 | 1111 1011 = 1111 1011
    assert cpu.A == 0xFB
    assert cpu.P == 0b10100000  # negative flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_16Bit_constant_noflag():
    mem = MemoryMock([0x09, 0xBA, 0x0C])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0FED

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    # 0000 1111 1110 1101 | 0000 1100 1011 1010 = 0000 1111 1111 1111
    assert cpu.A == 0x0FFF
    assert cpu.P == 0b00000000  # no flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ORA_8Bit_constant_noflag():
    mem = MemoryMock([0x09, 0x75])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x25

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    # 1111 0101 & 1000 0101 = 1111 0101
    assert cpu.A == 0x75
    assert cpu.P == 0b00100000  # no flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indexed_indirect_X():
    mem = MemoryMock([0x01, 0x02])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0xCDAB

    mem.write(0x000026, 0x09)
    mem.write(0x000027, 0x88)

    mem.write(0x808809, 0xCD)
    mem.write(0x80880A, 0xAB)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    # 1100 1101 1010 1011 | 1010 1011 1100 1101 = 1110 1111 1110 1111
    assert cpu.A == 0xEFEF
    assert cpu.P == 0b10000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indexed_indirect_X2():
    mem = MemoryMock([0x01, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.DP = 0xFF00
    cpu.X = 0x000A
    cpu.A = 0xABCD

    mem.write(0x000008, 0xFF)
    mem.write(0x000009, 0xFF)

    mem.write(0x12FFFF, 0xAB)
    mem.write(0x130000, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 7
    assert cpu.A == 0xEFEF
    assert cpu.P == 0b10000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_stack_relative():
    mem = MemoryMock([0x03, 0x01])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0x1FF0
    cpu.A = 0xCDAB

    mem.write(0x001FF1, 0x00)
    mem.write(0x001FF2, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_stack_relative2():
    mem = MemoryMock([0x03, 0xFA])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0xFF10
    cpu.A = 0x0AAA

    mem.write(0x00000A, 0x23)
    mem.write(0x00000B, 0x01)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    # 0000 1010 1010 1010 | 0000 0001 0010 00011 = 0000 1011 1010 1011
    assert cpu.A == 0x0BAB
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP():
    mem = MemoryMock([0x05, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x0000

    mem.write(0x001234, 0xAB)
    mem.write(0x001235, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert cpu.A == 0x0FAB
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP2():
    mem = MemoryMock([0x05, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    cpu.A = 0x0DAB

    mem.write(0x000000, 0x0D)
    mem.write(0x00FFFF, 0xAB)  # zero bank wrapping!
    mem.write(0x010000, 0xEF)  # Bug if this is read

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert cpu.A == 0x0DAB
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indirect_long():
    mem = MemoryMock([0x07, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.A = 0x0123

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)

    mem.write(0x234030, 0x21)
    mem.write(0x234031, 0x03)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert cpu.A == 0x0323
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indirect_long2():
    mem = MemoryMock([0x07, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    cpu.A = 0xFECD

    mem.write(0x000000, 0x12)
    mem.write(0x00FFFE, 0xFF)
    mem.write(0x00FFFF, 0xFF)

    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 7
    assert cpu.A == 0xFECD
    assert cpu.P == 0b10000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_absolute():
    mem = MemoryMock([0x0D, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0xFFFF

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b10000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ORA_absolute2():
    mem = MemoryMock([0x0D, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0x1234

    mem.write(0x12FFFF, 0x34)  # no wrapping
    mem.write(0x130000, 0x12)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0x1234
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ORA_long():
    mem = MemoryMock([0x0F, 0x56, 0x34, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.A = 0xF000

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0xFF)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b10000000
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_ORA_long2():
    mem = MemoryMock([0x0F, 0xFF, 0xFF, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.A = 0xFABC

    mem.write(0x12FFFF, 0x23)
    mem.write(0x130000, 0xF1)  # no wrapping

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    # 1111 1010 1011 1100 | 1111 0001 0010 0011 = 1111 1011 1011 1111
    assert cpu.A == 0xFBBF
    assert cpu.P == 0b10000000
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_ORA_DP_indirect_indexed_Y():
    mem = MemoryMock([0x11, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    cpu.A = 0x0FF0

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)

    mem.write(0x804031, 0x0F)
    mem.write(0x804032, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 7
    assert cpu.A == 0x0FFF
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indirect_indexed_Y2():
    mem = MemoryMock([0x11, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.DP = 0xFF00
    cpu.Y = 0x000A
    cpu.A = 0xFFFF

    mem.write(0x000000, 0xFF)
    mem.write(0x00FFFF, 0xFE)

    mem.write(0x130008, 0xAB)
    mem.write(0x130009, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 7
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b10000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indirect():
    mem = MemoryMock([0x12, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.A = 0xCDAB

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)

    mem.write(0x804030, 0xAB)
    mem.write(0x804031, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 7
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indirect2():
    mem = MemoryMock([0x12, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.DP = 0xFF00
    cpu.A = 0x1234

    mem.write(0x000000, 0xFF)
    mem.write(0x00FFFF, 0xFF)

    mem.write(0x12FFFF, 0x00)
    mem.write(0x130000, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert cpu.A == 0x1234
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_stack_relative_indirect_indexed_Y():
    mem = MemoryMock([0x13, 0xFA])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0xFF10
    cpu.Y = 0x50
    cpu.DBR = 0x12
    cpu.A = 0x1234

    mem.write(0x00000A, 0xF0) # 0x1000A becomes 0x000A
    mem.write(0x00000B, 0xFF) # 0x1000B becomes 0x000B

    mem.write(0x130040, 0x21)
    mem.write(0x130041, 0x43)

    cpu.fetch_decode_execute()
    assert cpu.cycles == 8
    assert cpu.A == 0x5335
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indexed_X():
    mem = MemoryMock([0x15, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0x0F0F

    mem.write(0x000054, 0xF0)
    mem.write(0x000055, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert cpu.A == 0x0FFF
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indexed_X2():
    mem = MemoryMock([0x15, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    cpu.X = 0x000A
    cpu.A = 0xCDAB

    mem.write(0x000008, 0xAB)
    mem.write(0x000009, 0xCD)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indirect_long_indexed_Y():
    mem = MemoryMock([0x17, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    cpu.A = 0xFEDC

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x50)

    mem.write(0x504031, 0xDC)
    mem.write(0x504032, 0x0E)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert cpu.A == 0xFEDC
    assert cpu.P == 0b10000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_DP_indirect_long_indexed_Y2():
    mem = MemoryMock([0x17, 0xFE])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0xFF00
    cpu.Y = 0x000A
    cpu.A = 0x1234

    mem.write(0x000000, 0x12)
    mem.write(0x00FFFE, 0xFC)
    mem.write(0x00FFFF, 0xFF)

    mem.write(0x130006, 0x34)
    mem.write(0x130007, 0x12)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 7
    assert cpu.A == 0x1234
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ORA_abs_indexed_Y():
    mem = MemoryMock([0x19, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.Y = 0x0001
    cpu.A = 0x0F0F

    mem.write(0x808001, 0xFF) # no wrapping
    mem.write(0x808002, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 6
    assert cpu.A == 0x0FFF
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ORA_abs_indexed_Y2():
    mem = MemoryMock([0x19, 0xFE, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.Y = 0x000A
    cpu.A = 0x0F0F

    mem.write(0x130008, 0xFF) # no wrapping
    mem.write(0x130009, 0xFF)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 6
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b10000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ORA_abs_indexed_X():
    mem = MemoryMock([0x1D, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    cpu.A = 0x0F0F

    mem.write(0x808001, 0xFF) # no wrapping
    mem.write(0x808002, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 6
    assert cpu.A == 0x0FFF
    assert cpu.P == 0b00000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ORA_abs_indexed_X2():
    mem = MemoryMock([0x1D, 0xFE, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.X = 0x000A
    cpu.A = 0x0F0F

    mem.write(0x130008, 0xFF) # no wrapping
    mem.write(0x130009, 0xFF)

    cpu.fetch_decode_execute()
    assert cpu.cycles >= 6
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b10000000
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ORA_long_indexed_X():
    mem = MemoryMock([0x1F, 0x00, 0x80, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.X = 0x0001
    cpu.A = 0xFFFF

    mem.write(0x808001, 0xAB)
    mem.write(0x808002, 0xCD)

    cpu.fetch_decode_execute()
    assert cpu.cycles == 6
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b10000000
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_ORA_long_indexed_X2():
    mem = MemoryMock([0x1F, 0xFE, 0xFF, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.X = 0x000A
    cpu.A = 0xCDAB

    mem.write(0x130008, 0xFF)
    mem.write(0x130009, 0xFF)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b10000000
    assert cpu.PC == 4 + mem.header.reset_int_addr
