from opcodes import Mode, opcode_map

class Disassembler(object):
    def disassemble(self, byte_array, add_new_line=False, add_descr=False, add_addr=False):
        index = 0
        symbolic = []
        while index < len(byte_array):
            opcode_info = opcode_map[byte_array[index]]
            mnemonic = opcode_info[0]
            addr_mode = opcode_info[1]
            flags = opcode_info[2]
            length = opcode_info[3]
            cycles = opcode_info[4]
            descr = opcode_info[5]
            if add_addr:
                symbolic.append(hex(index)+":\t"+mnemonic)
            else:
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
            if add_descr:
                symbolic.append("\t"*(4-length)+descr)
            if add_new_line:
                symbolic.append("\n")
        return symbolic

    def print_assembler(self, ba, start, end):
        symbolic_code = self.disassemble(ba[start:end], True, True, True)
        i = 0
        print
        print("Assembly:")
        print
        while i < len(symbolic_code):
            string = symbol = symbolic_code[i]
            while i < len(symbolic_code):
                i = i + 1
                symbol = symbolic_code[i]
                if symbol == '\n':
                    break
                string += " " + symbol
            i = i + 1
            print(string)


