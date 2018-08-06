from tool.cpu import CPU65816

class MemoryMock(object):
    def __init__(self):
        self.ram = [0x00] * 0xFFFFFF

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value


def test_LDA_long():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    mem.write(0x123456, 0xAB)
    mem.write(0x123457, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xAF, 0x56, 0x34, 0x12])
    assert cpu.cycles == 6
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_const16Bit():
    cpu = CPU65816(None)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xA9, 0x34, 0x12])
    assert cpu.cycles == 3
    assert cpu.A == 0x1234
    assert cpu.P == 0b00000000


def test_LDA_const8Bit():
    cpu = CPU65816(None)
    cpu.P = 0b00100000 # 8 Bit mode
    cpu.e = 1
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xA9, 0x34])
    assert cpu.cycles == 2
    assert cpu.A == 0x34
    assert cpu.P == 0b00100000


def test_LDA_DP():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    mem.write(0x001234, 0xAB)
    cpu.DP = 0x1200
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xA5, 0x34])
    assert cpu.cycles in (3, 4, 5)
    assert cpu.A == 0x00AB
    assert cpu.P == 0b00000000


def test_LDA_absolute():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    mem.write(0x123456, 0xAB)
    mem.write(0x123457, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xAD, 0x56, 0x34])
    assert cpu.cycles == 5
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_DP_indirect_indexed_Y():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)
    mem.write(0x000033, 0x22)
    mem.write(0x000034, 0xFA)
    mem.write(0x000035, 0x22)
    mem.write(0x000036, 0x23)
    mem.write(0x000037, 0x1C)

    mem.write(0x000038, 0x23)
    mem.write(0x000039, 0x2D)
    mem.write(0x00003A, 0xDD)
    mem.write(0x00003B, 0xF4)
    mem.write(0x00003C, 0xFF)
    mem.write(0x00003D, 0xFF)
    mem.write(0x00003E, 0xFF)
    mem.write(0x00003F, 0xFF)

    mem.write(0x804031, 0xAB)
    mem.write(0x804032, 0xCD)
    cpu.P = 0b00000000  # 16 Bit mode
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xB1, 0x10])
    assert cpu.cycles >= 5
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_DP_indirect():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)
    mem.write(0x000033, 0x22)
    mem.write(0x000034, 0xFA)
    mem.write(0x000035, 0x22)
    mem.write(0x000036, 0x23)
    mem.write(0x000037, 0x1C)

    mem.write(0x000038, 0x23)
    mem.write(0x000039, 0x2D)
    mem.write(0x00003A, 0xDD)
    mem.write(0x00003B, 0xF4)
    mem.write(0x00003C, 0xFF)
    mem.write(0x00003D, 0xFF)
    mem.write(0x00003E, 0xFF)
    mem.write(0x00003F, 0xFF)

    mem.write(0x804030, 0xAB)
    mem.write(0x804031, 0xCD)
    cpu.P = 0b00000000  # 16 Bit mode
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xB2, 0x10])
    assert cpu.cycles in (6, 7)
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000

def test_LDA_DP_indirect_long_indexed_Y():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)
    mem.write(0x000033, 0x22)
    mem.write(0x000034, 0xFA)
    mem.write(0x000035, 0x22)
    mem.write(0x000036, 0x23)
    mem.write(0x000037, 0x1C)

    mem.write(0x000038, 0x23)
    mem.write(0x000039, 0x2D)
    mem.write(0x00003A, 0xDD)
    mem.write(0x00003B, 0xF4)
    mem.write(0x00003C, 0xFF)
    mem.write(0x00003D, 0xFF)
    mem.write(0x00003E, 0xFF)
    mem.write(0x00003F, 0xFF)

    mem.write(0x234031, 0xAB)
    mem.write(0x234032, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xB7, 0x10])
    assert cpu.cycles in (7, 8)
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_DP_indirect_long():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)
    mem.write(0x000033, 0x22)
    mem.write(0x000034, 0xFA)
    mem.write(0x000035, 0x22)
    mem.write(0x000036, 0x23)
    mem.write(0x000037, 0x1C)

    mem.write(0x000038, 0x23)
    mem.write(0x000039, 0x2D)
    mem.write(0x00003A, 0xDD)
    mem.write(0x00003B, 0xF4)
    mem.write(0x00003C, 0xFF)
    mem.write(0x00003D, 0xFF)
    mem.write(0x00003E, 0xFF)
    mem.write(0x00003F, 0xFF)

    mem.write(0x234030, 0xAB)
    mem.write(0x234031, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xA7, 0x10])
    assert cpu.cycles in (6, 7, 8)
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_DP_indexed_indirect_X():
    mem = MemoryMock()
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
    mem.write(0x000026, 0x09)
    mem.write(0x000027, 0x88)

    mem.write(0x000028, 0x08)
    mem.write(0x000029, 0x76)
    mem.write(0x00002A, 0x66)
    mem.write(0x00002B, 0x36)
    mem.write(0x00002C, 0xD7)
    mem.write(0x00002D, 0x23)
    mem.write(0x00002E, 0x99)
    mem.write(0x00002F, 0x00)

    mem.write(0x808809, 0xAB)
    mem.write(0x80880A, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xA1, 0x02])
    assert cpu.cycles in (6,7,8)
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_DP_indexed_X():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.X = 0x0004

    mem.write(0x000054, 0xAB)
    mem.write(0x000055, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xB5, 0x30])
    assert cpu.cycles in (5, 6)
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_abs_indexed_X():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001

    mem.write(0x808001, 0xAB)
    mem.write(0x808002, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xBD, 0x00, 0x80])
    assert cpu.cycles >= 6
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_abs_indexed_Y():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.Y = 0x0001

    mem.write(0x808001, 0xAB)
    mem.write(0x808002, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xB9, 0x00, 0x80])
    assert cpu.cycles >= 6
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_long_indexed_X():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.X = 0x0001

    mem.write(0x808001, 0xAB)
    mem.write(0x808002, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xBF, 0x00, 0x80, 0x80])
    assert cpu.cycles == 6
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_stack_relative():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0x1FF0

    mem.write(0x001FF1, 0xAB)
    mem.write(0x001FF2, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xA3, 0x01])
    assert cpu.cycles == 5
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000


def test_LDA_stack_relative_indirect_indexed_Y():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0xFF10
    cpu.Y = 0x50
    cpu.DBR = 0x13

    mem.write(0x00000A, 0xF0) # 0x1000A becomes 0x000A
    mem.write(0x00000B, 0xFF) # 0x1000B becomes 0x000B

    mem.write(0x130040, 0xAB)
    mem.write(0x130041, 0xCD)
    assert cpu.A == 0
    cpu.fetch_decode_execute([0xB3, 0xFA])
    assert cpu.cycles == 8
    assert cpu.A == 0xCDAB
    assert cpu.P == 0b10000000