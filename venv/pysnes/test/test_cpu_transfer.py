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
    assert cpu.PC == 1


def test_tcd_zero():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0000

    cpu.fetch_decode_execute([0x5B])

    assert cpu.cycles == 2
    assert cpu.DP == 0x0000
    assert cpu.P == 0b0000010  # zero flag
    assert cpu.PC == 1


def test_tcd_negative():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0xF234

    cpu.fetch_decode_execute([0x5B])

    assert cpu.cycles == 2
    assert cpu.DP == 0xF234
    assert cpu.P == 0b10000000  # negative flag
    assert cpu.PC == 1


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
    assert cpu.PC == 1


def test_tcs_16_zero():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0x0000

    cpu.fetch_decode_execute([0x1B])

    assert cpu.cycles == 2
    assert cpu.SP == 0x0000
    assert cpu.P == 0b0000010  # zero flag
    assert cpu.PC == 1


def test_tcs_16_negative():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.A = 0xF234

    cpu.fetch_decode_execute([0x1B])

    assert cpu.cycles == 2
    assert cpu.SP == 0xF234
    assert cpu.P == 0b10000000  # negative flag
    assert cpu.PC == 1


def test_tcs_8():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 1
    cpu.A = 0x34
    cpu.SP = 0x3412

    cpu.fetch_decode_execute([0x1B])

    assert cpu.cycles == 2
    assert cpu.SP == 0x3434
    assert cpu.P == 0b00100000  # no flag
    assert cpu.PC == 1


def test_tcs_8_zero():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 1
    cpu.A = 0x00
    cpu.SP = 0x3412

    cpu.fetch_decode_execute([0x1B])

    assert cpu.cycles == 2
    assert cpu.SP == 0x3400
    assert cpu.P == 0b00100010  # zero flag
    assert cpu.PC == 1


def test_tcs_8_negative():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00100000  # 8 Bit mode
    cpu.e = 1
    cpu.A = 0x80
    cpu.SP = 0x3412

    cpu.fetch_decode_execute([0x1B])

    assert cpu.cycles == 2
    assert cpu.SP == 0x3480
    assert cpu.P == 0b10100000  # negative flag
    assert cpu.PC == 1


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
    assert cpu.PC == 1


def test_tdc_zero():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0x0000

    cpu.fetch_decode_execute([0x7B])

    assert cpu.cycles == 2
    assert cpu.A == 0x0000
    assert cpu.P == 0b0000010  # zero flag
    assert cpu.PC == 1


def test_tdc_negative():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.DP = 0xF234

    cpu.fetch_decode_execute([0x7B])

    assert cpu.cycles == 2
    assert cpu.A == 0xF234
    assert cpu.P == 0b10000000  # negative flag
    assert cpu.PC == 1


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
    assert cpu.PC == 1


def test_tsc_zero():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0x0000

    cpu.fetch_decode_execute([0x3B])

    assert cpu.cycles == 2
    assert cpu.A == 0x0000
    assert cpu.P == 0b0000010  # zero flag
    assert cpu.PC == 1


def test_tsc_negative():
    mem = MemoryMock()
    cpu = CPU65816(mem)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.e = 0
    cpu.SP = 0xF234

    cpu.fetch_decode_execute([0x3B])

    assert cpu.cycles == 2
    assert cpu.A == 0xF234
    assert cpu.P == 0b10000000  # negative flag
    assert cpu.PC == 1


def test_xba():
    cpu = CPU65816(None)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.A = 0x6789

    cpu.fetch_decode_execute([0xEB])

    assert cpu.A == 0x8967
    assert cpu.P == 0b00000000  # result is based on AL
    assert cpu.cycles == 3
    assert cpu.PC == 1


def test_xba2():
    cpu = CPU65816(None)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.A = 0xF789

    cpu.fetch_decode_execute([0xEB])

    assert cpu.A == 0x89F7
    assert cpu.P == 0b10000000  # result is based on AL
    assert cpu.cycles == 3
    assert cpu.PC == 1


def test_xba3():
    cpu = CPU65816(None)
    cpu.P = 0b00000000  # 16 Bit mode
    cpu.A = 0x0089

    cpu.fetch_decode_execute([0xEB])

    assert cpu.A == 0x8900
    assert cpu.P == 0b00000010  # result is based on AL
    assert cpu.cycles == 3
    assert cpu.PC == 1
