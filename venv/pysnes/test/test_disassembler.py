from pysnes.disassembler import Disassembler

# .../PySNES/venv/$ py.test pysnes/test/
class HeaderMock():
    def __init__(self):
        self.reset_int_addr = 0x0

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


def test_random_opcodes():
    binary_code = [0x78, 0x18, 0xFB, 0xC2, 0x10, 0xE2, 0x20, 0x9C,
                   0x0D, 0x42, 0x9C, 0x0B, 0x42, 0x9C, 0x0C, 0x42,
                   0xA9, 0x8F, 0x8D, 0x00, 0x21, 0xA9, 0x00, 0x8D,
                   0x00, 0x42, 0xA9, 0x00, 0xEB, 0xA9, 0x00, 0x48]
    mem = MemoryMock(binary_code)
    d = Disassembler()
    symbolic_code = d.disassemble(mem, 0, len(binary_code), False, False, False, True)
    print(symbolic_code)
    assert symbolic_code == ["SEI",
                             "CLC",
                             "XCE",
                             "REP", "0x10",
                             "SEP", "0x20",
                             "STZ", "0x420d",
                             "STZ", "0x420b",
                             "STZ", "0x420c",
                             "LDA", "0x8f",
                             "STA", "0x2100",
                             "LDA", "0x0",
                             "STA", "0x4200",
                             "LDA", "0x0",
                             "XBA",
                             "LDA", "0x0",
                             "PHA"]
