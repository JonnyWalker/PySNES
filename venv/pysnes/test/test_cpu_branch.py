from pysnes.cpu import CPU65816

# .../PySNES/venv/$ py.test pysnes/test/

# cycles = 2+t+t*e*p
# t = branch taken
# e = emulation mode
# p = page crossed

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


# jump if C==0 to PC + 2 + OFFSET
def test_BCC_forward():
    mem = MemoryMock([0x90, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 + mem.header.reset_int_addr # 0 + 2 + 5


# jump if C==0 to PC + 2 + OFFSET
def test_BCC_backward():
    mem = MemoryMock([0x90, 0xF9], start=10)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 10

    cpu.fetch_decode_execute() # -7

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 + mem.header.reset_int_addr # 10 + 2 - 7


# jump if C==0 to PC + 2 + OFFSET
def test_BCC_no_branch():
    mem = MemoryMock([0x90, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000001
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000001
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 + mem.header.reset_int_addr # 0 + 2


# jump if C==0 to PC + 2 + OFFSET
def test_BCC_branch_page_boundary():
    mem = MemoryMock([0x90, 0x05], start=253)
    cpu = CPU65816(mem)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC += 253

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 + mem.header.reset_int_addr # 253 + 2 + 5


# jump if C==0 to PC + 2 + OFFSET
def test_BCC_wrapped_execution():
    mem = MemoryMock([0x90, 0x0F], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_forward():
    mem = MemoryMock([0xB0, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000001
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000001
    assert cpu.cycles == 3
    assert cpu.PC == 7 + mem.header.reset_int_addr # 0 + 2 + 5


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_backward():
    mem = MemoryMock([0xB0, 0xF9], start=10)
    cpu = CPU65816(mem)
    cpu.P = 0b00000001
    cpu.PC += 10

    cpu.fetch_decode_execute() # -7

    assert cpu.P == 0b00000001
    assert cpu.cycles == 3
    assert cpu.PC == 5 + mem.header.reset_int_addr # 10 + 2 - 7


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_no_branch():
    mem = MemoryMock([0xB0, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 + mem.header.reset_int_addr # 0 + 2


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_branch_page_boundary():
    mem = MemoryMock([0xB0, 0x05], start=253)
    cpu = CPU65816(mem)
    cpu.e = 1
    cpu.P = 0b00110001
    cpu.PC += 253

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00110001
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 + mem.header.reset_int_addr # 253 + 2 + 5


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_wrapped_execution():
    mem = MemoryMock([0xB0, 0x0F], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b00000001
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00000001
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_forward():
    mem = MemoryMock([0xF0, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000010
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000010
    assert cpu.cycles == 3
    assert cpu.PC == 7 + mem.header.reset_int_addr # 0 + 2 + 5


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_backward():
    mem = MemoryMock([0xF0, 0xF9], start=10)
    cpu = CPU65816(mem)
    cpu.P = 0b00000010
    cpu.PC += 10

    cpu.fetch_decode_execute() # -7

    assert cpu.P == 0b00000010
    assert cpu.cycles == 3
    assert cpu.PC == 5 + mem.header.reset_int_addr # 10 + 2 - 7


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_no_branch():
    mem = MemoryMock([0xF0, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b0000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 + mem.header.reset_int_addr # 0 + 2


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_branch_page_boundary():
    mem = MemoryMock([0xF0, 0x05], start=253)
    cpu = CPU65816(mem)
    cpu.e = 1
    cpu.P = 0b00110010
    cpu.PC += 253

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00110010
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 + mem.header.reset_int_addr # 253 + 2 + 5


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_wrapped_execution():
    mem = MemoryMock([0xF0, 0x0F], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b00000010
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00000010
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_forward():
    mem = MemoryMock([0xD0, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 + mem.header.reset_int_addr # 0 + 2 + 5


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_backward():
    mem = MemoryMock([0xD0, 0xF9], start=10)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 10

    cpu.fetch_decode_execute() # -7

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 + mem.header.reset_int_addr # 10 + 2 - 7


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_no_branch():
    mem = MemoryMock([0xD0, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b0000010
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000010
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 + mem.header.reset_int_addr # 0 + 2


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_branch_page_boundary():
    mem = MemoryMock([0xD0, 0x05], start=253)
    cpu = CPU65816(mem)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC += 253

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 + mem.header.reset_int_addr # 253 + 2 + 5


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_wrapped_execution():
    mem = MemoryMock([0xD0, 0x0F], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_forward():
    mem = MemoryMock([0x30, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b10000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b10000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 + mem.header.reset_int_addr # 0 + 2 + 5


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_backward():
    mem = MemoryMock([0x30, 0xF9], start=10)
    cpu = CPU65816(mem)
    cpu.P = 0b10000000
    cpu.PC += 10

    cpu.fetch_decode_execute() # -7

    assert cpu.P == 0b10000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 + mem.header.reset_int_addr # 10 + 2 - 7


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_no_branch():
    mem = MemoryMock([0x30, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 + mem.header.reset_int_addr # 0 + 2


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_branch_page_boundary():
    mem = MemoryMock([0x30, 0x05], start=253)
    cpu = CPU65816(mem)
    cpu.e = 1
    cpu.P = 0b10110000
    cpu.PC += 253

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b10110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 + mem.header.reset_int_addr # 253 + 2 + 5


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_wrapped_execution():
    mem = MemoryMock([0x30, 0x0F], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b10000000
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b10000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_forward():
    mem = MemoryMock([0x10, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 + mem.header.reset_int_addr # 0 + 2 + 5


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_backward():
    mem = MemoryMock([0x10, 0xF9], start=10)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 10

    cpu.fetch_decode_execute() # -7

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 + mem.header.reset_int_addr # 10 + 2 - 7


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_no_branch():
    mem = MemoryMock([0x10, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b10000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b10000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 + mem.header.reset_int_addr # 0 + 2


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_branch_page_boundary():
    mem = MemoryMock([0x10, 0x05], start=253)
    cpu = CPU65816(mem)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC += 253

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 + mem.header.reset_int_addr # 253 + 2 + 5


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_wrapped_execution():
    mem = MemoryMock([0x10, 0x0F], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_forward():
    mem = MemoryMock([0x50, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 + mem.header.reset_int_addr # 0 + 2 + 5


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_backward():
    mem = MemoryMock([0x50, 0xF9], start=10)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 10

    cpu.fetch_decode_execute() # -7

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 + mem.header.reset_int_addr # 10 + 2 - 7


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_no_branch():
    mem = MemoryMock([0x50, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b01000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b01000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 + mem.header.reset_int_addr # 0 + 2


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_branch_page_boundary():
    mem = MemoryMock([0x50, 0x05], start=253)
    cpu = CPU65816(mem)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC += 253

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 + mem.header.reset_int_addr # 253 + 2 + 5


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_wrapped_execution():
    mem = MemoryMock([0x50, 0x0F], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_forward():
    mem = MemoryMock([0x70, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b01000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b01000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 + mem.header.reset_int_addr # 0 + 2 + 5


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_backward():
    mem = MemoryMock([0x70, 0xF9], start=10)
    cpu = CPU65816(mem)
    cpu.P = 0b01000000
    cpu.PC += 10

    cpu.fetch_decode_execute() # -7

    assert cpu.P == 0b01000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 + mem.header.reset_int_addr # 10 + 2 - 7


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_no_branch():
    mem = MemoryMock([0x70, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 + mem.header.reset_int_addr # 0 + 2


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_branch_page_boundary():
    mem = MemoryMock([0x70, 0x05], start=253)
    cpu = CPU65816(mem)
    cpu.e = 1
    cpu.P = 0b01110000
    cpu.PC += 253

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b01110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 + mem.header.reset_int_addr # 253 + 2 + 5


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_wrapped_execution():
    mem = MemoryMock([0x70, 0x0F], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b01000000
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b01000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump to PC + 2 + OFFSET
def test_BRA_forward():
    mem = MemoryMock([0x80, 0x05])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 + mem.header.reset_int_addr # 0 + 2 + 5


# jump to PC + 2 + OFFSET
def test_BRA_backward():
    mem = MemoryMock([0x80, 0xF9], start=10)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 10

    cpu.fetch_decode_execute() # -7

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 + mem.header.reset_int_addr # 10 + 2 - 7


# jump to PC + 2 + OFFSET
def test_BRA_branch_page_boundary():
    mem = MemoryMock([0x80, 0x05], start=253)
    cpu = CPU65816(mem)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC += 253

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 + mem.header.reset_int_addr # 253 + 2 + 5


# jump to PC + 2 + OFFSET
def test_BRA_wrapped_execution():
    mem = MemoryMock([0x80, 0x0F], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# maybe wrong example at http://www.6502.org/tutorials/65c816opcodes.html#6.2.1.2
# maybe $C045 must be $0042
# jump to PC + 3 + OFFSET
def test_BRL_forward():
    mem = MemoryMock([0x82, 0x05, 0x00])
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC += 0

    cpu.fetch_decode_execute()

    assert cpu.P == 0b00000000
    assert cpu.cycles == 4
    assert cpu.PC == 8 + mem.header.reset_int_addr # 0 + 3 + 5


# jump to PC + 3 + OFFSET
def test_BRL_wrapped_execution():
    mem = MemoryMock([0x82, 0x0F, 0x00], start=0x7FF0)
    cpu = CPU65816(mem)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0

    cpu.fetch_decode_execute() # branches forward

    assert cpu.P == 0b00000000
    assert cpu.cycles == 4
    assert (cpu.PC & 0xFFFF) == 2 # 65520 + 3 + 16