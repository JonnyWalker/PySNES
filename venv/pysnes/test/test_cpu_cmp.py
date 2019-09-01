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


def test_CMP_zero():
    mem = MemoryMock([0xC9, 0x34, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x1234

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x1234
    assert cpu.P == 0b00000011  # z and c flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_CMP_zero_8bit():
    mem = MemoryMock([0xC9, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x12

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x12
    assert cpu.P == 0b00100011  # z and c flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_negative():
    mem = MemoryMock([0xC9, 0x35, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x1234

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x1234
    assert cpu.P == 0b10000000  # n flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_CMP_negative_8bit():
    mem = MemoryMock([0xC9, 0x13])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x12

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x12
    assert cpu.P == 0b10100000  # n flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_cflag():
    mem = MemoryMock([0xC9, 0x33, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x1234

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x1234
    assert cpu.P == 0b00000001  # c flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_CMP_cflag_8bit():
    mem = MemoryMock([0xC9, 0x11])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x12

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x12
    assert cpu.P == 0b00100001  # c flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_DP_indexed_indirect_X():
    mem = MemoryMock([0xC1, 0x02])
    cpu = CPU65816(mem)
    cpu.P = 0b10000010  # 16 Bit mode, n and z flag should be cleared
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0x1234

    mem.write(0x000026, 0x09)
    mem.write(0x000027, 0x88)

    mem.write(0x808809, 0x33)
    mem.write(0x80880A, 0x12)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert cpu.A == 0x1234
    assert cpu.P == 0b00000001
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_stack_relative():
    mem = MemoryMock([0xC3, 0x01])
    cpu = CPU65816(mem)
    cpu.P = 0b10000010  # 16 Bit mode, n and z flag should be cleared
    cpu.e = 0
    cpu.SP = 0x1FF0
    cpu.A = 0x0DAB

    mem.write(0x001FF1, 0x00)
    mem.write(0x001FF2, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0x0DAB
    assert cpu.P == 0b00000001
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_DP():
    mem = MemoryMock([0xC5, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b10000000  # 16 Bit mode, n flag should be cleared
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0x0FAB

    mem.write(0x001234, 0xAB)
    mem.write(0x001235, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert cpu.A == 0x0FAB
    assert cpu.P == 0b00000011
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_DP_indirect_long():
    mem = MemoryMock([0xC7, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000011  # 16 Bit mode, c and n flag should remain set
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.A = 0x0321

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)

    mem.write(0x234030, 0x21)
    mem.write(0x234031, 0x03)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert cpu.A == 0x0321
    assert cpu.P == 0b00000011
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_absolute():
    mem = MemoryMock([0xCD, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b10000011  # 16 Bit mode, n and z should be cleared, c should remain set
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0x0FFF

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0x0FFF
    assert cpu.P == 0b00000001
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_CMP_long():
    mem = MemoryMock([0xCF, 0x56, 0x34, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b10000000  # 16 Bit mode, n should remain set
    cpu.e = 0
    cpu.A = 0x0000

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert cpu.A == 0x0000
    assert cpu.P == 0b10000000
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_CMP_DP_indirect_indexed_Y():
    mem = MemoryMock([0xD1, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b10000010  # 16 Bit mode, n and z should be cleared
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    cpu.A = 0x0FFF

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)

    mem.write(0x804031, 0x00)
    mem.write(0x804032, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 7
    assert cpu.A == 0x0FFF
    assert cpu.P == 0b00000001
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_DP_indirect():
    mem = MemoryMock([0xD2, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000011  # 16 Bit mode, n and c should remain set
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
    assert cpu.P == 0b00000011
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_stack_relative_indirect_indexed_Y():
    mem = MemoryMock([0xD3, 0xFA])
    cpu = CPU65816(mem)
    cpu.P = 0b00000011  # 16 Bit mode, n and c should be cleared
    cpu.e = 0
    cpu.SP = 0xFF10
    cpu.Y = 0x50
    cpu.DBR = 0x12
    cpu.A = 0x1234

    mem.write(0x00000A, 0xF0)  # 0x1000A becomes 0x000A
    mem.write(0x00000B, 0xFF)  # 0x1000B becomes 0x000B

    mem.write(0x130040, 0x21)
    mem.write(0x130041, 0x43)

    cpu.fetch_decode_execute()
    assert cpu.cycles == 8
    assert cpu.A == 0x1234
    assert cpu.P == 0b10000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_DP_indexed_X():
    mem = MemoryMock([0xD5, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0x0F0F

    mem.write(0x000054, 0xF0)
    mem.write(0x000055, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert cpu.A == 0x0F0F
    assert cpu.P == 0b00000001
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_DP_indirect_long_indexed_Y():
    mem = MemoryMock([0xD7, 0x10])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    cpu.A = 0xFEDC

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x50)

    mem.write(0x504031, 0xDC)
    mem.write(0x504032, 0xFE)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert cpu.A == 0xFEDC
    assert cpu.P == 0b00000011
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CMP_abs_indexed_Y():
    mem = MemoryMock([0xD9, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b10000011  # 16 Bit mode, n and z should be cleared
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.Y = 0x0001
    cpu.A = 0x0F0F

    mem.write(0x808001, 0xFF)  # no wrapping
    mem.write(0x808002, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 6
    assert cpu.A == 0x0F0F
    assert cpu.P == 0b00000001
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_CMP_abs_indexed_X():
    mem = MemoryMock([0xDD, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    cpu.A = 0x0F0F

    mem.write(0x808001, 0xFF)  # no wrapping
    mem.write(0x808002, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 6
    assert cpu.A == 0x0F0F
    assert cpu.P == 0b00000001
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_CMP_long_indexed_X():
    mem = MemoryMock([0xDF, 0x00, 0x80, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b10000010  # 16 Bit mode, n and z should be cleared
    cpu.e = 0
    cpu.X = 0x0001
    cpu.A = 0xFFFF

    mem.write(0x808001, 0xAB)
    mem.write(0x808002, 0xCD)

    cpu.fetch_decode_execute()
    assert cpu.cycles == 6
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b00000001
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_CPX_cflag():
    mem = MemoryMock([0xE0, 0x33, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.X = 0x1234

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.X == 0x1234
    assert cpu.P == 0b00000001  # c flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_CMP_DP():
    mem = MemoryMock([0xE4, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000010  # 16 Bit mode, n should remain set
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.X = 0x0FAB

    mem.write(0x001234, 0xAB)
    mem.write(0x001235, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert cpu.X == 0x0FAB
    assert cpu.P == 0b00000011
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CPX_absolute():
    mem = MemoryMock([0xEC, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.X = 0x0FFF

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.X == 0x0FFF
    assert cpu.P == 0b00000001
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_CPY_cflag():
    mem = MemoryMock([0xC0, 0x33, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.Y = 0x1234

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.Y == 0x1234
    assert cpu.P == 0b00000001  # c flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_CPY_DP():
    mem = MemoryMock([0xC4, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b10000011  # 16 Bit mode, n should be cleared
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.Y = 0x0FAB

    mem.write(0x001234, 0xAB)
    mem.write(0x001235, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert cpu.Y == 0x0FAB
    assert cpu.P == 0b00000011
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_CPY_absolute():
    mem = MemoryMock([0xCC, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b10000001  # 16 Bit mode, n should be cleared
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.Y = 0x0FFF

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.Y == 0x0FFF
    assert cpu.P == 0b00000001
    assert cpu.PC == 3 + mem.header.reset_int_addr
