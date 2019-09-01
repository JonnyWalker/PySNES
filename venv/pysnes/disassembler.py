from opcodes import opcode_map, Mode

class Disassembler(object):
    def disassemble_single_opcode(self, memory, index, add_new_line=False,
                                  add_descr=False, add_addr=False, M=False, X=False):
        opcode = memory.read(index)
        opcode_info = opcode_map[opcode]
        mnemonic = opcode_info[0]
        addr_mode = opcode_info[1]
        flags = opcode_info[2]
        length = opcode_info[3]
        cycles = opcode_info[4]
        descr = opcode_info[5]
        result = ""
        if add_addr:
            result += hex(index)+":"
        result += hex(opcode)+":"+mnemonic+" "
        index = index + 1
        if length == 2:
            immediate8bit = memory.read(index)
            result += hex(immediate8bit)
        elif length == 3 and addr_mode == Mode.IMMEDIATE_MINUS_M:
            if M:
                immediate8bit = memory.read(index)
                result += hex(immediate8bit)
            else:
                addr = memory.read(index)
                index = index + 1
                addr = addr + (memory.read(index) << 8)
                index = index + 1
                result += hex(addr)
        elif length == 3 and addr_mode == Mode.IMMEDIATE_MINUS_X:
            if X:
                immediate8bit = memory.read(index)
                result += hex(immediate8bit)
            else:
                addr = memory.read(index)
                index = index + 1
                addr = addr + (memory.read(index) << 8)
                index = index + 1
                result += hex(addr)
        elif length == 3:
            addr = memory.read(index)
            index = index + 1
            addr = addr + (memory.read(index) << 8)
            index = index + 1
            result += hex(addr)
        elif length == 4:
            addr = memory.read(index)
            index = index + 1
            addr = addr + (memory.read(index) << 8)
            index = index + 1
            addr = addr + (memory.read(index) << 16)
            index = index + 1
            result += hex(addr)
        return result

    def disassemble(self, memory, start, end, add_new_line=False, add_descr=False, add_addr=False, M=False, X=False):
        index = start
        symbolic = []
        while index < end:
            opcode_info = opcode_map[memory.read(index)]
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
            # TODO: Use 65816 synatax like dp, [byte], etc...
            # FIXME: Some opcodes have variable length.
            #       E.g. ADC has the length 2 or 3 depending on the M flag
            #       so basically, this code is wrong :'(
            if length == 2:
                immediate8bit = memory.read(index)
                symbolic.append(hex(immediate8bit))
                index = index + 1
            elif length == 3 and addr_mode == Mode.IMMEDIATE_MINUS_M:
                if M:
                    immediate8bit = memory.read(index)
                    symbolic.append(hex(immediate8bit))
                    index = index + 1
                else:
                    addr = memory.read(index)
                    index = index + 1
                    addr = addr + (memory.read(index) << 8)
                    index = index + 1
                    symbolic.append(hex(addr))
            elif length == 3 and addr_mode == Mode.IMMEDIATE_MINUS_X:
                if X:
                    immediate8bit = memory.read(index)
                    symbolic.append(hex(immediate8bit))
                    index = index + 1
                else:
                    addr = memory.read(index)
                    index = index + 1
                    addr = addr + (memory.read(index) << 8)
                    index = index + 1
                    symbolic.append(hex(addr))
            elif length == 3:
                addr = memory.read(index)
                index = index + 1
                addr = addr + (memory.read(index) << 8)
                index = index + 1
                symbolic.append(hex(addr))
            elif length == 4:
                addr = memory.read(index)
                index = index + 1
                addr = addr + (memory.read(index) << 8)
                index = index + 1
                addr = addr + (memory.read(index) << 16)
                index = index + 1
                symbolic.append(hex(addr))
            if add_descr:
                if length == 2:
                    symbolic.append("\t"*(2) + descr)
                elif length == 3:
                    symbolic.append("\t"*(2) + descr)
                else:
                    symbolic.append("\t"*(3) + descr)
            if add_new_line:
                symbolic.append("\n")
        return symbolic

    def print_assembler(self, memory, start, end):
        symbolic_code = self.disassemble(memory, start, end, True, True, True, True, False) # FIXME
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


