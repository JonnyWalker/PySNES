# Direct = Direct Page Register (DP/DPR)
class Mode(object): # Addressing modes
    IMPLIED = 0                             # obvious by instruction name
    IMMEDIATE_MEMORY_FLAG = 1
    IMMEDIATE_INDEX_FLAG = 2
    IMMEDIATE_8BIT = 3                      # XXX #const
    RELATIVE = 4                            # XXX nearlabel
    RELATIVE_LONG = 5                       # XXX label
    DIRECT = 6                              # XXX dp
    DIRECT_INDEXED_WITH_X = 7               # XXX addr, X
    DIRECT_INDEXED_WITH_Y = 8               # XXX addr, Y
    DIRECT_INDIRECT = 9                     # XXX (dp)
    DIRECT_INDEXED_INDIRECT_X = 10          # XXX (dp, X)
    DIRECT_INDIRECT_INDEXED_Y = 11          # XXX (dp), Y
    DIRECT_INDIRECT_LONG = 12               # XXX [dp]
    DIRECT_INDIRECT_INDEXED_LONG_Y = 13     # XXX [byte], Y
    ABSOLUTE = 14                           # XXX 2Bytes
    ABSOLUTE_INDEXED_WITH_X = 15            # XXX dp, X
    ABSOLUTE_INDEXED_WITH_Y = 16            # XXX dp, Y
    ABSOLUTE_LONG = 17                      # XXX 3Bytes
    ABSOLUTE_INDEXED_LONG_X = 18            # XXX long, X
    STACK_RELATIVE = 19                     # XXX sr, S
    STACK_RELATIVE_INDIRECT_INDEXED_Y = 20  # XXX (byte, s), Y
    ABSOLUTE_INDIRECT = 21
    ABSOLUTE_INDIRECT_LONG = 22
    ABSOLUTE_INDEXED_INDIRECT = 23
    IMPLIED_ACCUMULATOR = 24
    BLOCK_MOVE = 25
    IMMEDIATE_MINUS_X = 26
    IMMEDIATE_MINUS_M = 27

# The opcode map:
# HEX: (MNEMONIC, Mode, Flags(may be set afterwards), Byte-Num, Cycles, Doc )
# FLAGs NVMXDIZC (Negative, Overflow, A-Size, XY-Size, Decimal, IRQ Disable, Zero, Carry)
# Native Mode A-Size = 16 or 8 , X-Size/Y-Size = 16 or 8
# Emulation Mode A-Size = 8, X-Size = 8, Y-Size = 8
#
opcode_map = {
    0x61: ('ADC', Mode.DIRECT_INDEXED_INDIRECT_X,   0b11000011, 2, 6, 'Add With Carry'), # ADC (dp, X)
    0x63: ('ADC', Mode.STACK_RELATIVE,              0b11000011, 2, 4, 'Add With Carry'), # ADC sr, S
    0x65: ('ADC', Mode.DIRECT,                      0b11000011, 2, 3, 'Add With Carry'), # ADC dp
    0x67: ('ADC', Mode.DIRECT_INDIRECT_LONG,        0b11000011, 2, 6, 'Add With Carry'), # ADC [dp]
    0x69: ('ADC', Mode.IMMEDIATE_MINUS_M,           0b11000011, 3, 2, 'Add With Carry'), # ADC #const
    0x6D: ('ADC', Mode.ABSOLUTE,                    0b11000011, 3, 2, 'Add With Carry'), # ADC addr
    0x6F: ('ADC', Mode.ABSOLUTE_LONG,               0b11000011, 4, 5, 'Add With Carry'), # ADC long
    0x71: ('ADC', Mode.DIRECT_INDIRECT_INDEXED_Y,   0b11000011, 2, 5, 'Add With Carry'), # ADC (dp), Y
    0x72: ('ADC', Mode.DIRECT_INDIRECT,             0b11000011, 2, 5, 'Add With Carry'), # ADC (dp)
    0x73: ('ADC', Mode.STACK_RELATIVE_INDIRECT_INDEXED_Y,   0b11000011, 2, 7, 'Add With Carry'), # ADC (sr, S), Y
    0x75: ('ADC', Mode.DIRECT_INDEXED_WITH_X,       0b11000011, 2, 4, 'Add With Carry'), # ADC dp, X
    0x77: ('ADC', Mode.DIRECT_INDIRECT_INDEXED_LONG_Y,      0b11000011, 2, 6, 'Add With Carry'), # ADC [dp], Y
    0x79: ('ADC', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b11000011, 3, 4, 'Add With Carry'), # ADC addr, Y
    0x7D: ('ADC', Mode.ABSOLUTE_INDEXED_WITH_X,     0b11000011, 3, 4, 'Add With Carry'), # ADC addr, X
    0x7F: ('ADC', Mode.ABSOLUTE_INDEXED_LONG_X,     0b11000011, 4, 5, 'Add With Carry'), # ADC long, X

    0x21: ('AND', Mode.DIRECT_INDEXED_INDIRECT_X,   0b10000010, 2, 6, 'AND Accumulator With Memory'), # AND (dp, X)
    0x23: ('AND', Mode.STACK_RELATIVE,              0b10000010, 2, 4, 'AND Accumulator With Memory'), # AND sr, S
    0x25: ('AND', Mode.DIRECT,                      0b10000010, 2, 3, 'AND Accumulator With Memory'), # AND dp
    0x27: ('AND', Mode.DIRECT_INDIRECT_LONG,        0b10000010, 2, 6, 'AND Accumulator With Memory'), # AND [dp]
    0x29: ('AND', Mode.IMMEDIATE_MINUS_M,           0b10000010, 3, 2, 'AND Accumulator With Memory'), # AND #const
    0x2D: ('AND', Mode.ABSOLUTE,                    0b10000010, 3, 4, 'AND Accumulator With Memory'), # AND addr
    0x2F: ('AND', Mode.ABSOLUTE_LONG,               0b10000010, 4, 5, 'AND Accumulator With Memory'), # AND long
    0x31: ('AND', Mode.DIRECT_INDIRECT_INDEXED_Y,   0b10000010, 2, 5, 'AND Accumulator With Memory'), # AND (dp), Y
    0x32: ('AND', Mode.DIRECT_INDIRECT,             0b10000010, 2, 5, 'AND Accumulator With Memory'), # AND (dp)
    0x33: ('AND', Mode.STACK_RELATIVE_INDIRECT_INDEXED_Y,   0b10000010, 2, 7, 'AND Accumulator With Memory'), # AND (sr, S), Y
    0x35: ('AND', Mode.DIRECT_INDEXED_WITH_X,       0b10000010, 2, 4, 'AND Accumulator With Memory'), # AND dp, X
    0x37: ('AND', Mode.DIRECT_INDIRECT_INDEXED_LONG_Y,      0b10000010, 2, 6, 'AND Accumulator With Memory'), # AND [dp], Y
    0x39: ('AND', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b10000010, 3, 4, 'AND Accumulator With Memory'), # AND addr, Y
    0x3D: ('AND', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000010, 3, 4, 'AND Accumulator With Memory'), # AND addr, X
    0x3F: ('AND', Mode.ABSOLUTE_INDEXED_LONG_X,     0b10000010, 4, 5, 'AND Accumulator With Memory'), # AND long, X

    0x06: ('ASL', Mode.DIRECT,                      0b10000011, 2, 5, 'Arithmetic Shift Left'), # ASL dp
    0x0A: ('ASL', Mode.IMPLIED,                     0b10000011, 1, 2, 'Arithmetic Shift Left'), # ASL A
    0x0E: ('ASL', Mode.ABSOLUTE,                    0b10000011, 3, 6, 'Arithmetic Shift Left'), # ASL addr
    0x16: ('ASL', Mode.DIRECT_INDEXED_WITH_X,       0b10000011, 2, 6, 'Arithmetic Shift Left'), # ASL dp, X
    0x1E: ('ASL', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000011, 3, 7, 'Arithmetic Shift Left'), # ASL addr, X

    0x90: ('BCC', Mode.RELATIVE,                    0b00000000, 2, 2, 'Branch if Carry Clear'), # BCC nearlabel
    0xB0: ('BCS', Mode.RELATIVE,                    0b00000000, 2, 2, 'Branch if Carry Set'), # BCS neealabel
    0xF0: ('BEQ', Mode.RELATIVE,                    0b00000000, 2, 2, 'Branch if Equal'), # BEQ nearlabel

    0x24: ('BIT', Mode.DIRECT,                      0b11000010, 2, 3, 'Bit Test'), # BIT dp
    0x2C: ('BIT', Mode.ABSOLUTE,                    0b11000010, 3, 4, 'Bit Test'), # BIT addr
    0x34: ('BIT', Mode.DIRECT_INDEXED_WITH_X,       0b11000010, 2, 4, 'Bit Test'), # Bit dp, X
    0x3C: ('BIT', Mode.ABSOLUTE_INDEXED_WITH_X,     0b11000010, 3, 4, 'Bit Test'), # Bit addr, X
    0x89: ('BIT', Mode.IMMEDIATE_MINUS_M,           0b00000010, 3, 2, 'Bit Test'), # Bit #const

    0x30: ('BMI', Mode.RELATIVE,                    0b00000000, 2, 2, 'Branch if Minus'), # BMI nearlabel
    0xD0: ('BNE', Mode.RELATIVE,                    0b00000000, 2, 2, 'Branch if Not Eqaul'), # BNE nearlabel
    0x10: ('BPL', Mode.RELATIVE,                    0b00000000, 2, 2, 'Branch if Plus'), # BPL nearlabel
    0x80: ('BRA', Mode.RELATIVE,                    0b00000000, 2, 2, 'Branch Always'), # BRA nearlabel
    0x00: ('BRK', Mode.IMPLIED,                     0b00001100, 2, 7, 'Break'), # BRK
    0x82: ('BRL', Mode.RELATIVE_LONG,               0b00000000, 3, 4, 'Branch Long Always'), # BRL label
    0x50: ('BVC', Mode.RELATIVE,                    0b00000000, 2, 2, 'Branch if Overflow Clear'), # BVC nearlabel
    0x70: ('BVS', Mode.RELATIVE,                    0b00000000, 2, 2, 'Branch if Overflow Set'), # BVS nearlabel

    0x18: ('CLC', Mode.IMPLIED,                     0b00000001, 1, 2, 'Clear Carry'), # CLC
    0xD8: ('CLD', Mode.IMPLIED,                     0b00001000, 1, 2, 'Clear Decimal Mode Flag'), # CLD
    0x58: ('CLI', Mode.IMPLIED,                     0b00000100, 1, 2, 'Clear Interrupt Diable Flag'), # CLI
    0xB8: ('CLV', Mode.IMPLIED,                     0b01000000, 1, 2, 'Clear Overflow Flag'), # CLV

    0xC1: ('CMP', Mode.DIRECT_INDEXED_INDIRECT_X,   0b10000011, 2, 4, 'Compare Accumulator With Memory'), # CMP (dp, X)
    0xC3: ('CMP', Mode.STACK_RELATIVE,              0b10000011, 2, 4, 'Compare Accumulator With Meomry'), # CMP sr, S
    0xC5: ('CMP', Mode.DIRECT,                      0b10000011, 2, 3, 'Compare Accumulator With Meomry'), # CMP dp
    0xC7: ('CMP', Mode.DIRECT_INDIRECT_LONG,        0b10000011, 2, 6, 'Compare Accumulator With Meomry'), # CMP [dp]
    0xC9: ('CMP', Mode.IMMEDIATE_MINUS_M,           0b10000011, 3, 2, 'Compare Accumulator With Meomry'), # CMP #const
    0xCD: ('CMP', Mode.ABSOLUTE,                    0b10000011, 3, 4, 'Compare Accumulator With Meomry'), # CMP addr
    0xCF: ('CMP', Mode.ABSOLUTE_LONG,               0b10000011, 4, 5, 'Compare Accumulator With Meomry'), # CMP long
    0xD1: ('CMP', Mode.DIRECT_INDIRECT_INDEXED_Y,   0b10000011, 2, 5, 'Compare Accumulator With Meomry'), # CMP (dp), Y
    0xD2: ('CMP', Mode.DIRECT_INDIRECT,             0b10000011, 2, 5, 'Compare Accumulator With Meomry'), # CMP (dp)
    0xD3: ('CMP', Mode.STACK_RELATIVE_INDIRECT_INDEXED_Y,   0b10000011, 2, 7, 'Compare Accumulator With Meomry'), # CMP (sr, S), Y
    0xD5: ('CMP', Mode.DIRECT_INDEXED_WITH_X,       0b10000011, 2, 4, 'Compare Accumulator With Meomry'), # CMP dp, X
    0xD7: ('CMP', Mode.DIRECT_INDIRECT_INDEXED_LONG_Y,      0b10000011, 2, 6, 'Compare Accumulator With Meomry'), # CMP [dp], Y
    0xD9: ('CMP', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b10000011, 3, 4, 'Compare Accumulator With Meomry'), # CMP addr, Y
    0xDD: ('CMP', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000011, 3, 4, 'Compare Accumulator With Meomry'), # CMP addr, X
    0xDF: ('CMP', Mode.ABSOLUTE_INDEXED_LONG_X,     0b10000011, 2, 7, 'Compare Accumulator With Meomry'), # CMP long, X

    0x02: ('COP', Mode.IMPLIED,                     0b00001100, 2, 7, 'Co-Processor Enable'), # COP #const

    0xE0: ('CPX', Mode.IMMEDIATE_MINUS_X,           0b10000011, 3, 2, 'Compare Index Register X With Memory'), # CPX #const
    0xE4: ('CPX', Mode.DIRECT,                      0b10000011, 2, 3, 'Compare Index Register X With Memory'), # CPX dp
    0xEC: ('CPX', Mode.ABSOLUTE,                    0b10000011, 3, 4, 'Compare Index Register X With Memory'), # CPX addr
    0xC0: ('CPY', Mode.IMMEDIATE_MINUS_X,           0b10000011, 3, 2, 'Compare Index Register Y With Memory'), # CPY #const
    0xC4: ('CPY', Mode.DIRECT,                      0b10000011, 2, 3, 'Compare Index Register Y With Memory'), # CPY dp
    0xCC: ('CPY', Mode.ABSOLUTE,                    0b10000011, 3, 4, 'Compare Index Register Y With Memory'), # CPY addr

    0x3A: ('DEC', Mode.IMPLIED,                     0b10000010, 1, 2, 'Decrecment'), # DEC A
    0xC6: ('DEC', Mode.DIRECT,                      0b10000010, 2, 5, 'Decrecment'), # DEC dp
    0xCE: ('DEC', Mode.ABSOLUTE,                    0b10000010, 3, 6, 'Decrecment'), # DEC addr
    0xD6: ('DEC', Mode.DIRECT_INDEXED_WITH_X,       0b10000010, 2, 6, 'Decrecment'), # DEC dp, X
    0xDE: ('DEC', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000010, 3, 7, 'Decrecment'), # DEC addr, X
    0xCA: ('DEX', Mode.IMPLIED,                     0b10000010, 1, 2, 'Decrecment'), # DEX
    0x88: ('DEY', Mode.IMPLIED,                     0b10000010, 1, 2, 'Decrecment'), # DEY

    0x41: ('EOR', Mode.DIRECT_INDEXED_INDIRECT_X,   0b10000010, 2, 6, 'XOR Accumulator With Memory'), # EOR (dp, X)
    0x43: ('EOR', Mode.STACK_RELATIVE,              0b10000010, 2, 4, 'XOR Accumulator With Memory'), # EOR sr, S
    0x45: ('EOR', Mode.DIRECT,                      0b10000010, 2, 3, 'XOR Accumulator With Memory'), # EOR dp
    0x47: ('EOR', Mode.DIRECT_INDIRECT_LONG,        0b10000010, 2, 6, 'XOR Accumulator With Memory'), # EOR [dp]
    0x49: ('EOR', Mode.IMMEDIATE_MINUS_M,           0b10000010, 3, 2, 'XOR Accumulator With Memory'), # EOR #const
    0x4D: ('EOR', Mode.ABSOLUTE,                    0b10000010, 3, 4, 'XOR Accumulator With Memory'), # EOR addr
    0x4F: ('EOR', Mode.ABSOLUTE_LONG,               0b10000010, 4, 5, 'XOR Accumulator With Memory'), # EOR long
    0x51: ('EOR', Mode.DIRECT_INDIRECT_INDEXED_Y,   0b10000010, 2, 5, 'XOR Accumulator With Memory'), # EOR (dp), Y
    0x52: ('EOR', Mode.DIRECT_INDIRECT,             0b10000010, 2, 5, 'XOR Accumulator With Memory'), # EOR (dp)
    0x53: ('EOR', Mode.STACK_RELATIVE_INDIRECT_INDEXED_Y,   0b10000010, 2, 7, 'XOR Accumulator With Memory'), # EOR (sr, S), Y
    0x55: ('EOR', Mode.DIRECT_INDEXED_WITH_X,       0b10000010, 2, 4, 'XOR Accumulator With Memory'), # EOR dp, X
    0x57: ('EOR', Mode.DIRECT_INDIRECT_INDEXED_LONG_Y,      0b10000010, 2, 6, 'XOR Accumulator With Memory'), # EOR [dp], Y
    0x59: ('EOR', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b10000010, 3, 4, 'XOR Accumulator With Memory'), # EOR addr, Y
    0x5D: ('EOR', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000010, 3, 4, 'XOR Accumulator With Memory'), # EOR addr, X
    0x5F: ('EOR', Mode.ABSOLUTE_INDEXED_LONG_X,     0b10000010, 4, 5, 'XOR Accumulator With Memory'), # EOR long, X

    0x1A: ('INC', Mode.IMPLIED,                     0b10000010, 1, 2, 'Increcment'),  # INC A
    0xE6: ('INC', Mode.DIRECT,                      0b10000010, 2, 5, 'Increcment'),  # INC dp
    0xEE: ('INC', Mode.ABSOLUTE,                    0b10000010, 3, 6, 'Increcment'),  # INC addr
    0xF6: ('INC', Mode.DIRECT_INDEXED_WITH_X,       0b10000010, 2, 6, 'Increcment'),  # INC dp, X
    0xFE: ('INC', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000010, 3, 7, 'Increcment'),  # INC addr, X
    0xE8: ('INC', Mode.IMPLIED,                     0b10000010, 1, 2, 'Increcment'),  # INX
    0xC8: ('INC', Mode.IMPLIED,                     0b10000010, 1, 2, 'Increcment'),  # INY

    0x4C: ('JMP', Mode.ABSOLUTE,                    0b00000000, 3, 3, 'Jump'), # JMP addr
    0x5C: ('JMP', Mode.ABSOLUTE_LONG,               0b00000000, 4, 4, 'Jump'), # JMP long
    0x6C: ('JMP', Mode.ABSOLUTE_INDIRECT,           0b00000000, 3, 5, 'Jump'), # JMP (addr)
    0x7C: ('JMP', Mode.ABSOLUTE_INDEXED_INDIRECT,   0b00000000, 3, 6, 'Jump'), # JMP (addr, X)
    0xDC: ('JMP', Mode.ABSOLUTE_INDIRECT_LONG,      0b00000000, 3, 6, 'Jump'), # JMP [addr]
    0x20: ('JSR', Mode.ABSOLUTE,                    0b00000000, 3, 6, 'Jump to Subroutine'), # JSR addr
    0x22: ('JSL', Mode.ABSOLUTE_LONG,               0b00000000, 4, 8, 'Jump to Subroutine'), # JSR long
    0xFC: ('JSR', Mode.ABSOLUTE_INDEXED_INDIRECT,   0b00000000, 3, 8, 'Jump to Subroutine'), # JSR (addr, X)

    0xA1: ('LDA', Mode.DIRECT_INDEXED_INDIRECT_X,   0b10000010, 2, 6, 'Load Accumulator With Memory'),  # LDA (dp, X)
    0xA3: ('LDA', Mode.STACK_RELATIVE,              0b10000010, 2, 4, 'Load Accumulator With Memory'),  # LDA sr, S
    0xA5: ('LDA', Mode.DIRECT,                      0b10000010, 2, 3, 'Load Accumulator With Memory'),  # LDA dp
    0xA7: ('LDA', Mode.DIRECT_INDIRECT_LONG,        0b10000010, 2, 6, 'Load Accumulator With Memory'),  # LDA [dp]
    0xA9: ('LDA', Mode.IMMEDIATE_MINUS_M,           0b10000010, 3, 2, 'Load Accumulator With Memory'),  # LDA #const
    0xAD: ('LDA', Mode.ABSOLUTE,                    0b10000010, 3, 4, 'Load Accumulator With Memory'),  # LDA addr
    0xAF: ('LDA', Mode.ABSOLUTE_LONG,               0b10000010, 4, 5, 'Load Accumulator With Memory'),  # LDA long
    0xB1: ('LDA', Mode.DIRECT_INDIRECT_INDEXED_Y,   0b10000010, 2, 5, 'Load Accumulator With Memory'),  # LDA (dp), Y
    0xB2: ('LDA', Mode.DIRECT_INDIRECT,             0b10000010, 2, 5, 'Load Accumulator With Memory'),  # LDA (dp)
    0xB3: ('LDA', Mode.STACK_RELATIVE_INDIRECT_INDEXED_Y,   0b10000010, 2, 7, 'Load Accumulator With Memory'), # LDA (sr, S), Y
    0xB5: ('LDA', Mode.DIRECT_INDEXED_WITH_X,       0b10000010, 2, 4, 'Load Accumulator With Memory'),  # LDA dp, X
    0xB7: ('LDA', Mode.DIRECT_INDIRECT_INDEXED_LONG_Y,      0b10000010, 2, 6, 'Load Accumulator With Memory'),  # LDA [dp], Y
    0xB9: ('LDA', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b10000010, 3, 4, 'Load Accumulator With Memory'),  # LDA addr, Y
    0xBD: ('LDA', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000010, 3, 4, 'Load Accumulator With Memory'),  # LDA addr, X
    0xBF: ('LDA', Mode.ABSOLUTE_INDEXED_LONG_X,     0b10000010, 4, 5, 'Load Accumulator With Memory'),  # LDA long, X
    0xA2: ('LDX', Mode.IMMEDIATE_MINUS_X,           0b10000010, 3, 2, 'Load Index Register X from Memory'), # LDX # const
    0xA6: ('LDX', Mode.DIRECT,                      0b10000010, 2, 3, 'Load Index Register X from Memory'), # LDX dp
    0xAE: ('LDX', Mode.ABSOLUTE,                    0b10000010, 3, 4, 'Load Index Register X from Memory'), # LDX addr
    0xB6: ('LDX', Mode.DIRECT_INDEXED_WITH_Y,       0b10000010, 2, 4, 'Load Index Register X from Memory'), # LDX dp, Y
    0xBE: ('LDX', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b10000010, 3, 4, 'Load Index Register X from Memory'), # LDX addr, Y
    0xA0: ('LDY', Mode.IMMEDIATE_MINUS_X,           0b10000010, 3, 2, 'Load Index Register Y from Memory'),  # LDY # const
    0xA4: ('LDY', Mode.DIRECT,                      0b10000010, 2, 3, 'Load Index Register Y from Memory'),  # LDY dp
    0xAC: ('LDY', Mode.ABSOLUTE,                    0b10000010, 3, 4, 'Load Index Register Y from Memory'),  # LDY addr
    0xB4: ('LDY', Mode.DIRECT_INDEXED_WITH_X,       0b10000010, 2, 4, 'Load Index Register Y from Memory'),  # LDY dp, Y
    0xBC: ('LDY', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000010, 3, 4, 'Load Index Register Y from Memory'),  # LDY addr, Y

    0x46: ('LSR', Mode.DIRECT,                      0b10000011, 2, 5, 'Logical Shift Right'), # LSR dp
    0x4A: ('LSR', Mode.IMPLIED,                     0b10000011, 1, 2, 'Logical Shift Right'), # LSR A
    0x4E: ('LSR', Mode.ABSOLUTE,                    0b10000011, 3, 6, 'Logical Shift Right'), # LSR addr
    0x56: ('LSR', Mode.DIRECT_INDEXED_WITH_X,       0b10000011, 2, 6, 'Logical Shift Right'), # LSR dp, X
    0x5E: ('LSR', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000011, 3, 7, 'Logical Shift Right'), # LSR addr, X

    0x54: ('MVN', Mode.BLOCK_MOVE,                  0b00000000, 3, 1, 'Block Move Negative'), # MVN srcbk, destbk
    0x44: ('MVP', Mode.BLOCK_MOVE,                  0b00000000, 3, 1, 'Block Move Positive'), # MVP srcbk, destbk

    0xEA: ('NOP', Mode.IMPLIED,                     0b00000000, 1, 2, 'No Operation'), # NOP

    0x01: ('ORA', Mode.DIRECT_INDEXED_INDIRECT_X,   0b10000010, 2, 6, 'OR Accumulator With Memory'),  # ORA (dp, X)
    0x03: ('ORA', Mode.STACK_RELATIVE,              0b10000010, 2, 4, 'OR Accumulator With Memory'),  # ORA sr, S
    0x05: ('ORA', Mode.DIRECT,                      0b10000010, 2, 3, 'OR Accumulator With Memory'),  # ORA dp
    0x07: ('ORA', Mode.DIRECT_INDIRECT_LONG,        0b10000010, 2, 6, 'OR Accumulator With Memory'),  # ORA [dp]
    0x09: ('ORA', Mode.IMMEDIATE_MINUS_M,           0b10000010, 3, 2, 'OR Accumulator With Memory'),  # ORA #const
    0x0D: ('ORA', Mode.ABSOLUTE,                    0b10000010, 3, 4, 'OR Accumulator With Memory'),  # ORA addr
    0x0F: ('ORA', Mode.ABSOLUTE_LONG,               0b10000010, 4, 5, 'OR Accumulator With Memory'),  # ORA long
    0x11: ('ORA', Mode.DIRECT_INDIRECT_INDEXED_Y,   0b10000010, 2, 5, 'OR Accumulator With Memory'),  # ORA (dp), Y
    0x12: ('ORA', Mode.DIRECT_INDIRECT,             0b10000010, 2, 5, 'OR Accumulator With Memory'),  # ORA (dp)
    0x13: ('ORA', Mode.STACK_RELATIVE_INDIRECT_INDEXED_Y,   0b10000010, 2, 7, 'OR Accumulator With Memory'),# ORA (sr, S), Y
    0x15: ('ORA', Mode.DIRECT_INDEXED_WITH_X,       0b10000010, 2, 4, 'OR Accumulator With Memory'),  # ORA dp, X
    0x17: ('ORA', Mode.DIRECT_INDIRECT_INDEXED_LONG_Y,      0b10000010, 2, 6, 'OR Accumulator With Memory'),  # ORA [dp], Y
    0x19: ('ORA', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b10000010, 3, 4, 'OR Accumulator With Memory'),  # ORA addr, Y
    0x1D: ('ORA', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000010, 3, 4, 'OR Accumulator With Memory'),  # ORA addr, X
    0x1F: ('ORA', Mode.ABSOLUTE_INDEXED_LONG_X,     0b10000010, 4, 5, 'OR Accumulator With Memory'),  # ORA long, X

    0x48: ('PHA', Mode.IMPLIED,                     0b00000000, 1, 3, 'Push Accumulator'), # PHA
    0x8B: ('PHB', Mode.IMPLIED,                     0b00000000, 1, 3, 'Push Data Bank Register'), # PHB
    0x0B: ('PHD', Mode.IMPLIED,                     0b00000000, 1, 4, 'Push Direct Page Register'), # PHD
    0x4B: ('PHK', Mode.IMPLIED,                     0b00000000, 1, 3, 'Push Program Bank Register'), # PHK
    0x08: ('PHP', Mode.IMPLIED,                     0b00000000, 1, 3, 'Push Processor Status Register'), # PHP
    0xDA: ('PHX', Mode.IMPLIED,                     0b00000000, 1, 3, 'Push Index Register X'), # PHX
    0x5A: ('PHY', Mode.IMPLIED,                     0b00000000, 1, 3, 'Push Index Register Y'), # PHY

    0x68: ('PLA', Mode.IMPLIED,                     0b00000000, 1, 4, 'Pull Accumulator'), # PLA
    0xAB: ('PLB', Mode.IMPLIED,                     0b00000000, 1, 4, 'Pull Data Bank Register'), # PLB
    0x2B: ('PLD', Mode.IMPLIED,                     0b00000000, 1, 5, 'Pull Direct Page Register'), # PLD
    0x28: ('PLP', Mode.IMPLIED,                     0b00000000, 1, 4, 'Pull Processor Status Register'), # PLP
    0xFA: ('PLX', Mode.IMPLIED,                     0b00000000, 1, 4, 'Pull Index Register X'), # PLX
    0x7A: ('PLY', Mode.IMPLIED,                     0b00000000, 1, 4, 'Pull Index Register Y'), # PLY

    0xC2: ('REP', Mode.IMMEDIATE_8BIT,              0b11111111, 2, 3, 'Reset Processor Status Bits'), # REP # const

    0x26: ('ROL', Mode.DIRECT,                      0b10000011, 2, 5, 'Rotate Left'), # ROL dp
    0x2A: ('ROL', Mode.IMPLIED,                     0b10000011, 1, 2, 'Rotate Left'), # ROL A
    0x2E: ('ROL', Mode.ABSOLUTE,                    0b10000011, 3, 6, 'Rotate Left'), # ROL addr
    0x36: ('ROL', Mode.DIRECT_INDEXED_WITH_X,       0b10000011, 2, 6, 'Rotate Left'), # ROL dp, X
    0x3E: ('ROL', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000011, 3, 7, 'Rotate Left'), # ROL addr, X

    0x66: ('ROR', Mode.DIRECT,                      0b10000011, 2, 5, 'Rotate Right'),  # ROR dp
    0x6A: ('ROR', Mode.IMPLIED,                     0b10000011, 1, 2, 'Rotate Right'),  # ROR A
    0x6E: ('ROR', Mode.ABSOLUTE,                    0b10000011, 3, 6, 'Rotate Right'),  # ROR addr
    0x76: ('ROR', Mode.DIRECT_INDEXED_WITH_X,       0b10000011, 2, 6, 'Rotate Right'),  # ROR dp, X
    0x7E: ('ROR', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000011, 3, 7, 'Rotate Right'),  # ROR addr, X

    0x40: ('RTI', Mode.IMPLIED,                     0b11111111, 1, 6, 'Return From Interrupt'), # RTI
    0x6B: ('RTL', Mode.IMPLIED,                     0b00000000, 1, 6, 'Return From Subroutine Long'), # RTL
    0x60: ('RTS', Mode.IMPLIED,                     0b00000000, 1, 6, 'Retrun From Subroutine'), # RTS

    0xE1: ('SBC', Mode.DIRECT_INDEXED_INDIRECT_X,   0b11000010, 2, 6, 'Subtract With Borrow From Accumulator'),  # SBC (dp, X)
    0xE3: ('SBC', Mode.STACK_RELATIVE,              0b11000010, 2, 4, 'Subtract With Borrow From Accumulator'),  # SBC sr, S
    0xE5: ('SBC', Mode.DIRECT,                      0b11000010, 2, 3, 'Subtract With Borrow From Accumulator'),  # SBC dp
    0xE7: ('SBC', Mode.DIRECT_INDIRECT_LONG,        0b11000010, 2, 6, 'Subtract With Borrow From Accumulator'),  # SBC [dp]
    0xE9: ('SBC', Mode.IMMEDIATE_MINUS_M,           0b11000010, 3, 2, 'Subtract With Borrow From Accumulator'),  # SBC #const
    0xED: ('SBC', Mode.ABSOLUTE,                    0b11000010, 3, 4, 'Subtract With Borrow From Accumulator'),  # SBC addr
    0xEF: ('SBC', Mode.ABSOLUTE_LONG,               0b11000010, 4, 5, 'Subtract With Borrow From Accumulator'),  # SBC long
    0xF1: ('SBC', Mode.DIRECT_INDIRECT_INDEXED_Y,   0b11000010, 2, 5, 'Subtract With Borrow From Accumulator'),  # SBC (dp), Y
    0xF2: ('SBC', Mode.DIRECT_INDIRECT,             0b11000010, 2, 5, 'Subtract With Borrow From Accumulator'),  # SBC (dp)
    0xF3: ('SBC', Mode.STACK_RELATIVE_INDIRECT_INDEXED_Y,   0b11000010, 2, 7, 'Subtract With Borrow From Accumulator'), # SBC (sr, S), Y
    0xF5: ('SBC', Mode.DIRECT_INDEXED_WITH_X,       0b11000010, 2, 4, 'Subtract With Borrow From Accumulator'),  # SBC dp, X
    0xF7: ('SBC', Mode.DIRECT_INDIRECT_INDEXED_LONG_Y,      0b11000010, 2, 6, 'Subtract With Borrow From Accumulator'),  # SBC [dp], Y
    0xF9: ('SBC', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b11000010, 3, 4, 'Subtract With Borrow From Accumulator'),  # SBC addr, Y
    0xFD: ('SBC', Mode.ABSOLUTE_INDEXED_WITH_X,     0b11000010, 3, 4, 'Subtract With Borrow From Accumulator'),  # SBC addr, X
    0xFF: ('SBC', Mode.ABSOLUTE_INDEXED_LONG_X,     0b11000010, 4, 5, 'Subtract With Borrow From Accumulator'),  # SBC long, X

    0x38: ('SEC', Mode.IMPLIED,                     0b00000001, 1, 2, 'Set Carry Flag'), # SEC
    0xF8: ('SED', Mode.IMPLIED,                     0b00001000, 1, 2, 'Set Decimal Flag'), # SED
    0x78: ('SEI', Mode.IMPLIED,                     0b00000100, 1, 2, 'Set Interrupt Disable Flag'), # SEI
    0xE2: ('SEP', Mode.IMMEDIATE_8BIT,              0b11111111, 2, 3, 'Reset Processor Status Bits'), # SEP # const

    0x81: ('STA', Mode.DIRECT_INDEXED_INDIRECT_X,   0b00000000, 2, 6, 'Store Accumulator To Memory'),# STA (dp, X)
    0x83: ('STA', Mode.STACK_RELATIVE,              0b00000000, 2, 4, 'Store Accumulator To Memory'),  # STA sr, S
    0x85: ('STA', Mode.DIRECT,                      0b00000000, 2, 3, 'Store Accumulator To Memory'),  # STA dp
    0x87: ('STA', Mode.DIRECT_INDIRECT_LONG,        0b00000000, 2, 6, 'Store Accumulator To Memory'),  # STA [dp]
    0x8D: ('STA', Mode.ABSOLUTE,                    0b00000000, 3, 4, 'Store Accumulator To Memory'),  # STA addr
    0x8F: ('STA', Mode.ABSOLUTE_LONG,               0b00000000, 4, 5, 'Store Accumulator To Memory'),  # STA long
    0x91: ('STA', Mode.DIRECT_INDIRECT_INDEXED_Y,   0b00000000, 2, 6, 'Store Accumulator To Memory'), # STA (dp), Y
    0x92: ('STA', Mode.DIRECT_INDIRECT,             0b00000000, 2, 5, 'Store Accumulator To Memory'),  # STA (dp)
    0x93: ('STA', Mode.STACK_RELATIVE_INDIRECT_INDEXED_Y,   0b00000000, 2, 7, 'Store Accumulator To Memory'), # STA (sr, S), Y
    0x95: ('STA', Mode.DIRECT_INDEXED_WITH_X,       0b00000000, 2, 4, 'Store Accumulator To Memory'), # STA dp, X
    0x97: ('STA', Mode.DIRECT_INDIRECT_INDEXED_LONG_Y,      0b00000000, 2, 6, 'Store Accumulator To Memory'), # STA [dp], Y
    0x99: ('STA', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b00000000, 3, 5, 'Store Accumulator To Memory'), # STA addr, Y
    0x9D: ('STA', Mode.ABSOLUTE_INDEXED_WITH_X,     0b00000000, 3, 5, 'Store Accumulator To Memory'), # STA addr, X
    0x9F: ('STA', Mode.ABSOLUTE_INDEXED_LONG_X,     0b00000000, 4, 5, 'Store Accumulator To Memory'), # STA long, X

    0xDB: ('STP', Mode.IMPLIED,                     0b00000000, 1, 3, 'Stop Processor'), # STP

    0x86: ('STX', Mode.DIRECT,                      0b00000000, 2, 3, 'Store Index Register X to Memorry'), # STX dp
    0x8E: ('STX', Mode.ABSOLUTE,                    0b00000000, 3, 4, 'Store Index Register X to Memorry'), # STX addr
    0x96: ('STX', Mode.DIRECT_INDEXED_WITH_Y,       0b00000000, 2, 4, 'Store Index Register X to Memorry'), # STX dp, Y
    0x84: ('STY', Mode.DIRECT,                      0b00000000, 2, 3, 'Store Index Register Y to Memorry'), # STY dp
    0x8C: ('STY', Mode.ABSOLUTE,                    0b00000000, 3, 4, 'Store Index Register Y to Memorry'), # STY addr
    0x94: ('STY', Mode.DIRECT_INDEXED_WITH_X,       0b00000000, 2, 4, 'Store Index Register Y to Memorry'), # STY dp, X

    0x64: ('STZ', Mode.DIRECT,                      0b00000000, 2, 3, 'Store Zero to Memory'), # STZ dp
    0x74: ('STZ', Mode.DIRECT_INDEXED_WITH_X,       0b00000000, 2, 4, 'Store Zero to Memory'), # STZ dp, X
    0x9C: ('STZ', Mode.ABSOLUTE,                    0b00000000, 3, 4, 'Store Zero to Memory'), # STZ addr
    0x9E: ('STZ', Mode.ABSOLUTE_INDEXED_WITH_X,     0b00000000, 3, 5, 'Store Zero to Memory'), # STZ addr, X

    0xAA: ('TAX', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer Accumulator To Index Register X'), # TAX
    0xA8: ('TAY', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer Accumulator To Index Register Y'), # TAY
    0x5B: ('TCD', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer 16-bit Accumulator to Direct Page Register'), # TCD
    0x1B: ('TCS', Mode.IMPLIED,                     0b00000000, 1, 2, 'Transfer 16-bit Accumulator to Stack Pointer'), # TCS
    0x7B: ('TDC', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer Direct Page Register to 16-bit Accumulator'), # TDC

    0x14: ('TRB', Mode.DIRECT,                      0b00000010, 2, 5, 'Test and Reset Memory Bits Against Accumulator'), # TRB dp
    0x1C: ('TRB', Mode.ABSOLUTE,                    0b00000010, 3, 6, 'Test and Reset Memory Bits Against Accumulator'), # TRB addr
    0x04: ('TSB', Mode.DIRECT,                      0b00000010, 2, 5, 'Test and Set Memory Bits Against Accumulator'), # TSB ap
    0x0C: ('TSB', Mode.ABSOLUTE,                    0b00000010, 3, 6, 'Test and Set Memory Bits Against Accumulator'), # TSB addr

    0x3B: ('TSC', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer Stack Pointer to 16-bit Accumulator'), # TSC
    0xBA: ('TSX', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer Stack Pointer to Index Register X'), # TSX
    0x8A: ('TXA', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer Index Register X to Accumulator'), # TXA
    0x9A: ('TXS', Mode.IMPLIED,                     0b00000000, 1, 2, 'Transfer Index Register X to Stack Pointer'), # TXS
    0x9B: ('TXY', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer Index Register X to Index Register Y'), # TXY
    0x98: ('TYA', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer Index Register Y to Accumulator'), # TYA
    0xBB: ('TYX', Mode.IMPLIED,                     0b10000010, 1, 2, 'Transfer Index Register Y to Index Register X'), # TYX

    0xCB: ('WAI', Mode.IMPLIED,                     0b00000000, 1, 3, 'Wait for Interrupt'), # WAI
    0x42: ('WDM', Mode.IMPLIED,                     0b00000000, 2, 0, 'Reserved for Future Expansion'), # WDM

    0xEB: ('XBA', Mode.IMPLIED,                     0b10000010, 1, 3, 'Exchange B and A 8-bit Accumulators'), # XBA
    0xFB: ('XCE', Mode.IMPLIED,                     0b00110011, 1, 2, 'Exchange Carry and Emulation Flags') # XCE
}