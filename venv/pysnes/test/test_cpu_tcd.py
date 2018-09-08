from pysnes.cpu import CPU65816

# .../PySNES/venv/$ py.test pysnes/test/


class MemoryMock(object):
    def __init__(self):
        self.ram = {}

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value

def test_tcd():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x1234

    cpu.fetch_decode_execute([0x5B])

    assert cpu.cycles == 2
    assert cpu.DP == 0x1234
    assert cpu.P == 0b0000000  # no flag


def test_tcs_16():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x1234

    cpu.fetch_decode_execute([0x1B])

    assert cpu.cycles == 2
    assert cpu.SP == 0x1234
    assert cpu.P == 0b0000000  # no flag


def test_tcs_8():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 1
    cpu.A = 0x1234
    cpu.SP = 0x3412

    cpu.fetch_decode_execute([0x1B])

    assert cpu.cycles == 2
    assert cpu.SP == 0x3434
    assert cpu.P == 0b0000000  # no flag

def test_tdc():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x1234

    cpu.fetch_decode_execute([0x7B])

    assert cpu.cycles == 2
    assert cpu.A == 0x1234
    assert cpu.P == 0b0000000  # no flag

def test_tsc():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0x1234

    cpu.fetch_decode_execute([0x3B])

    assert cpu.cycles == 2
    assert cpu.A == 0x1234
    assert cpu.P == 0b0000000  # no flag