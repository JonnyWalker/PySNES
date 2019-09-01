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


def test_ADC_imm_setZ_8bit():
    ROM = [0x69, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x00

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x00
    assert cpu.P == 0b00100010  # zero flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_imm_clearZ_8bit():
    ROM = [0x69, 0x10]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00100010  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x00

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x10
    assert cpu.P == 0b00100000  # no zero flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_imm_setN_8bit():
    ROM = [0x69, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x8F

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x8F
    assert cpu.P == 0b10100000  # negative flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_imm_clearN_8bit():
    ROM = [0x69, 0x10]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b10100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x00

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x10
    assert cpu.P == 0b00100000  # no negative flag
    assert cpu.PC == 2 + mem.header.reset_int_addr

def test_ADC_imm_setV_8bit():
    ROM = [0x69, 0x01]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x7F

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x80
    assert cpu.P == 0b11100000  # overflow + negative flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_imm_clearV_8bit():
    ROM = [0x69, 0x10]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x00

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x10
    assert cpu.P == 0b00100000  # no overflow + negative flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_imm_setC_8bit():
    ROM = [0x69, 0x02]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0xFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x01
    assert cpu.P == 0b00100001  # carry flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_imm_clearC_8bit():
    ROM = [0x69, 0x01]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00100001  # 8 Bit mode
    cpu.e = 0
    cpu.A = 0x01

    cpu.fetch_decode_execute()

    assert cpu.cycles == 2
    assert cpu.A == 0x03  # A + const + carry = 3
    assert cpu.P == 0b00100000  # no carry flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_imm_setZ_16bit():
    ROM = [0x69, 0x00, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0000

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x0000
    assert cpu.P == 0b00000010  # zero flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_imm_clearZ_16bit():
    ROM = [0x69, 0x10, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000010  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0000

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x0010
    assert cpu.P == 0b00000000  # no zero flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_imm_setN_16bit():
    ROM = [0x69, 0x00, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x8FFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x8FFF
    assert cpu.P == 0b10000000  # negative flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_imm_clearN_16bit():
    ROM = [0x69, 0x10, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b10000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0000

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x0010
    assert cpu.P == 0b00000000  # no negative flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_imm_setV_16bit():
    ROM = [0x69, 0x01, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x7FFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x8000
    assert cpu.P == 0b11000000  # overflow + negative flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_imm_clearV_16bit():
    ROM = [0x69, 0x10, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0000

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x0010
    assert cpu.P == 0b00000000  # no overflow + negative flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_imm_setC_16bit():
    ROM = [0x69, 0x02, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0xFFFF

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x0001
    assert cpu.P == 0b00000001  # carry flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_imm_clearC_16bit():
    ROM = [0x69, 0x01, 0x00]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000001  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0001

    cpu.fetch_decode_execute()

    assert cpu.cycles == 3
    assert cpu.A == 0x03  # A + const + carry = 3
    assert cpu.P == 0b00000000  # no carry flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_DP_indexed_indirect_X():
    ROM = [0x61, 0x02]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11000010  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0x1111

    mem.write(0x000026, 0x09)
    mem.write(0x000027, 0x88)

    mem.write(0x808809, 0x22)
    mem.write(0x80880A, 0x22)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert cpu.A == 0x3333
    assert cpu.P == 0b00000000  # no flags
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_stack_relative():
    ROM = [0x63, 0x01]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11000010  # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0x1FF0
    cpu.A = 0x7777

    mem.write(0x001FF1, 0x11)
    mem.write(0x001FF2, 0x11)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0x8888
    assert cpu.P == 0b11000000  # negative and overflow flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_DP():
    ROM = [0x65, 0x34]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1200
    cpu.A = 0xAAAA

    mem.write(0x001234, 0xAA)
    mem.write(0x001235, 0xAA)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 4
    assert cpu.A == 0x5554
    assert cpu.P == 0b00000001  # carry flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_DP_indirect_long():
    ROM = [0x67, 0x10]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.A = 0xFFFF

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x23)

    mem.write(0x234030, 0x01)
    mem.write(0x234031, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert cpu.A == 0x0000
    assert cpu.P == 0b00000011  # carry and zero flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_absolute():
    ROM = [0x6D, 0x56, 0x34]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11000011  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x12
    cpu.A = 0x7000

    mem.write(0x123456, 0x00)
    mem.write(0x123457, 0x10)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 5
    assert cpu.A == 0x8001
    assert cpu.P == 0b11000000  # negative and overflow flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_long():
    ROM = [0x6F, 0x56, 0x34, 0x12]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11000010 # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0000

    mem.write(0x123456, 0xFF)
    mem.write(0x123457, 0x0F)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert cpu.A == 0x0FFF
    assert cpu.P == 0b00000000  # no flags
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_ADC_DP_indirect_indexed_Y():
    ROM = [0x71, 0x10]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
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
    assert cpu.A == 0x1EFF
    assert cpu.P == 0b00000000  # no flags
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_DP_indirect():
    ROM = [0x72, 0x10]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000 # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.DP = 0x0020
    cpu.A = 0x1234

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)

    mem.write(0x804030, 0x21)
    mem.write(0x804031, 0x43)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 7
    assert cpu.A == 0x5555
    assert cpu.P == 0b00000000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_stack_relative_indirect_indexed_Y():
    ROM = [0x73, 0xFA]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000001  # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0xFF10
    cpu.Y = 0x50
    cpu.DBR = 0x12
    cpu.A = 0x7FFF

    mem.write(0x00000A, 0xF0) # 0x1000A becomes 0x000A
    mem.write(0x00000B, 0xFF) # 0x1000B becomes 0x000B

    mem.write(0x130040, 0x00)
    mem.write(0x130041, 0x80)

    cpu.fetch_decode_execute()
    assert cpu.cycles == 8
    assert cpu.A == 0x0000
    assert cpu.P == 0b01000011  # negative, zero and carry flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_DP_indexed_X():
    ROM = [0x75, 0x30]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11000010  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.X = 0x0004
    cpu.A = 0x0F0F

    mem.write(0x000054, 0xF0)
    mem.write(0x000055, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 6
    assert cpu.A == 0x0FFF
    assert cpu.P == 0b00000000  # no flags
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_DP_indirect_long_indexed_Y():
    ROM = [0x77, 0x10]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000001  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0020
    cpu.Y = 0x0001
    cpu.A = 0xFFFF

    mem.write(0x000030, 0x30)
    mem.write(0x000031, 0x40)
    mem.write(0x000032, 0x50)

    mem.write(0x504031, 0x00)
    mem.write(0x504032, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles == 8
    assert cpu.A == 0x0000
    assert cpu.P == 0b00000011  # zero and carry flag
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_ADC_abs_indexed_Y():
    ROM = [0x79, 0x00, 0x80]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.Y = 0x0001
    cpu.A = 0x7FFF

    mem.write(0x808001, 0x01) # no wrapping
    mem.write(0x808002, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 6
    assert cpu.A == 0x8000
    assert cpu.P == 0b11000000  # overflow and negative flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_abs_indexed_X():
    ROM = [0x7D, 0x00, 0x80]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11000011  # 16 Bit mode
    cpu.e = 0
    cpu.DBR = 0x80
    cpu.X = 0x0001
    cpu.A = 0xFFFF

    mem.write(0x808001, 0xFF) # no wrapping
    mem.write(0x808002, 0xFF)

    cpu.fetch_decode_execute()

    assert cpu.cycles >= 6
    assert cpu.A == 0xFFFF
    assert cpu.P == 0b10000001  # carry and negative flag
    assert cpu.PC == 3 + mem.header.reset_int_addr


def test_ADC_long_indexed_X():
    ROM = [0x7F, 0x00, 0x80, 0x80]
    mem = MemoryMock(ROM)
    cpu = CPU65816(mem)
    cpu.P = 0b11000011  # 16 Bit mode
    cpu.e = 0
    cpu.X = 0x0001
    cpu.A = 0x1234

    mem.write(0x808001, 0xCD)
    mem.write(0x808002, 0xAB)

    cpu.fetch_decode_execute()
    assert cpu.cycles == 6
    assert cpu.A == 0xBE02
    assert cpu.P == 0b11000000  # negative and overflow flag
    assert cpu.PC == 4 + mem.header.reset_int_addr
