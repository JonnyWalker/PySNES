from pysnes.cpu import CPU65816

# .../PySNES/venv/$ py.test pysnes/test/
class HeaderMock():
    def __init__(self):
        self.reset_int_addr = 0x8000

class MemoryMock(object):
    def __init__(self, ROM, start=0):
        self.ram = {}
        self.ROM = ROM
        self.header = HeaderMock()
        pc = self.header.reset_int_addr
        for byte in ROM:
            self.ram[pc+start] = byte
            pc += 1

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value

def test_JMP_abs():
    mem = MemoryMock([0x4C, 0x34, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 0x1234


def test_JMP_abs2():
    mem = MemoryMock([0x4C, 0x34, 0x12], 0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0x7FF0

    cpu.fetch_decode_execute()
    print(mem.ram)

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 0x1234


def test_JMP_long():
    mem = MemoryMock([0x5C, 0x56, 0x34, 0x12])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0
    cpu.PBR = 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 4
    assert cpu.PC == 0x3456
    assert cpu.PBR == 0x12


def test_JMP_abs_indirect():
    mem = MemoryMock([0x6C, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0
    cpu.PBR = 0
    mem.write(0x000000, 0x34)
    mem.write(0x00FFFF, 0x56) # zero bank wrapping!
    mem.write(0x010000, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 5
    assert cpu.PC == 0x3456
    assert cpu.PBR == 0


def test_JMP_abs_indirect_indexed_X():
    mem = MemoryMock([0x7C, 0xF0, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0
    cpu.PBR = 0
    cpu.X = 0xF
    mem.write(0x000000, 0x34)
    mem.write(0x00FFFF, 0x56) # zero bank wrapping!
    mem.write(0x010000, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 6
    assert cpu.PC == 0x3456
    assert cpu.PBR == 0


def test_JMP_abs_indirect_3byte():
    mem = MemoryMock([0xDC, 0xFF, 0xFF])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0
    cpu.PBR = 0
    mem.write(0x000000, 0x34)
    mem.write(0x000001, 0x12)
    mem.write(0x00FFFF, 0x56) # zero bank wrapping!
    mem.write(0x010000, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 6
    assert cpu.PC == 0x3456
    assert cpu.PBR == 0x12


def test_JSR_abs():
    mem = MemoryMock([0x20, 0xCD, 0xAB], ((0x12 << 16)+0x3456-0x8000))
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PBR = 0x12
    cpu.PC = 0x3456
    cpu.SP = 0x01FF

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 6
    assert cpu.PBR == 0x12
    assert cpu.PC == 0xABCD
    assert mem.read(0x0001FF) == 0x34
    assert mem.read(0x0001FE) == 0x56 + 2
    assert cpu.SP == 0x01FD


def test_JSR_abs_indirect_indexed_X():
    mem = MemoryMock([0xFC, 0xF0, 0xFF], ((0x12 << 16)+0x3456-0x8000))
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0x3456
    cpu.SP = 0x01FF
    cpu.PBR = 0x12
    cpu.X = 0xF
    mem.write(0x000000, 0xAB)
    mem.write(0x00FFFF, 0xCD) # zero bank wrapping!
    mem.write(0x010000, 0x00)

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 8
    assert cpu.PC == 0xABCD
    assert cpu.PBR == 0x12
    assert mem.read(0x0001FF) == 0x34
    assert mem.read(0x0001FE) == 0x56 + 2
    assert cpu.SP == 0x01FD


def test_JSR_long():
    mem = MemoryMock([0x22, 0xCD, 0xAB, 0x12], ((0x06 << 16)++0x3456-0x8000))
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0x3456
    cpu.SP = 0x01FF
    cpu.PBR = 0x06

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 8
    assert cpu.PC == 0xABCD
    assert cpu.PBR == 0x12
    assert mem.read(0x0001FF) == 0x06 # old PBR register
    assert mem.read(0x0001FE) == 0x34
    assert mem.read(0x0001FD) == 0x56 + 3
    assert cpu.SP == 0x01FC


def test_RTS():
    mem = MemoryMock([0x60], ((0x12 << 16)))
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PBR = 0x12
    cpu.SP = 0x01FD
    mem.write(0x0001FF, 0x34)
    mem.write(0x0001FE, 0x56)
    cpu.stack = [0x34, 0x56]

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000 # no effect
    assert cpu.cycles == 6
    assert cpu.PBR == 0x12
    assert cpu.PC == 0x3456 + 1 # the inc to 3456 will be done by the loop
    assert cpu.SP == 0x01FF


def test_RTL():
    mem = MemoryMock([0x6B])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PBR = 0x00
    cpu.SP = 0x01FC
    mem.write(0x0001FF, 0x12)
    mem.write(0x0001FE, 0x34)
    mem.write(0x0001FD, 0x56)
    cpu.stack = [0x12, 0x34, 0x56]

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000 # no effect
    assert cpu.cycles == 6
    assert cpu.PBR == 0x12
    assert cpu.PC == 0x3456 + 1 # the inc to 3456 will be done by the loop
    assert cpu.SP == 0x01FF