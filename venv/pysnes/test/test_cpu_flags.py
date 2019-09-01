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


def test_NOP():
    mem = MemoryMock([0xEA])
    cpu = CPU65816(mem)
    assert cpu.P == 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_SEP1():
    mem = MemoryMock([0xE2, 0x00])
    cpu = CPU65816(mem)
    assert cpu.P == 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_SEP2():
    mem = MemoryMock([0xE2, 0x01])
    cpu = CPU65816(mem)
    assert cpu.P == 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000001
    assert cpu.cycles == 3
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_SEP3():
    mem = MemoryMock([0xE2, 0x81])
    cpu = CPU65816(mem)
    assert cpu.P == 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b10000001
    assert cpu.cycles == 3
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_REP0():
    mem = MemoryMock([0xC2, 0x00])
    cpu = CPU65816(mem)
    assert cpu.P == 0b00000000
    cpu.e = 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_REP1():
    mem = MemoryMock([0xC2, 0x00])
    cpu = CPU65816(mem)
    cpu.P = 0b00100010
    cpu.e = 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00100010
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_REP2():
    mem = MemoryMock([0xC2, 0x02])
    cpu = CPU65816(mem)
    cpu.P = 0b00100010
    cpu.e = 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00100000
    assert cpu.PC == 2 + mem.header.reset_int_addr


def test_SEP_REP():
    mem = MemoryMock([0xE2, 0x02, 0xC2, 0x02])
    cpu = CPU65816(mem)
    cpu.e = 0

    cpu.fetch_decode_execute() # SEP 00000 0010
    cpu.fetch_decode_execute() # REP 0000 0010

    assert cpu.P == 0b00000000
    assert cpu.PC == 4 + mem.header.reset_int_addr


def test_CLC():
    mem = MemoryMock([0x18])
    cpu = CPU65816(mem)
    cpu.P = 0b00000001

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_CLC1():
    mem = MemoryMock([0x18])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_SEI():
    mem = MemoryMock([0x78])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000100
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_SEI1():
    mem = MemoryMock([0x78])
    cpu = CPU65816(mem)
    cpu.P = 0b00000100

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000100
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_SED():
    mem = MemoryMock([0xF8])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00001000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_SED1():
    mem = MemoryMock([0xF8])
    cpu = CPU65816(mem)
    cpu.P = 0b00001000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00001000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_SEC():
    mem = MemoryMock([0x38])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000001
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_SEC1():
    mem = MemoryMock([0x38])
    cpu = CPU65816(mem)
    cpu.P = 0b00000001

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000001
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_CLD():
    mem = MemoryMock([0xD8])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_CLD1():
    mem = MemoryMock([0xD8])
    cpu = CPU65816(mem)
    cpu.P = 0b00001000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_CLI():
    mem = MemoryMock([0x58])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_CLI1():
    mem = MemoryMock([0x58])
    cpu = CPU65816(mem)
    cpu.P = 0b00000100

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_CLV():
    mem = MemoryMock([0xB8])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_CLV1():
    mem = MemoryMock([0xB8])
    cpu = CPU65816(mem)
    cpu.P = 0b01000000

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_XCE():
    mem = MemoryMock([0xFB])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.e = 1

    cpu.fetch_decode_execute()

    assert cpu.e == 0
    assert cpu.P == 0b00000001
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_XCE1():
    mem = MemoryMock([0xFB])
    cpu = CPU65816(mem)
    cpu.P = 0b00000001
    cpu.e = 1
    cpu.X = 0x1234
    cpu.Y = 0x5678
    cpu.SP = 0x0201

    cpu.fetch_decode_execute()

    assert cpu.e == 1
    assert cpu.P == 0b00110001
    assert cpu.X == 0x0034
    assert cpu.Y == 0x0078
    assert cpu.SP == 0x0101
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr


def test_XCE2():
    mem = MemoryMock([0xFB])
    cpu = CPU65816(mem)
    cpu.P = 0b00000001
    cpu.e = 0
    cpu.X = 0x1234
    cpu.Y = 0x5678
    cpu.SP = 0x0201

    cpu.fetch_decode_execute()

    assert cpu.e == 1
    assert cpu.P == 0b00110000
    assert cpu.X == 0x0034
    assert cpu.Y == 0x0078
    assert cpu.SP == 0x0101
    assert cpu.cycles == 2
    assert cpu.PC == 1 + mem.header.reset_int_addr