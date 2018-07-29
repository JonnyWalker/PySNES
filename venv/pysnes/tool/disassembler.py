from opcodes import Mode, opcode_map

class Disassembler(object):
    def disassemble(self, byte_array):
        index = 0
        symbolic = []
        while index < len(byte_array):
            opcode_info = opcode_map[byte_array[index]]
            mnemonic = opcode_info[0]
            addr_mode = opcode_info[1]
            flags = opcode_info[2]
            length = opcode_info[3]
            cycles = opcode_info[4]
            symbolic.append(mnemonic)
            index = index + 1
            if length == 2  and addr_mode == Mode.IMMEDIATE_8BIT:
                immediate8bit = byte_array[index]
                symbolic.append("(I8)" + hex(immediate8bit))
                index = index + 1
            elif length == 3 and addr_mode == Mode.ABSOLUTE: # Address
                addr = byte_array[index]
                index = index + 1
                addr = addr + (byte_array[index] << 8)
                index = index + 1
                symbolic.append("(ADDR)" + hex(addr))
        return symbolic


