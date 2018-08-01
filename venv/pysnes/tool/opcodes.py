# Direct = Direct Page Register (DP/DPR)
class Mode(object): # Addressing modes
    IMPLIED = 0                             # obvious by instruction name
    IMMEDIATE_MEMORY_FLAG = 1
    IMMEDIATE_INDEX_FLAG = 2
    IMMEDIATE_8BIT = 3                      # 0x09: XXX #const
    RELATIVE = 4
    RELATIVE_LONG = 5
    DIRECT = 6                              # 0x01: XXX dp
    DIRECT_INDEXED_WITH_X = 7               # 0x15: XXX addr, X
    DIRECT_INDEXED_WITH_Y = 8               # XXX addr, Y
    DIRECT_INDIRECT = 9                     # 0x12: XXX (dp)
    DIRECT_INDEXED_INDIRECT_X = 10          # 0x01: XXX (dp, X)
    DIRECT_INDIRECT_INDEXED_Y = 11          # 0x11: XXX (dp), Y
    DIRECT_INDIRECT_LONG = 12               # 0x07: XXX [dp]
    DIRECT_INDIRECT_INDEXED_LONG_Y = 13     # 0x17: XXX [byte], Y
    ABSOLUTE = 14                           # 0x0D: XXX 2Bytes
    ABSOLUTE_INDEXED_WITH_X = 15            # 0x1D: XXX dp, X
    ABSOLUTE_INDEXED_WITH_Y = 16            # 0x19: XXX dp, Y
    ABSOLUTE_LONG = 17                      # 0x0F: XXX 3Bytes
    ABSOLUTE_INDEXED_LONG_X = 18            # 0x1F: XXX long, X
    STACK_RELATIVE = 19                     # 0x03: XXX sr, S
    STACK_RELATIVE_INDIRECT_INDEXED_Y = 20  # 0x13: XXX (byte, s), Y
    ABSOLUTE_INDIRECT = 21
    ABSOLUTE_INDIRECT_LONG = 22
    ABSOLUTE_INDEXED_INDIRECT = 23
    IMPLIED_ACCUMULATOR = 24
    BLOCK_MOVE = 25

# The opcode map:
# HEX: (MNEMONIC, Mode, Flags, Byte-Num, Cycles, Doc )
# FLAGs NVMXDIZC (Negative, Overflow, A-Size, XY-Size, Decimal, IRQ Disable, Zero, Carry)
# Native Mode A-Size = 16, X-Size = 16, Y-Size = 16
# Emulation Mode A-Size = 8, X-Size = 8, Y-Size = 8
#
opcode_map = {
    0x61: ("ADC", Mode.DIRECT_INDEXED_INDIRECT_X,   0b11000011, 2, 6, 'Add With Carry'), # ADC (dp, X)
    0x63: ("ADC", Mode.STACK_RELATIVE,              0b11000011, 2, 4, 'Add With Carry'), # ADC sr, S
    0x65: ("ADC", Mode.DIRECT,                      0b11000011, 2, 3, 'Add With Carry'), # ADC dp
    0x67: ("ADC", Mode.DIRECT_INDIRECT_LONG,        0b11000011, 2, 6, 'Add With Carry'), # ADC [dp]
    0x69: ('ADC', Mode.IMMEDIATE_8BIT,              0b11000011, 2, 2, 'Add With Carry'), # ADC #const
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
    0x29: ('AND', Mode.IMMEDIATE_8BIT,              0b10000010, 2, 2, 'AND Accumulator With Memory'), # AND #const
    0x2D: ('AND', Mode.ABSOLUTE,                    0b10000010, 3, 4, 'AND Accumulator With Memory'), # AND addr
    0x2F: ('AND', Mode.ABSOLUTE_LONG,               0b10000010, 4, 5, 'AND Accumulator With Memory'), # AND long
    0x31: ('AND', Mode.DIRECT_INDIRECT_INDEXED_Y,   0b10000010, 2, 5, 'AND Accumulator With Memory'), # AND (dp), Y
    0x32: ('AND', Mode.DIRECT_INDIRECT,             0b10000010, 2, 5, 'AND Accumulator With Memory'), # AND (dp)
    0x33: ('AND', Mode.STACK_RELATIVE_INDIRECT_INDEXED_Y,   0b10000010, 2, 7, 'AND Accumulator With Memory'), # AND (sr, S), Y
    0x35: ('AND', Mode.DIRECT_INDEXED_INDIRECT_X,   0b10000010, 2, 4, 'AND Accumulator With Memory'), # AND dp, X
    0x37: ('AND', Mode.DIRECT_INDIRECT_INDEXED_LONG_Y,      0b10000010, 2, 6, 'AND Accumulator With Memory'), # AND [dp], Y
    0x39: ('AND', Mode.ABSOLUTE_INDEXED_WITH_Y,     0b10000010, 3, 4, 'AND Accumulator With Memory'), # AND addr, Y
    0x3D: ('AND', Mode.ABSOLUTE_INDEXED_WITH_X,     0b10000010, 3, 4, 'AND Accumulator With Memory'), # AND addr, X
    0x3F: ('AND', Mode.ABSOLUTE_INDEXED_LONG_X,     0b10000010, 4, 5, 'AND Accumulator With Memory'), # AND long, X

    0x18: ("CLC", Mode.IMPLIED,                     0b00000001, 1, 2, 'Clear Carry'),
    0xA9: ("LDA", Mode.IMMEDIATE_8BIT,              0b10000010, 2, 2, 'Load Accumulator from Memory'),
    0x48: ("PHA", Mode.IMPLIED,                     0b00000000, 1, 3, 'Push Accumulator'),
    0xC2: ("REP", Mode.IMMEDIATE_8BIT,              0b11111111, 2, 3, 'Reset Processor Status Bits'),
    0x78: ("SEI", Mode.IMPLIED,                     0b00000100, 1, 2, 'Set Interrupt Disable Flag'),
    0xE2: ("SEP", Mode.IMMEDIATE_8BIT,              0b11111111, 2, 3, 'Reset Processor Status Bits'),
    0x8D: ("STA", Mode.ABSOLUTE,                    0b00000000, 3, 4, 'Store Accumulator to Memory'),
    0x9C: ("STZ", Mode.ABSOLUTE,                    0b00000000, 3, 4, 'Store Zero to Memory'),
    0xEB: ("XBA", Mode.IMPLIED,                     0b10000010, 1, 3, 'Exchange B and A 8-bit Accumulators'),
    0xFB: ("XCE", Mode.IMPLIED,                     0b00110011, 1, 2, 'Exchange Carry and Emulation Flags')
}