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


def test_INC():
    mem = MemoryMock([0x1A])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0000

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x0001
    assert cpu.P == 0b00000000 # no flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INC_8BIT():
    mem = MemoryMock([0x1A])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x00

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x01
    assert cpu.P == 0b00100000 # no flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INC_Zero():
    mem = MemoryMock([0x1A])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0xFFFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x0000
    assert cpu.P == 0b00000010  # zero flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INC_Zero_8BIT():
    mem = MemoryMock([0x1A])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0xFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x00
    assert cpu.P == 0b00100010  # zero flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INC_no_overflow():
    mem = MemoryMock([0x1A])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x7FFF      # 32.767 (Max Int)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x8000      # -32.768 (MIN INT)
    assert cpu.P == 0b10000000  # negative flag, no overflow flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INC_no_overflow_8BIT():
    mem = MemoryMock([0x1A])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x7F        # 127 (Max Int)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x80        # -128 (MIN INT)
    assert cpu.P == 0b10100000  # negative flag, no overflow flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INC_DP():
    mem = MemoryMock([0xE6, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6, 7, 8)
    assert mem.read(0x001234) == 0x01
    assert mem.read(0x001235) == 0x00
    assert cpu.P == 0b00000000 # no flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_8BIT():
    mem = MemoryMock([0xE6, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0x00)
    mem.write(0x001235, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6, 7, 8)
    assert mem.read(0x001234) == 0x01
    assert mem.read(0x001235) == 0x00
    assert cpu.P == 0b00100000 # no flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_Zero():
    mem = MemoryMock([0xE6, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0xFF)
    mem.write(0x001235, 0xFF)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6, 7, 8)
    assert mem.read(0x001234) == 0x00
    assert mem.read(0x001235) == 0x00
    assert cpu.P == 0b00000010 # zero flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_Zero_8BIT():
    mem = MemoryMock([0xE6, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0xFF)
    mem.write(0x001235, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6, 7, 8)
    assert mem.read(0x001234) == 0x00
    assert mem.read(0x001235) == 0x00
    assert cpu.P == 0b00100010 # zero flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_no_overflow():
    mem = MemoryMock([0xE6, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0xFF) # 32.767 (Max Int)
    mem.write(0x001235, 0x7F)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6, 7, 8)
    assert mem.read(0x001234) == 0x00 # -32.768 (MIN INT)
    assert mem.read(0x001235) == 0x80
    assert cpu.P == 0b10000000 # negative flag, no overflow flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_no_overflow_8BIT():
    mem = MemoryMock([0xE6, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    mem.write(0x001234, 0x7F) # 127 (Max Int)
    mem.write(0x001235, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (5, 6, 7, 8)
    assert mem.read(0x001234) == 0x80 # -128 (MIN INT)
    assert mem.read(0x001235) == 0x00
    assert cpu.P == 0b10100000 # negative flag, no overflow flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_absolute():
    mem = MemoryMock([0xEE, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert mem.read(0x123456) == 0x01
    assert mem.read(0x123457) == 0x00
    assert cpu.P == 0b00000000 # no flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_absolute_8BIT():
    mem = MemoryMock([0xEE, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x123456) == 0x01
    assert mem.read(0x123457) == 0x00
    assert cpu.P == 0b00100000 # no flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_absolute_Zero():
    mem = MemoryMock([0xEE, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0xFF)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert mem.read(0x123456) == 0x00
    assert mem.read(0x123457) == 0x00
    assert cpu.P == 0b00000010 # zero flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_absolute_Zero_8BIT():
    mem = MemoryMock([0xEE, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x123456) == 0x00
    assert mem.read(0x123457) == 0x00
    assert cpu.P == 0b00100010 # zero flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_absolute_no_overflow():
    mem = MemoryMock([0xEE, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0xFF) # 32.767 (Max Int)
    mem.write(0x123457, 0x7F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert mem.read(0x123456) == 0x00 # -32.768 (MIN INT)
    assert mem.read(0x123457) == 0x80
    assert cpu.P == 0b10000000 # negative flag, no overflow flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_absolute_no_overflow_8BIT():
    mem = MemoryMock([0xEE, 0x56, 0x34])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0x7F) # 127 (Max Int)
    mem.write(0x123457, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert mem.read(0x123456) == 0x80 # -128 (MIN INT)
    assert mem.read(0x123457) == 0x00
    assert cpu.P == 0b10100000 # negative flag, no overflow flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_DP_indexed_X():
    mem = MemoryMock([0xF6, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0x00)
    mem.write(0x000055, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (8, 9)
    assert mem.read(0x000054) == 0x01
    assert mem.read(0x000055) == 0x00
    assert cpu.P == 0b00000000  # no flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_indexed_X_8BIT():
    mem = MemoryMock([0xF6, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0x00)
    mem.write(0x000055, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7)
    assert mem.read(0x000054) == 0x01
    assert mem.read(0x000055) == 0x00
    assert cpu.P == 0b00100000  # no flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_indexed_X_Zero():
    mem = MemoryMock([0xF6, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0xFF)
    mem.write(0x000055, 0xFF)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (8, 9)
    assert mem.read(0x000054) == 0x00
    assert mem.read(0x000055) == 0x00
    assert cpu.P == 0b00000010  # zero flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_indexed_X_Zero_8BIT():
    mem = MemoryMock([0xF6, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0xFF)
    mem.write(0x000055, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7)
    assert mem.read(0x000054) == 0x00
    assert mem.read(0x000055) == 0x00
    assert cpu.P == 0b00100010  # zero flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_indexed_X_no_overflow():
    mem = MemoryMock([0xF6, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0xFF) # 32.767 (MAX INT)
    mem.write(0x000055, 0x7F)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (8, 9)
    assert mem.read(0x000054) == 0x00 # -32.768 (MIN INT)
    assert mem.read(0x000055) == 0x80
    assert cpu.P == 0b10000000  # negative flag, no overflow flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_DP_indexed_X_no_overflow_8BIT():
    mem = MemoryMock([0xF6, 0x30])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80  # should have no effect
    cpu.DP = 0x0020
    cpu.X = 0x0004
    mem.write(0x000054, 0x7F) # 127 (MAX INT)
    mem.write(0x000055, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles in (6, 7)
    assert mem.read(0x000054) == 0x80 # -128 (MIN INT)
    assert mem.read(0x000055) == 0x00
    assert cpu.P == 0b10100000  # negative flag, no overflow flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_INC_abs_indexed_X():
    mem = MemoryMock([0xFE, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0x00) # no wrapping
    mem.write(0x808002, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 9
    assert mem.read(0x808001) == 0x01
    assert mem.read(0x808002) == 0x00
    assert cpu.P == 0b00000000 # no flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_abs_indexed_X_8BIT():
    mem = MemoryMock([0xFE, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0x00) # no wrapping
    mem.write(0x808002, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 7
    assert mem.read(0x808001) == 0x01
    assert mem.read(0x808002) == 0x00
    assert cpu.P == 0b00100000 # no flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_abs_indexed_X_Zero():
    mem = MemoryMock([0xFE, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0xFF) # no wrapping
    mem.write(0x808002, 0xFF)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 9
    assert mem.read(0x808001) == 0x00
    assert mem.read(0x808002) == 0x00
    assert cpu.P == 0b00000010 # zero flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_abs_indexed_X_Zero_8BIT():
    mem = MemoryMock([0xFE, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0xFF) # no wrapping
    mem.write(0x808002, 0x00)
    cpu.fetch_decode_execute()

    assert cpu.cycles == 7
    assert mem.read(0x808001) == 0x00
    assert mem.read(0x808002) == 0x00
    assert cpu.P == 0b00100010 # zero flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_abs_indexed_X_no_overflow():
    mem = MemoryMock([0xFE, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0xFF) # no wrapping
    mem.write(0x808002, 0x7F) # 32.767 (MAX INT)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 9
    assert mem.read(0x808001) == 0x00 # -32.768 (MIN INT)
    assert mem.read(0x808002) == 0x80
    assert cpu.P == 0b10000000 # negative flag, no overflow flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INC_abs_indexed_X_no_overflow_8BIT():
    mem = MemoryMock([0xFE, 0x00, 0x80])
    cpu = CPU65816(mem)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    mem.write(0x808001, 0x7F) # no wrapping
    mem.write(0x808002, 0x00) # 128(MAX INT)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 7
    assert mem.read(0x808001) == 0x80 # -127(MIN INT)
    assert mem.read(0x808002) == 0x00
    assert cpu.P == 0b10100000 # negative flag, no overflow flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_INX():
    mem = MemoryMock([0xE8])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.X = 0x0000

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.X == 0x0001
    assert cpu.P == 0b00000000 # no flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INX_8BIT():
    mem = MemoryMock([0xE8])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.X = 0x00

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.X == 0x01
    assert cpu.P == 0b00010000 # no flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INX_Zero():
    mem = MemoryMock([0xE8])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.X = 0xFFFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.X == 0x0000
    assert cpu.P == 0b00000010 # zero flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INX_Zero_8BIT():
    mem = MemoryMock([0xE8])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000  # 8 Bit mode
    cpu.e = 0
    cpu.X = 0xFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.X == 0x00
    assert cpu.P == 0b00010010  # zero flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INX_no_overflow():
    mem = MemoryMock([0xE8])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.X = 0x7FFF # 32.767 (Max Int)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.X == 0x8000      # -32.768 (MIN INT)
    assert cpu.P == 0b10000000  # negative flag, no overflow flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INX_no_overflow_8BIT():
    mem = MemoryMock([0xE8])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000  # 8 Bit mode
    cpu.e = 0
    cpu.X = 0x7F # 127 (Max Int)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.X == 0x80        # -128 (MIN INT)
    assert cpu.P == 0b10010000  # negative flag, no overflow flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INY():
    mem = MemoryMock([0xC8])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.Y = 0x0000

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.Y == 0x0001
    assert cpu.P == 0b00000000 # no flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INY_8BIT():
    mem = MemoryMock([0xC8])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000 # 8 Bit mode
    cpu.e = 0
    cpu.Y = 0x00

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.Y == 0x01
    assert cpu.P == 0b00010000 # no flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INY_Zero():
    mem = MemoryMock([0xC8])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.Y = 0xFFFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.Y == 0x0000
    assert cpu.P == 0b00000010  # zero flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INY_Zero_8BIT():
    mem = MemoryMock([0xC8])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000  # 8 Bit mode
    cpu.e = 0
    cpu.Y = 0xFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.Y == 0x00
    assert cpu.P == 0b00010010  # zero flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INY_no_overflow():
    mem = MemoryMock([0xC8])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.Y = 0x7FFF      # 32.767 (Max Int)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.Y == 0x8000 # -32.768 (MIN INT)
    assert cpu.P == 0b10000000  # negative flag, no overflow flag
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_INY_no_overflow_8BIT():
    mem = MemoryMock([0xC8])
    cpu = CPU65816(mem)
    cpu.P = 0b00010000  # 8 Bit mode
    cpu.e = 0
    cpu.Y = 0x7F        # 127 (Max Int)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.Y == 0x80 # -128 (MIN INT)
    assert cpu.P == 0b10010000  # negative flag, no overflow flag
    assert cpu.PC == 1 + mem.header.reset_int_addr
