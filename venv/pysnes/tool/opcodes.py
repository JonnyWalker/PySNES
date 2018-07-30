class Mode(object): # Addressing modes
    IMPLIED = 0
    IMMEDIATE_MEMORY_FLAG = 1
    IMMEDIATE_INDEX_FLAG = 2
    IMMEDIATE_8BIT = 3
    RELATIVE = 4
    RELATIVE_LONG = 5
    DIRECT = 6
    DIRECT_INDEXED_WITH_X = 7
    DIRECT_INDEXED_WITH_Y = 8
    DIRECT_INDIRECT = 9
    DIRECT_INDEXED_INDIRECT = 10
    DIRECT_INDIRECT_INDEXED = 11
    DIRECT_INDIRECT_LONG = 12
    DIRECT_INDIRECT_INDEXED_LONG = 13
    ABSOLUTE = 14
    ABSOLUTE_INDEXED_WITH_X = 15
    ABSOLUTE_INDEXED_WITH_Y = 16
    ABSOLUTE_LONG = 17
    ABSOLUTE_INDEXED_LONG = 18
    STACK_RELATIVE = 19
    STACK_RELATIVE_INDIRECT_INDEXED = 20
    ABSOLUTE_INDIRECT = 21
    ABSOLUTE_INDIRECT_LONG = 22
    ABSOLUTE_INDEXED_INDIRECT = 23
    IMPLIED_ACCUMULATOR = 24
    BLOCK_MOVE = 25

# HEX: (MNEMONIC, Mode, Flags, Len, Cycles, Doc )
# FLAGs NVMXDIZC
# TODO: Mode.IMMEDIATE_8BIT maybe wrong (lucky guess because arg is 8bit)
opcode_map = {
    0x18: ("CLC", Mode.IMPLIED,         0b00000001, 1, 2, 'Clear Carry'),
    0xA9: ("LDA", Mode.IMMEDIATE_8BIT,  0b10000010, 2, 2, 'Load Accumulator from Memory'),
    0x48: ("PHA", Mode.STACK_RELATIVE,  0b00000000, 1, 3, 'Push Accumulator'),
    0xC2: ("REP", Mode.IMMEDIATE_8BIT,  0b11111111, 2, 3, 'Reset Processor Status Bits'),
    0x78: ("SEI", Mode.IMPLIED,         0b00000100, 1, 2, 'Set Interrupt Disable Flag'),
    0xE2: ("SEP", Mode.IMMEDIATE_8BIT,  0b11111111, 2, 3, 'Reset Processor Status Bits'),
    0x8D: ("STA", Mode.ABSOLUTE,        0b00000000, 3, 4, 'Store Accumulator to Memory'),
    0x9C: ("STZ", Mode.ABSOLUTE,        0b00000000, 3, 4, 'Store Zero to Memory'),
    0xEB: ("XBA", Mode.IMPLIED,         0b10000010, 1, 3, 'Exchange B and A 8-bit Accumulators'),
    0xFB: ("XCE", Mode.IMPLIED,         0b00110011, 1, 2, 'Exchange Carry and Emulation Flags')
}