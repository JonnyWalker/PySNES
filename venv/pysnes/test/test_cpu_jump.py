from pysnes.cpu import CPU65816

# .../PySNES/venv/$ py.test pysnes/test/
class MemoryMock(object):
    def __init__(self):
        self.ram = [0x00] * 0xFFFFFF

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value

def test_JMP_abs():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x4C, 0x34, 0x12])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 0x1234


def test_JMP_abs2():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x4C, 0x34, 0x12])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 0x1234


def test_JMP_long():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.PBR = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x5C, 0x56, 0x34, 0x12])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 4
    assert cpu.PC == 0x3456
    assert cpu.PBR == 0x12


def test_JMP_abs_indirect():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.PBR = 0
    mem.write(0x000000, 0x34)
    mem.write(0x00FFFF, 0x56) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    cpu.fetch_decode_execute([0x6C, 0xFF, 0xFF])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 5
    assert cpu.PC == 0x3456
    assert cpu.PBR == 0


def test_JMP_abs_indirect_indexed_X():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.PBR = 0
    cpu.X = 0xF
    mem.write(0x000000, 0x34)
    mem.write(0x00FFFF, 0x56) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    cpu.fetch_decode_execute([0x7C, 0xF0, 0xFF])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 6
    assert cpu.PC == 0x3456
    assert cpu.PBR == 0


def test_JMP_abs_indirect_3byte():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.PBR = 0
    mem.write(0x000000, 0x34)
    mem.write(0x000001, 0x12)
    mem.write(0x00FFFF, 0x56) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    cpu.fetch_decode_execute([0xDC, 0xFF, 0xFF])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 6
    assert cpu.PC == 0x3456
    assert cpu.PBR == 0x12


def test_JSR_abs():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PBR = 0x12
    cpu.PC = 0x3456
    cpu.SP = 0x01FF
    nops = [0xEA] * ((cpu.PBR << 16) + cpu.PC)
    cpu.fetch_decode_execute(nops+[0x20, 0xCD, 0xAB])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 6
    assert cpu.PBR == 0x12
    assert cpu.PC == 0xABCD
    assert mem.read(0x0001FF) == 0x34
    assert mem.read(0x0001FE) == 0x56 + 2
    assert cpu.SP == 0x01FD


def test_JSR_abs_indirect_indexed_X():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0x3456
    cpu.SP = 0x01FF
    cpu.PBR = 0x12
    cpu.X = 0xF
    mem.write(0x000000, 0xAB)
    mem.write(0x00FFFF, 0xCD) # zero bank wrapping!
    mem.write(0x010000, 0x00)
    nops = [0xEA] * ((cpu.PBR << 16) + cpu.PC)
    cpu.fetch_decode_execute(nops+[0xFC, 0xF0, 0xFF])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 8
    assert cpu.PC == 0xABCD
    assert cpu.PBR == 0x12
    assert mem.read(0x0001FF) == 0x34
    assert mem.read(0x0001FE) == 0x56 + 2
    assert cpu.SP == 0x01FD


def test_JSR_long():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0x3456
    cpu.SP = 0x01FF
    cpu.PBR = 0x06
    nops = [0xEA] * ((cpu.PBR << 16) + cpu.PC)
    cpu.fetch_decode_execute(nops+[0x22, 0xCD, 0xAB, 0x12])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 8
    assert cpu.PC == 0xABCD
    assert cpu.PBR == 0x12
    assert mem.read(0x0001FF) == 0x06 # old PBR register
    assert mem.read(0x0001FE) == 0x34
    assert mem.read(0x0001FD) == 0x56 + 3
    assert cpu.SP == 0x01FC
