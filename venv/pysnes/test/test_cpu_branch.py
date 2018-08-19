from pysnes.cpu import CPU65816

# .../PySNES/venv/$ py.test pysnes/test/

# jump if C==0 to PC + 2 + OFFSET
def test_BCC_forward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x90, 0x05])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 # 0 + 2 + 5


# jump if C==0 to PC + 2 + OFFSET
def test_BCC_backward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 10
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x90, 0xF9]) # -7
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 # 10 + 2 - 7


# jump if C==0 to PC + 2 + OFFSET
def test_BCC_no_branch():
    cpu = CPU65816(None)
    cpu.P = 0b00000001
    cpu.PC = 0
    cpu.fetch_decode_execute([0x90, 0x05])
    assert cpu.P == 0b00000001
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 # 0 + 2


# jump if C==0 to PC + 2 + OFFSET
def test_BCC_branch_page_boundary():
    cpu = CPU65816(None)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC = 253
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x90, 0x05]) # branches forward
    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 # 253 + 2 + 5


# jump if C==0 to PC + 2 + OFFSET
def test_BCC_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x90, 0x0F]) # branches forward
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_forward():
    cpu = CPU65816(None)
    cpu.P = 0b00000001
    cpu.PC = 0
    cpu.fetch_decode_execute([0xB0, 0x05])
    assert cpu.P == 0b00000001
    assert cpu.cycles == 3
    assert cpu.PC == 7 # 0 + 2 + 5


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_backward():
    cpu = CPU65816(None)
    cpu.P = 0b00000001
    cpu.PC = 10
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0xB0, 0xF9]) # -7
    assert cpu.P == 0b00000001
    assert cpu.cycles == 3
    assert cpu.PC == 5 # 10 + 2 - 7


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_no_branch():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0xB0, 0x05])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 # 0 + 2


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_branch_page_boundary():
    cpu = CPU65816(None)
    cpu.e = 1
    cpu.P = 0b00110001
    cpu.PC = 253
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0xB0, 0x05]) # branches forward
    assert cpu.P == 0b00110001
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 # 253 + 2 + 5


# jump if C==1 to PC + 2 + OFFSET
def test_BCS_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b00000001
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0xB0, 0x0F]) # branches forward
    assert cpu.P == 0b00000001
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_forward():
    cpu = CPU65816(None)
    cpu.P = 0b00000010
    cpu.PC = 0
    cpu.fetch_decode_execute([0xF0, 0x05])
    assert cpu.P == 0b00000010
    assert cpu.cycles == 3
    assert cpu.PC == 7 # 0 + 2 + 5


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_backward():
    cpu = CPU65816(None)
    cpu.P = 0b00000010
    cpu.PC = 10
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0xF0, 0xF9]) # -7
    assert cpu.P == 0b00000010
    assert cpu.cycles == 3
    assert cpu.PC == 5 # 10 + 2 - 7


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_no_branch():
    cpu = CPU65816(None)
    cpu.P = 0b0000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0xF0, 0x05])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 # 0 + 2


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_branch_page_boundary():
    cpu = CPU65816(None)
    cpu.e = 1
    cpu.P = 0b00110010
    cpu.PC = 253
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0xF0, 0x05]) # branches forward
    assert cpu.P == 0b00110010
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 # 253 + 2 + 5


# jump if Z==1 to PC + 2 + OFFSET
def test_BEQ_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b00000010
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0xF0, 0x0F]) # branches forward
    assert cpu.P == 0b00000010
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_forward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0xD0, 0x05])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 # 0 + 2 + 5


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_backward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 10
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0xD0, 0xF9]) # -7
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 # 10 + 2 - 7


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_no_branch():
    cpu = CPU65816(None)
    cpu.P = 0b0000010
    cpu.PC = 0
    cpu.fetch_decode_execute([0xD0, 0x05])
    assert cpu.P == 0b00000010
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 # 0 + 2


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_branch_page_boundary():
    cpu = CPU65816(None)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC = 253
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0xD0, 0x05]) # branches forward
    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 # 253 + 2 + 5


# jump if Z==0 to PC + 2 + OFFSET
def test_BNE_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0xD0, 0x0F]) # branches forward
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_forward():
    cpu = CPU65816(None)
    cpu.P = 0b10000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x30, 0x05])
    assert cpu.P == 0b10000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 # 0 + 2 + 5


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_backward():
    cpu = CPU65816(None)
    cpu.P = 0b10000000
    cpu.PC = 10
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x30, 0xF9]) # -7
    assert cpu.P == 0b10000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 # 10 + 2 - 7


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_no_branch():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x30, 0x05])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 # 0 + 2


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_branch_page_boundary():
    cpu = CPU65816(None)
    cpu.e = 1
    cpu.P = 0b10110000
    cpu.PC = 253
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x30, 0x05]) # branches forward
    assert cpu.P == 0b10110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 # 253 + 2 + 5


# jump if N==1 to PC + 2 + OFFSET
def test_BMI_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b10000000
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x30, 0x0F]) # branches forward
    assert cpu.P == 0b10000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_forward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x10, 0x05])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 # 0 + 2 + 5


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_backward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 10
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x10, 0xF9]) # -7
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 # 10 + 2 - 7


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_no_branch():
    cpu = CPU65816(None)
    cpu.P = 0b10000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x10, 0x05])
    assert cpu.P == 0b10000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 # 0 + 2


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_branch_page_boundary():
    cpu = CPU65816(None)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC = 253
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x10, 0x05]) # branches forward
    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 # 253 + 2 + 5


# jump if N==0 to PC + 2 + OFFSET
def test_BPL_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x10, 0x0F]) # branches forward
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_forward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x50, 0x05])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 # 0 + 2 + 5


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_backward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 10
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x50, 0xF9]) # -7
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 # 10 + 2 - 7


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_no_branch():
    cpu = CPU65816(None)
    cpu.P = 0b01000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x50, 0x05])
    assert cpu.P == 0b01000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 # 0 + 2


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_branch_page_boundary():
    cpu = CPU65816(None)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC = 253
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x50, 0x05]) # branches forward
    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 # 253 + 2 + 5


# jump if V==0 to PC + 2 + OFFSET
def test_BVC_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x50, 0x0F]) # branches forward
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_forward():
    cpu = CPU65816(None)
    cpu.P = 0b01000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x70, 0x05])
    assert cpu.P == 0b01000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 # 0 + 2 + 5


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_backward():
    cpu = CPU65816(None)
    cpu.P = 0b01000000
    cpu.PC = 10
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x70, 0xF9]) # -7
    assert cpu.P == 0b01000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 # 10 + 2 - 7


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_no_branch():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x70, 0x05])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 2 # no branch
    assert cpu.PC == 2 # 0 + 2


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_branch_page_boundary():
    cpu = CPU65816(None)
    cpu.e = 1
    cpu.P = 0b01110000
    cpu.PC = 253
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x70, 0x05]) # branches forward
    assert cpu.P == 0b01110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 # 253 + 2 + 5


# jump if V==1 to PC + 2 + OFFSET
def test_BVS_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b01000000
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x70, 0x0F]) # branches forward
    assert cpu.P == 0b01000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump to PC + 2 + OFFSET
def test_BRA_forward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x80, 0x05])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 7 # 0 + 2 + 5


# jump to PC + 2 + OFFSET
def test_BRA_backward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 10
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x80, 0xF9]) # -7
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert cpu.PC == 5 # 10 + 2 - 7


# jump to PC + 2 + OFFSET
def test_BRA_branch_page_boundary():
    cpu = CPU65816(None)
    cpu.e = 1
    cpu.P = 0b00110000
    cpu.PC = 253
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x80, 0x05]) # branches forward
    assert cpu.P == 0b00110000
    assert cpu.cycles == 4 # page boundary crossed in emulation mode
    assert cpu.PC == 260 # 253 + 2 + 5


# jump to PC + 2 + OFFSET
def test_BRA_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x80, 0x0F]) # branches forward
    assert cpu.P == 0b00000000
    assert cpu.cycles == 3
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16


# jump to PC + 3 + OFFSET
def test_BRL_forward():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0
    cpu.fetch_decode_execute([0x82, 0x05, 0x00])
    assert cpu.P == 0b00000000
    assert cpu.cycles == 4
    assert cpu.PC == 7 # 0 + 2 + 5


# jump to PC + 3 + OFFSET
def test_BRL_wrapped_execution():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.PC = 0xFFF0
    cpu.e = 0
    nops = [0xEA] * cpu.PC
    cpu.fetch_decode_execute(nops+[0x82, 0x0F, 0x00]) # branches forward
    assert cpu.P == 0b00000000
    assert cpu.cycles == 4
    assert (cpu.PC & 0xFFFF) == 1 # 65520 + 2 + 16