from tool.disassembler import Disassembler

def test_random_opcodes():
    binary_code = [0x78, 0x18, 0xFB, 0xC2, 0x10, 0xE2, 0x20, 0x9C,
                   0x0D, 0x42, 0x9C, 0x0B, 0x42, 0x9C, 0x0C, 0x42,
                   0xA9, 0x8F, 0x8D, 0x00, 0x21, 0xA9, 0x00, 0x8D,
                   0x00, 0x42, 0xA9, 0x00, 0xEB, 0xA9, 0x00, 0x48]
    d = Disassembler()
    symbolic_code = d.disassemble(binary_code)
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
