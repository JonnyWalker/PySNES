import address_computation_helper as compute_addr

class CPU65816(object):
    def __init__(self, memory):
        self.A = 0      # Accumulator           - 8 or 16 Bit (also called A(8Bit) and B(next 8Bit))
        self.X = 0      # Index Register        - 8 or 16 Bit
        self.Y = 0      # Index Register        - 8 or 16 Bit
        self.SP = 0     # Stack Pointer         - 16 Bit
        self.DBR = 0    # Data Bank Register    - 8 Bit (also called B)
        self.DP = 0     # Direct Page Register  - 16 Bit (also called D)
        self.PBR = 0    # Program Bank Register - 8 Bit (also called K)
        #self.P = 0x34   # Flag Register         - 8 Bit #TODO check if init ok
        self.P = 0
        self.PC = memory.header.reset_int_addr  # Program Counter       - 16 Bit
        self.memory = memory
        self.cycles = 0
        self.e = 1  # e-flag = 0 (native 16 Bit) e-flag = 1 (emulation 8 Bit)
        self.stack = [] # only for debugging


    def fetch_decode_execute(self):
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        opcode = self.memory.read((self.PBR << 16) +self.PC)
        # this meean every address > 0xFF will be wrapped. E.g. 0xFF +1 == 0x00
        # TODO: use BCD sub if D Flag is set
        # ADC (dp, X)
        if opcode == 0x61:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True)  # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # ADC stk, S
        elif opcode == 0x63:
            byte = self.fetch_byte()
            address = compute_addr.stack(byte, self.SP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # ADC dp
        elif opcode == 0x65:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # ADC [dp]
        elif opcode == 0x67:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            address = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # ADC #const
        elif opcode == 0x69:
            if self.isM():
                const = self.fetch_byte()
            else:
                const = self.fetch_twobyte()
            result = self.add_twos_complement(self.A, const + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 3 - self.m()
            self.PC = self.PC + 1
        # ADC abs
        elif opcode == 0x6D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # ADC long
        elif opcode == 0x6F:
            address = self.fetch_threebyte()
            value = self.read_memory(address, byte_num=2 - self.m())  # no wrapping
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # ADC (dp), Y
        elif opcode == 0x71:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 7 - self.m() + self.w() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # ADC (dp)
        elif opcode == 0x72:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2-self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 6 - self.m() + self.w()
            self.PC = self.PC + 1
        # ADC (stk, S), Y
        elif opcode == 0x73:
            byte = self.fetch_byte()
            address_pointer = compute_addr.stack(byte, self.SP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True)  # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 8 - self.m()
            self.PC = self.PC + 1
        # ADC dir, X
        elif opcode == 0x75:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 5 - self.m() + self.w()
            self.PC = self.PC + 1
        # ADC [dir], Y
        elif opcode == 0x77:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            address = compute_addr.long_y(bytes, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # ADC abs, Y
        elif opcode == 0x79:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # ADC abs, X
        elif opcode == 0x7D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # ADC long, X
        elif opcode == 0x7F:
            bytes = self.fetch_threebyte()
            address = compute_addr.long_x(bytes, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.add_twos_complement(self.A, value + self.c(), self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # AND (dp, X)
        elif opcode == 0x21:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # AND stk, S
        elif opcode == 0x23:
            byte = self.fetch_byte()
            address = compute_addr.stack(byte, self.SP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # AND dp
        elif opcode == 0x25:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # AND [dp]
        elif opcode == 0x27:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            address = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # AND #const
        elif opcode == 0x29:
            if self.isM():
                value = self.fetch_byte()
            else:
                value = self.fetch_twobyte()
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 3-self.isM()
            self.PC = self.PC + 1
        # AND abs
        elif opcode == 0x2D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # AND long
        elif opcode == 0x2F:
            address = self.fetch_threebyte()
            value = self.read_memory(address, byte_num=2 - self.m())  # no wrapping
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # AND (dp), Y
        elif opcode == 0x31:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 7 - self.m() + self.w() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # AND (dp)
        elif opcode == 0x32:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2-self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 6 - self.m() + self.w()
            self.PC = self.PC + 1
        # AND (stk, S), Y
        elif opcode == 0x33:
            byte = self.fetch_byte()
            address_pointer = compute_addr.stack(byte, self.SP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 8 - self.m()
            self.PC = self.PC + 1
        # AND dp, X
        elif opcode == 0x35:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 5-self.m() + self.w()
            self.PC = self.PC + 1
        # AND [dp], Y
        elif opcode == 0x37:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            address = compute_addr.long_y(bytes, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # AND abs, Y
        elif opcode == 0x39:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # AND abs, X
        elif opcode == 0x3D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # AND long, X
        elif opcode == 0x3F:
            bytes = self.fetch_threebyte()
            address = compute_addr.long_x(bytes, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A & value)
            self.A = result
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # ASL A
        elif opcode == 0x0A:
            self.A = self.A << 1
            self.cycles += 2
            self.PC = self.PC + 1
        # BCC nearlabel
        elif opcode == 0x90:
            nearlabel = self.fetch_byte()
            self.cycles += 2
            if not self.isC():
                self.PC = self.computeBXX(nearlabel)
            else:
                self.PC = self.PC + 1
        # BCS nearlabel
        elif opcode == 0xB0:
            nearlabel = self.fetch_byte()
            self.cycles += 2
            if self.isC():
                self.PC = self.computeBXX(nearlabel)
            else:
                self.PC = self.PC + 1
        # BEQ nearlabel
        elif opcode == 0xF0:
            nearlabel = self.fetch_byte()
            self.cycles += 2
            if self.isZ():
                self.PC = self.computeBXX(nearlabel)
            else:
                self.PC = self.PC + 1
        # BIT dp
        elif opcode == 0x24:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num=2 - self.m(), wrapp=True)  # zero bank wrapping!
            self.compute_bit_flags(value)
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # BIT abs
        elif opcode == 0x2C:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2 - self.m())
            self.compute_bit_flags(value)
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # BIT dir, X
        elif opcode == 0x34:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m(), wrapp=True)  # zero bank wrapping!
            self.compute_bit_flags(value)
            self.cycles += 5 - self.m() + self.w()
            self.PC = self.PC + 1
        # BIT abs, X
        elif opcode == 0x3C:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            self.compute_bit_flags(value)
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # BIT imm
        # this is the only bit opcode that only affects the Z flag
        elif opcode == 0x89:
            if self.isM():
                value = self.fetch_byte()
                if not value & (0x00FF & self.A):
                    self.setZ()
                else:
                    self.clearZ()
            else:
                value = self.fetch_twobyte()
                if not value & self.A:
                    self.setZ()
                else:
                    self.clearZ()
            self.cycles += 3 - self.m()
            self.PC = self.PC + 1
        # BMI nearlabel
        elif opcode == 0x30:
            nearlabel = self.fetch_byte()
            self.cycles += 2
            if self.isN():
                self.PC = self.computeBXX(nearlabel)
            else:
                self.PC = self.PC + 1
        # BNE nearlabel
        elif opcode == 0xD0:
            nearlabel = self.fetch_byte()
            self.cycles += 2
            if not self.isZ():
                self.PC = self.computeBXX(nearlabel)
            else:
                self.PC = self.PC + 1
        # BPL nearlabel
        elif opcode == 0x10:
            nearlabel = self.fetch_byte()
            self.cycles += 2
            if not self.isN():
                self.PC = self.computeBXX(nearlabel)
            else:
                self.PC = self.PC + 1
        # BRA nearlabel
        elif opcode == 0x80:
            nearlabel = self.fetch_byte()
            self.cycles += 2
            self.PC = self.computeBXX(nearlabel)
         # BRL label
        elif opcode == 0x82:
            label = self.fetch_twobyte() # PC +=2
            self.cycles += 4
            self.PC += label+1 # instruction length 3
        # BVC nearlabel
        elif opcode == 0x50:
            nearlabel = self.fetch_byte()
            self.cycles += 2
            if not self.isV():
                self.PC = self.computeBXX(nearlabel)
            else:
                self.PC = self.PC + 1
        # BVS nearlabel
        elif opcode == 0x70:
            nearlabel = self.fetch_byte()
            self.cycles += 2
            if self.isV():
                self.PC = self.computeBXX(nearlabel)
            else:
                self.PC = self.PC + 1
        # CLC
        elif opcode == 0x18:
            self.clearC()
            self.cycles += 2
            self.PC = self.PC + 1
        # CLD
        elif opcode == 0xD8:
            self.clearD()
            self.cycles += 2
            self.PC = self.PC + 1
        # CLI
        elif opcode == 0x58:
            self.clearI()
            self.cycles += 2
            self.PC = self.PC + 1
        # CLV
        elif opcode == 0xB8:
            self.clearV()
            self.cycles += 2
            self.PC = self.PC + 1
        # CMP (dir, X)
        elif opcode == 0xC1:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True)  # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # CMP stk, S
        elif opcode == 0xC3:
            byte = self.fetch_byte()
            address = compute_addr.stack(byte, self.SP)
            value = self.read_memory(address, byte_num=2 - self.m(), wrapp=True)  # zero bank wrapping
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # CMP dir
        elif opcode == 0xC5:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num=2 - self.m(), wrapp=True)  # zero bank wrapping!
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # CMP [dir]
        elif opcode == 0xC7:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            address = self.read_memory(address_pointer, byte_num=3, wrapp=True)  # zero bank wrapping!
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # CMP #const
        elif opcode == 0xC9:
            if self.isM():
                const = self.fetch_byte()
            else:
                const = self.fetch_twobyte()
            result = self.A - const
            self.compute_NZflags(result, self.isM())
            if self.A >= const:
                self.setC()
            else:
                self.clearC()
            self.cycles += 3 - self.m()
            self.PC = self.PC + 1
        # CMP abs
        elif opcode == 0xCD:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # CMP long
        elif opcode == 0xCF:
            address = self.fetch_threebyte()
            value = self.read_memory(address, byte_num=2 - self.m())  # no wrapping
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # CMP (dir), Y
        elif opcode == 0xD1:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True)  # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 7 - self.m() + self.w() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # CMP (dir)
        elif opcode == 0xD2:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True)  # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 6 - self.m() + self.w()
            self.PC = self.PC + 1
        # CMP (stk, S), Y
        elif opcode == 0xD3:
            byte = self.fetch_byte()
            address_pointer = compute_addr.stack(byte, self.SP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True)  # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 8 - self.m()
            self.PC = self.PC + 1
        # CMP dir, X
        elif opcode == 0xD5:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m(), wrapp=True)  # zero bank wrapping!
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 5 - self.m() + self.w()
            self.PC = self.PC + 1
        # CMP [dir], Y
        elif opcode == 0xD7:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=3, wrapp=True)  # zero bank wrapping!
            address = compute_addr.long_y(bytes, self.Y, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # CMP abs, Y
        elif opcode == 0xD9:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # CMP abs, X
        elif opcode == 0xDD:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # CMP long, X
        elif opcode == 0xDF:
            bytes = self.fetch_threebyte()
            address = compute_addr.long_x(bytes, self.X, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.A - value
            self.compute_NZflags(result, self.isM())
            if self.A >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # CPX #const
        elif opcode == 0xE0:
            if self.isX():
                const = self.fetch_byte()
            else:
                const = self.fetch_twobyte()
            result = self.X - const
            self.compute_NZflags(result, self.isM())
            if self.X >= const:
                self.setC()
            else:
                self.clearC()
            self.cycles += 3 - self.x()
            self.PC = self.PC + 1
        # CPX dir
        elif opcode == 0xE4:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num=2 - self.m(), wrapp=True)  # zero bank wrapping!
            result = self.X - value
            self.compute_NZflags(result, self.isX())
            if self.X >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 4 - self.x() + self.w()
            self.PC = self.PC + 1
        # CPX abs
        elif opcode == 0xEC:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.X - value
            self.compute_NZflags(result, self.isM())
            if self.X >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 5 - self.x()
            self.PC = self.PC + 1
        # CPY #const
        elif opcode == 0xC0:
            if self.isX():
                const = self.fetch_byte()
            else:
                const = self.fetch_twobyte()
            result = self.Y - const
            self.compute_NZflags(result, self.isM())
            if self.Y >= const:
                self.setC()
            else:
                self.clearC()
            self.cycles += 3 - self.x()
            self.PC = self.PC + 1
        # CPY dir
        elif opcode == 0xC4:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num=2 - self.m(), wrapp=True)  # zero bank wrapping!
            result = self.Y - value
            self.compute_NZflags(result, self.isX())
            if self.Y >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 4 - self.x() + self.w()
            self.PC = self.PC + 1
        # CPY abs
        elif opcode == 0xCC:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.Y - value
            self.compute_NZflags(result, self.isM())
            if self.Y >= value:
                self.setC()
            else:
                self.clearC()
            self.cycles += 5 - self.x()
            self.PC = self.PC + 1
        # DEC A
        elif opcode == 0x3A:
            result = self.sub_twos_complement(self.A, 1, is8BitMode = self.isM())
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # DEC dp
        elif opcode == 0xC6:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.sub_twos_complement(value, 1, is8BitMode=self.isM())
            self.compute_NZflags(result, self.isM())
            self.write_memory(address, result, byte_num = 2 - self.m(), wrapp=True)  # zero bank wrapping!
            self.cycles += 7 - self.m()*2 + self.w()
            self.PC = self.PC + 1
        # DEC abs
        elif opcode == 0xCE:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.sub_twos_complement(value, 1, is8BitMode = self.isM())
            self.compute_NZflags(result, self.isM())
            self.write_memory(address, result, byte_num = 2 - self.m()) # no wrapping
            self.cycles += 8 - self.m() * 2
            self.PC = self.PC + 1
        # DEC dp, X
        elif opcode == 0xD6:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.sub_twos_complement(value, 1, is8BitMode = self.isM())
            self.compute_NZflags(result, self.isM())
            self.write_memory(address, result, byte_num = 2 - self.m(), wrapp=True)  # zero bank wrapping!
            self.cycles += 8 - self.m() * 2 + self.w()
            self.PC = self.PC + 1
        # DEC abs, X
        elif opcode == 0xDE:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.sub_twos_complement(value, 1, is8BitMode=self.isM())
            self.compute_NZflags(result, self.isM())
            self.write_memory(address, result, byte_num = 2 - self.m())
            self.cycles += 9 - self.m() * 2
            self.PC = self.PC + 1
        # DEX
        elif opcode == 0xCA:
            result = self.sub_twos_complement(self.X, 1, is8BitMode = self.isX())
            self.compute_NZflags(result, self.isX())
            self.X = result
            self.cycles += 2
            self.PC = self.PC + 1
        # DEY
        elif opcode == 0x88:
            result = self.sub_twos_complement(self.Y, 1, is8BitMode = self.isX())
            self.compute_NZflags(result, self.isX())
            self.Y = result
            self.cycles += 2
            self.PC = self.PC + 1
        # EOR (dp, X)
        elif opcode == 0x41:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # EOR stk, S
        elif opcode == 0x43:
            byte = self.fetch_byte()
            address = compute_addr.stack(byte, self.SP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # EOR dp
        elif opcode == 0x45:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # EOR [dp]
        elif opcode == 0x47:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            address = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # EOR #const
        elif opcode == 0x49:
            if self.isM():
                value = self.fetch_byte()
            else:
                value = self.fetch_twobyte()
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 3-self.isM()
            self.PC = self.PC + 1
        # EOR abs
        elif opcode == 0x4D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # EOR long
        elif opcode == 0x4F:
            address = self.fetch_threebyte()
            value = self.read_memory(address, byte_num=2 - self.m())  # no wrapping
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # EOR (dp), Y
        elif opcode == 0x51:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 7 - self.m() + self.w() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # EOR (dp)
        elif opcode == 0x52:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2-self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 6 - self.m() + self.w()
            self.PC = self.PC + 1
        # EOR (stk, S), Y
        elif opcode == 0x53:
            byte = self.fetch_byte()
            address_pointer = compute_addr.stack(byte, self.SP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 8 - self.m()
            self.PC = self.PC + 1
        # EOR dp, X
        elif opcode == 0x55:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 5-self.m() + self.w()
            self.PC = self.PC + 1
        # EOR [dp], Y
        elif opcode == 0x57:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            address = compute_addr.long_y(bytes, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # EOR abs, Y
        elif opcode == 0x59:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # EOR abs, X
        elif opcode == 0x5D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # EOR long, X
        elif opcode == 0x5F:
            bytes = self.fetch_threebyte()
            address = compute_addr.long_x(bytes, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A ^ value)
            self.A = result
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # INC A
        elif opcode == 0x1A:
            if self.isM():
                result = (self.A + 1) & 0x0000FF
            else:
                result = (self.A + 1) & 0x00FFFF
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # INC dp
        elif opcode == 0xE6:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            if self.isM():
                result = (value + 1) & 0x0000FF
            else:
                result = (value + 1) & 0x00FFFF
            self.compute_NZflags(result, self.isM())
            self.write_memory(address, result, byte_num = 2 - self.m(), wrapp=True)  # zero bank wrapping!
            self.cycles += 7 - self.m()*2 + self.w()
            self.PC = self.PC + 1
        # INC abs
        elif opcode == 0xEE:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            if self.isM():
                result = (value + 1) & 0x0000FF
            else:
                result = (value + 1) & 0x00FFFF
            self.compute_NZflags(result, self.isM())
            self.write_memory(address, result, byte_num = 2 - self.m()) # no wrapping
            self.cycles += 8 - self.m() * 2
            self.PC = self.PC + 1
        # INC dp, X
        elif opcode == 0xF6:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            if self.isM():
                result = (value + 1) & 0x0000FF
            else:
                result = (value + 1) & 0x00FFFF
            self.compute_NZflags(result, self.isM())
            self.write_memory(address, result, byte_num = 2 - self.m(), wrapp=True)  # zero bank wrapping!
            self.cycles += 8 - self.m() * 2 + self.w()
            self.PC = self.PC + 1
        # INC abs, X
        elif opcode == 0xFE:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            if self.isM():
                result = (value + 1) & 0x0000FF
            else:
                result = (value + 1) & 0x00FFFF
            self.compute_NZflags(result, self.isM())
            self.write_memory(address, result, byte_num = 2 - self.m())
            self.cycles += 9 - self.m() * 2
            self.PC = self.PC + 1
        # INX
        elif opcode == 0xE8:
            if self.isX():
                result = (self.X + 1) & 0x0000FF
            else:
                result = (self.X + 1) & 0x00FFFF
            self.compute_NZflags(result, self.isX())
            self.X = result
            self.cycles += 2
            self.PC = self.PC + 1
        # INY
        elif opcode == 0xC8:
            if self.isX():
                result = (self.Y + 1) & 0x0000FF
            else:
                result = (self.Y + 1) & 0x00FFFF
            self.compute_NZflags(result, self.isX())
            self.Y = result
            self.cycles += 2
            self.PC = self.PC + 1
        # JMP addr
        elif opcode == 0x4C:
            label = self.fetch_twobyte()
            self.cycles += 3
            self.PC = label
        # JMP long
        elif opcode == 0x5C:
            label = self.fetch_twobyte()
            bank = self.fetch_byte()
            self.PBR = bank
            self.cycles += 4
            self.PC = label
        # JMP (addr)
        elif opcode == 0x6C:
            addr = self.fetch_twobyte()
            label = self.read_memory((0x0 << 16) + addr, byte_num = 2, wrapp=True) # zero bank wrapping!
            self.cycles += 5
            self.PC = label
        # JMP (addr, X)
        elif opcode == 0x7C:
            addr = self.fetch_twobyte()
            wrapped_addr = (addr + self.X) & 0xFFFF
            label = self.read_memory((self.DBR << 16) + wrapped_addr, byte_num = 2, wrapp=True) # zero bank wrapping!
            self.cycles += 6
            self.PC = label
        # JMP [addr]
        elif opcode == 0xDC:
            addr = self.fetch_twobyte()
            label = self.read_memory((0x0 << 16) + addr, byte_num = 3, wrapp=True) # zero bank wrapping!
            self.PBR = (label & 0xFF0000) >> 16
            self.cycles += 6
            self.PC = label & 0x00FFFF
        # JSL long
        elif opcode == 0x22:
            self.push_stack_8bit(self.PBR) # save return addr
            self.push_stack(self.PC + 3)   # save return addr
            label = self.fetch_twobyte()
            bank = self.fetch_byte()
            self.PBR = bank
            self.cycles += 8
            self.PC = label
        # JSR addr
        elif opcode == 0x20:
            self.push_stack(self.PC + 2) # save return addr
            label = self.fetch_twobyte()
            self.cycles += 6
            self.PC = label
        # JSR (addr, X)
        elif opcode == 0xFC:
            self.push_stack(self.PC + 2)  # save return addr
            addr = self.fetch_twobyte()
            wrapped_addr = (addr + self.X) & 0xFFFF
            label = self.read_memory((self.DBR << 16) + wrapped_addr, byte_num = 2, wrapp=True) # zero bank wrapping!
            self.cycles += 8
            self.PC = label
        # LDA (dp, X)
        elif opcode == 0xA1:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # LDA stk, S
        elif opcode == 0xA3:
            byte = self.fetch_byte()
            address = compute_addr.stack(byte, self.SP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # LDA dp
        elif opcode == 0xA5:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # LDA [dp]
        elif opcode == 0xA7:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            address = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # LDA #const
        elif opcode == 0xA9:
            if self.isM(): # 8 Bit A/M
                const = self.fetch_byte() # M=1 -> 8 Bit A -> one byte
            else:  # 16 Bit A/M
                const = self.fetch_twobyte()  # M=0 -> 16 Bit A -> two byte
            result = const
            self.compute_NZflags(result, self.isM())
            self.A = result
            self.cycles += 3 - self.m()
            self.PC = self.PC + 1
        # LDA abs
        elif opcode == 0xAD:
            bytes = self.fetch_twobyte() # no wrapping
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # LDA long
        elif opcode == 0xAF:
            address = self.fetch_threebyte()
            value = self.read_memory(address, byte_num = 2 - self.m()) # no wrapping
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # LDA (dp), Y
        elif opcode == 0xB1:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 7 - self.m() + self.w() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # LDA (dp)
        elif opcode == 0xB2:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 6 - self.m() + self.w()
            self.PC = self.PC + 1
        # LDA (stk, S), Y
        elif opcode == 0xB3:
            byte = self.fetch_byte()
            address_pointer = compute_addr.stack(byte, self.SP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 8 - self.m()
            self.PC = self.PC + 1
        # LDA dp, X
        elif opcode == 0xB5:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 5 - self.m() + self.w()
            self.PC = self.PC + 1
        # LDA [dp], Y
        elif opcode == 0xB7:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            address = compute_addr.long_y(bytes, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # LDA abs, Y
        elif opcode == 0xB9:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # LDA abs, X
        elif opcode == 0xBD:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # LDA long, X
        elif opcode == 0xBF:
            bytes = self.fetch_threebyte()
            address = compute_addr.long_x(bytes, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isM())
            self.A = value
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # LDX #const
        elif opcode == 0xA2:
            if self.isX(): # 8 Bit Y/X
                const = self.fetch_byte() # X=1 -> 8 Bit X -> one byte
            else:  # 16 Bit X/Y
                const = self.fetch_twobyte()  # X=0 -> 16 Bit X -> two byte
            result = const
            self.compute_NZflags(result, self.isX())
            self.X = result
            self.cycles += 3 - self.x()
            self.PC = self.PC + 1
        # LDX dp
        elif opcode == 0xA6:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.compute_NZflags(value, self.isX())
            self.X = value
            self.cycles += 4 - self.x() + self.w()
            self.PC = self.PC + 1
        # LDX abs
        elif opcode == 0xAE:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isX())
            self.X = value
            self.cycles += 5 - self.x()
            self.PC = self.PC + 1
        # LDX dp, Y
        elif opcode == 0xB6:
            byte = self.fetch_byte()
            address = compute_addr.dp_y(byte, self.DP, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.compute_NZflags(value, self.isX())
            self.X = value
            self.cycles += 5 - self.x() + self.w()
            self.PC = self.PC + 1
        # LDX abs, Y
        elif opcode == 0xBE:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isX())
            self.X = value
            self.cycles += 6 - 2 * self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # LDY #const
        elif opcode == 0xA0:
            if self.isX():  # 8 Bit Y/X
                const = self.fetch_byte()     # X=1 ->  8 Bit Y -> one byte
            else:           # 16 Bit X/Y
                const = self.fetch_twobyte()  # X=0 -> 16 Bit Y -> two byte
            result = const
            self.compute_NZflags(result, self.isX())
            self.Y = result
            self.cycles += 3 - self.x()
            self.PC = self.PC + 1
        # LDY dp
        elif opcode == 0xA4:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.compute_NZflags(value, self.isX())
            self.Y = value
            self.cycles += 4 - self.x() + self.w()
            self.PC = self.PC + 1
        # LDY abs
        elif opcode == 0xAC:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isX())
            self.Y = value
            self.cycles += 5 - self.x()
            self.PC = self.PC + 1
        # LDY dp, X
        elif opcode == 0xB4:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.compute_NZflags(value, self.isX())
            self.Y = value
            self.cycles += 5 - self.x() + self.w()
            self.PC = self.PC + 1
        # LDY abs, X
        elif opcode == 0xBC:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            self.compute_NZflags(value, self.isX())
            self.Y = value
            self.cycles += 6 - 2 * self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # LSR A
        elif opcode == 0x4A:
            result = self.A >> 1
            self.compute_NZflags(result, self.isM())
            if self.A & 0b1 == 1:
                self.setC()
            else:
                self.clearC()
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # NOP
        elif opcode == 0xEA:
            self.cycles += 2
            self.PC = self.PC + 1
        # ORA (dp, X)
        elif opcode == 0x01:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # ORA stk, S
        elif opcode == 0x03:
            byte = self.fetch_byte()
            address = compute_addr.stack(byte, self.SP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # ORA dp
        elif opcode == 0x05:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # ORA [dp]
        elif opcode == 0x07:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            address = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # ORA #const
        elif opcode == 0x09:
            if self.isM():
                value = self.fetch_byte()
            else:
                value = self.fetch_twobyte()
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 3-self.isM()
            self.PC = self.PC + 1
        # ORA abs
        elif opcode == 0x0D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # ORA long
        elif opcode == 0x0F:
            address = self.fetch_threebyte()
            value = self.read_memory(address, byte_num=2 - self.m())  # no wrapping
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # ORA (dp), Y
        elif opcode == 0x11:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 7 - self.m() + self.w() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # ORA (dp)
        elif opcode == 0x12:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num=2-self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 6 - self.m() + self.w()
            self.PC = self.PC + 1
        # ORA (stk, S), Y
        elif opcode == 0x13:
            byte = self.fetch_byte()
            address_pointer = compute_addr.stack(byte, self.SP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num=2 - self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 8 - self.m()
            self.PC = self.PC + 1
        # ORA dp, X
        elif opcode == 0x15:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 5-self.m() + self.w()
            self.PC = self.PC + 1
        # ORA [dp], Y
        elif opcode == 0x17:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            address = compute_addr.long_y(bytes, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # ORA abs, Y
        elif opcode == 0x19:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # ORA abs, X
        elif opcode == 0x1D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
            self.PC = self.PC + 1
        # ORA long, X
        elif opcode == 0x1F:
            bytes = self.fetch_threebyte()
            address = compute_addr.long_x(bytes, self.X, self.isX())
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_logic_operation(self.A | value)
            self.A = result
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # PEA imm
        elif opcode == 0xF4:
            bytes = self.fetch_twobyte()
            self.push_stack(bytes)
            self.cycles += 5
            self.PC = self.PC + 1
        # PEI dir
        elif opcode == 0xD4:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2, wrapp=True)
            self.push_stack(value)
            self.cycles = 6 + self.w()
            self.PC = self.PC + 1
        # PER imm
        elif opcode == 0x62:
            bytes = self.fetch_twobyte()
            self.push_stack(bytes + self.PC+1)
            self.cycles += 6
            self.PC = self.PC + 1
        # PHA
        elif opcode == 0x48:
            if self.isM():# 8 bit mode
                self.push_stack_8bit(self.A & 0x00FF)
                self.cycles += 3
                self.PC += 1
            else: # 16 bit mode
                self.push_stack(self.A)
                self.cycles += 4
                self.PC += 1
        # PHB
        elif opcode == 0x8B:
            self.push_stack_8bit(self.DBR)
            self.cycles += 3
            self.PC = self.PC + 1
        # PHD
        elif opcode == 0x0B:
            self.push_stack(self.DP)
            self.cycles += 4
            self.PC = self.PC + 1
        # PHK
        elif opcode == 0x4B:
            self.push_stack_8bit(self.PBR)
            self.cycles += 3
            self.PC = self.PC + 1
        # PHP
        elif opcode == 0x08:
            self.push_stack_8bit(self.P)
            self.cycles += 3
            self.PC = self.PC + 1
        # PHX
        elif opcode == 0xDA:
            if self.isX():
                self.push_stack_8bit(self.X & 0x00FF)
                self.cycles += 3
                self.PC += 1
            else:
                self.push_stack(self.X)
                self.cycles += 4
                self.PC += 1
        # PHY
        elif opcode == 0x5A:
            if self.isX():# x flag also controls Y register.
                self.push_stack_8bit(self.Y & 0x00FF)
                self.cycles += 3
                self.PC += 1
            else:
                self.push_stack(self.Y)
                self.cycles += 4
                self.PC += 1
        # PLA
        elif opcode == 0x68:
            if self.isM(): # 8 bit mode
                A_low = self.pop_stack_8bit()
                A_high = self.A & 0xFF00
                self.A = A_high + A_low # in 8 bit mode the high byte of the A register persists
                self.compute_NZflags(A_low, True)
                self.cycles += 4
                self.PC += 1
            else: # 16 bit mode
                self.A = self.pop_stack()
                self.compute_NZflags(self.A, False)
                self.cycles += 5
                self.PC += 1
        # PLB
        elif opcode == 0xAB:
            result = self.pop_stack_8bit()
            self.compute_NZflags(result, True)
            self.DBR = result
            self.cycles += 4
            self.PC += 1
        # PLD
        elif opcode == 0x2B:
            result = self.pop_stack()
            self.compute_NZflags(result, False)
            self.DP = result
            self.cycles += 5
            self.PC += 1
        # PLP
        elif opcode == 0x28:
            self.P = self.pop_stack_8bit()
            if self.e:
                self.P = self.P | 0b00110000
            self.cycles += 4
            self.PC += 1
        # PLX
        elif opcode == 0xFA:
            if self.isX():
                self.X = self.pop_stack_8bit() # in 8 bit mode the high byte of X is forced to 0
                self.compute_NZflags(self.X,True)
                self.cycles += 4
                self.PC += 1
            else:
                self.X = self.pop_stack()
                self.compute_NZflags(self.X,False)
                self.cycles += 5
                self.PC += 1
        # PLY
        elif opcode == 0x7A:
            if self.isX(): # there is no y flag. the x flag controls the Y register.
                self.Y = self.pop_stack_8bit() # in 8 bit mode the high byte of Y is forced to 0
                self.compute_NZflags(self.Y,True)
                self.cycles += 4
                self.PC += 1
            else:
                self.Y = self.pop_stack()
                self.compute_NZflags(self.Y,False)
                self.cycles += 5
                self.PC += 1
        # REP
        elif opcode == 0xC2:
            const = self.fetch_byte()
            nconst = ~const
            self.P = self.P & nconst
            if self.e: # if e is one, m and x will always be 1
                self.P = self.P | 0b00110000
            self.cycles += 3
            self.PC = self.PC + 1
        # ROL A
        elif opcode == 0x2A:
            result = self.A << 1
            if self.isC():
                result = result & 0b1111111111111111
            else:
                result = result & 0b1111111111111110
            self.compute_NZflags(result, self.isM())
            if self.A & 0b10000000 != 0:
                self.setC()
            else:
                self.clearC()
            self.A = result
            self.PC = self.PC + 1
        # ROR A
        elif opcode == 0x6A:
            result = self.A >> 1
            if self.isC():
                result = result & 0b1111111111111111
            else:
                result = result & 0b0111111111111111
            self.compute_NZflags(result, self.isM())
            if self.A & 0b00000001 != 0:
                self.setC()
            else:
                self.clearC()
            self.A = result
            self.PC = self.PC + 1
        # RTS
        elif opcode == 0x60:
            addr = self.pop_stack() # get return addr
            self.cycles += 6
            self.PC = addr +1
        # RTL
        elif opcode == 0x6B:
            addr = self.pop_stack()      # get return addr
            bank = self.pop_stack_8bit() # get return addr
            self.PBR = bank
            self.cycles += 6
            self.PC = addr +1
        # TODO: use BCD sub if D Flag is set
        # SBC #const #TODO: v and c
        elif opcode == 0xE9:
            const = self.fetch_byte()
            result = self.A - const - 1
            self.compute_NZflags(result, self.isM())
            self.A = result
            if self.isC():
                self.A += 1
            self.cycles += 2
            self.PC = self.PC + 1
        # SEC
        elif opcode == 0x38:
            self.setC()
            self.cycles += 2
            self.PC = self.PC + 1
        # SED
        elif opcode == 0xF8:
            self.setD()
            self.cycles += 2
            self.PC = self.PC + 1
        # SEI (Disable Interrupts) Set I to 1
        elif opcode == 0x78:
            self.setI()
            self.cycles += 2
            self.PC = self.PC + 1
        # SEP #const
        elif opcode == 0xE2:
            const = self.fetch_byte()
            self.P = self.P | const;
            self.cycles += 3
            self.PC = self.PC + 1
        # STA (dp, X)
        elif opcode == 0x81:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA stk, S
        elif opcode == 0x83:
            byte = self.fetch_byte()
            address = compute_addr.stack(byte, self.SP)
            self.write_memory(address, self.A, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # STA dp
        elif opcode == 0x85:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            self.write_memory(address, self.A, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA [dp]
        elif opcode == 0x87:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            address = self.read_memory(address_pointer, byte_num=3, wrapp=True) # zero bank wrapping!
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA abs
        elif opcode == 0x8D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # STA long
        elif opcode == 0x8F:
            address = self.fetch_threebyte()
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # STA (dp), Y
        elif opcode == 0x91:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA (dp)
        elif opcode == 0x92:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs(bytes, self.DBR)
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 6 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA (stk, S), Y
        elif opcode == 0x93:
            byte = self.fetch_byte()
            address_pointer = compute_addr.stack(byte, self.SP)
            bytes = self.read_memory(address_pointer, byte_num=2, wrapp=True) # zero bank wrapping!
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 8 - self.m()
            self.PC = self.PC + 1
        # STA dp, X
        elif opcode == 0x95:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            self.write_memory(address, self.A, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 5 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA [dp], Y
        elif opcode == 0x97:
            byte = self.fetch_byte()
            address_pointer = compute_addr.dp(byte, self.DP)
            bytes = self.read_memory(address_pointer, byte_num=3, wrapp=True)
            address = compute_addr.long_y(bytes, self.Y, self.isX())
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA abs, Y
        elif opcode == 0x99:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_y(bytes, self.DBR, self.Y, self.isX())
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # STA abs, X
        elif opcode == 0x9D:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # STA long, X
        elif opcode == 0x9F:
            bytes = self.fetch_threebyte()
            address = compute_addr.long_x(bytes, self.X, self.isX())
            self.write_memory(address, self.A, byte_num = 2 - self.m())
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # STX dp
        elif opcode == 0x86:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            self.write_memory(address, self.X, byte_num = 2 - self.x(), wrapp=True) # zero bank wrapping!
            self.cycles += 4 - self.x() + self.w()
            self.PC = self.PC + 1
        # STX abs
        elif opcode == 0x8E:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            self.write_memory(address, self.X, byte_num = 2 - self.x())
            self.cycles += 5 - self.x()
            self.PC = self.PC + 1
        # STX dp, Y
        elif opcode == 0x96:
            byte = self.fetch_byte()
            address = compute_addr.dp_y(byte, self.DP, self.Y, self.isX())
            self.write_memory(address, self.X, byte_num = 2 - self.x(), wrapp=True) # zero bank wrapping!
            self.cycles += 5 - self.x() + self.w()
            self.PC = self.PC + 1
        # STY dp
        elif opcode == 0x84:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            self.write_memory(address, self.Y, byte_num = 2 - self.x(), wrapp=True) # zero bank wrapping!
            self.cycles += 4 - self.x() + self.w()
            self.PC = self.PC + 1
        # STY abs
        elif opcode == 0x8C:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            self.write_memory(address, self.Y, byte_num = 2 - self.x())
            self.cycles += 5 - self.x()
            self.PC = self.PC + 1
        # STY dp, X
        elif opcode == 0x94:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            self.write_memory(address, self.Y, byte_num = 2 - self.x(), wrapp=True) # zero bank wrapping!
            self.cycles += 5 - self.x() + self.w()
            self.PC = self.PC + 1
        # STZ dp
        elif opcode == 0x64:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            self.write_memory(address, 0x00, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # STZ dp, X
        elif opcode == 0x74:
            byte = self.fetch_byte()
            address = compute_addr.dp_x(byte, self.DP, self.X, self.isX())
            self.write_memory(address, 0x00, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 5 - self.m() + self.w()
            self.PC = self.PC + 1
        # STZ abs
        elif opcode == 0x9C:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            self.write_memory(address, 0x00, byte_num = 2 - self.m())
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # STZ abs, X
        elif opcode == 0x9E:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs_x(bytes, self.DBR, self.X, self.isX())
            self.write_memory(address, 0x00, byte_num = 2 - self.m())
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # TAX
        elif opcode == 0x78:
            self.compute_NZflags(self.A, self.isM())
            self.X = self.A
            self.cycles += 2
            self.PC = self.PC + 1
        # TCD
        elif opcode == 0x5B:
            self.compute_NZflags(self.A, self.isM())
            self.DP = self.A
            self.cycles += 2
            self.PC += 1
        # TCS
        elif opcode == 0x1B:
            self.compute_NZflags(self.A, self.isM())
            if self.e:
                self.SP = (self.SP & 0xFF00) | (self.A & 0x00FF)
            else:
                self.SP = self.A
            self.cycles += 2
            self.PC += 1
        # TDC
        elif opcode == 0x7B:
            self.compute_NZflags(self.DP, False) # DP is always 16 bit
            self.A = self.DP
            self.cycles += 2
            self.PC += 1
        # TSC
        elif opcode == 0x3B:
            self.compute_NZflags(self.SP, False) # SP is always 16 bit
            self.A = self.SP
            self.cycles += 2
            self.PC +=1
        # TRB dir
        elif opcode == 0x14:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.compute_trb(value)
            self.write_memory(address, result, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 7 - 2 * self.m() + self.w()
            self.PC = self.PC + 1
        # TRB abs
        elif opcode == 0x1C:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_trb(value)
            self.write_memory(address, result, byte_num=2 - self.m())
            self.cycles += 8 - 2 * self.m()
            self.PC = self.PC + 1
        # TSB dir
        elif opcode == 0x04:
            byte = self.fetch_byte()
            address = compute_addr.dp(byte, self.DP)
            value = self.read_memory(address, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.compute_tsb(value)
            self.write_memory(address, result, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 7 - 2 * self.m() + self.w()
            self.PC = self.PC + 1
        # TSB abs
        elif opcode == 0x0C:
            bytes = self.fetch_twobyte()
            address = compute_addr.abs(bytes, self.DBR)
            value = self.read_memory(address, byte_num = 2 - self.m())
            result = self.compute_tsb(value)
            self.write_memory(address, result, byte_num=2 - self.m())
            self.cycles += 8 - 2 * self.m()
            self.PC = self.PC + 1
        # TAX
        elif opcode == 0xAA:
            if self.isX():
                self.X = (self.X & 0xFF00) | (self.A & 0x00FF)
            else:
                self.X = self.A
            self.compute_NZflags(self.X, self.isX())
            self.cycles += 2
            self.PC += 1
        # TAY
        elif opcode == 0xA8:
            if self.isX():
                self.Y = (self.Y & 0xFF00) | (self.A & 0x00FF)
            else:
                self.Y = self.A
            self.compute_NZflags(self.Y, self.isX())
            self.cycles += 2
            self.PC += 1
        # TSX
        elif opcode == 0xBA:
            if self.isX():
                self.X = (self.X & 0xFF00) | (self.SP & 0x00FF)
            else:
                self.X = self.SP
            self.compute_NZflags(self.X, self.isX())
            self.cycles += 2
            self.PC += 1
        # TXA
        elif opcode == 0x8A:
            if self.isM():
                self.A = (self.A & 0xFF00) | (self.X & 0x00FF)
            else:
                self.A = self.X
            self.compute_NZflags(self.A, self.isM())
            self.cycles += 2
            self.PC += 1
        # TXS
        elif opcode == 0x9A:
            if self.e == 1:
                self.SP = (self.SP & 0xFF00) | (self.X & 0x00FF)
            else:
                self.SP = self.X
            # Flags are not set
            self.cycles += 2
            self.PC += 1
        # TXY
        elif opcode == 0x9B:
            if self.isX():
                self.Y = (self.Y & 0xFF00) | (self.X & 0x00FF)
            else:
                self.Y = self.X
            self.compute_NZflags(self.Y, self.isX())
            self.cycles += 2
            self.PC += 1
        # TYA
        elif opcode == 0x98:
            if self.isM():
                self.A = (self.A & 0xFF00) | (self.Y & 0x00FF)
            else:
                self.A = self.Y
            self.compute_NZflags(self.A, self.isM())
            self.cycles += 2
            self.PC += 1
        # TYX
        elif opcode == 0xBB:
            if self.isX():
                self.X = (self.X & 0xFF00) | (self.Y & 0x00FF)
            else:
                self.X = self.Y
            self.compute_NZflags(self.X, self.isX())
            self.cycles += 2
            self.PC += 1
        # TAX
        elif opcode == 0xAA:
            if self.isX():
                self.X = (self.X & 0xFF00) | (self.A & 0x00FF)
            else:
                self.X = self.A
            self.compute_NZflags(self.X, self.isX())
            self.cycles += 2
            self.PC += 1
        # TAY
        elif opcode == 0xA8:
            if self.isX():
                self.Y = (self.Y & 0xFF00) | (self.A & 0x00FF)
            else:
                self.Y = self.A
            self.compute_NZflags(self.Y, self.isX())
            self.cycles += 2
            self.PC += 1
        # TSX
        elif opcode == 0xBA:
            if self.isX():
                self.X = (self.X & 0xFF00) | (self.SP & 0x00FF)
            else:
                self.X = self.SP
            self.compute_NZflags(self.X, self.isX())
            self.cycles += 2
            self.PC += 1
        # TXA
        elif opcode == 0x8A:
            if self.isM():
                self.A = (self.A & 0xFF00) | (self.X & 0x00FF)
            else:
                self.A = self.X
            self.compute_NZflags(self.A, self.isM())
            self.cycles += 2
            self.PC += 1
        # TXS
        elif opcode == 0x9A:
            if self.isX():
                self.SP = (self.SP & 0xFF00) | (self.X & 0x00FF)
            else:
                self.SP = self.X
            # Flags are not set
            self.cycles += 2
            self.PC += 1
        # TXY
        elif opcode == 0x9B:
            if self.isX():
                self.Y = (self.Y & 0xFF00) | (self.X & 0x00FF)
            else:
                self.Y = self.X
            self.compute_NZflags(self.Y, self.isX())
            self.cycles += 2
            self.PC += 1
        # TYA
        elif opcode == 0x98:
            if self.isM():
                self.A = (self.A & 0xFF00) | (self.Y & 0x00FF)
            else:
                self.A = self.Y
            self.compute_NZflags(self.A, self.isM())
            self.cycles += 2
            self.PC += 1
        # TYX
        elif opcode == 0xBB:
            if self.isX():
                self.X = (self.X & 0xFF00) | (self.Y & 0x00FF)
            else:
                self.X = self.Y
            self.compute_NZflags(self.X, self.isX())
            self.cycles += 2
            self.PC += 1
        # XBA
        elif opcode == 0xEB:
            AH = (self.A & 0xFF00) >> 8
            AL = (self.A & 0x00FF)
            self.compute_NZflags(AH, True)  # 8 bit
            self.A = (AL << 8) + AH
            self.cycles += 3
            self.PC = self.PC + 1
        # XCE
        elif opcode == 0xFB:
            c = self.P & 0b00000001
            if self.e == 1:
                self.setC()
            else:
                self.clearC()
            self.e = c
            if self.e == 1: # 8 Bit 6502 Emu-mode
                self.setM() # 8 Bit A/M
                self.setX() # 8 Bit X/M
                self.SP = self.SP & 0x00FF
                self.SP = self.SP | 0x0100
                self.X = self.X & 0x00FF
                self.Y = self.Y & 0x00FF
            self.cycles += 2
            self.PC = self.PC + 1
        else:
            from opcodes import opcode_map
            print("unkown opcode:", hex(opcode), " maybe:", opcode_map[opcode])
            raise NotImplementedError()


    # used by BXX opcodes.
    def computeBXX(self, nearlabel):
        self.cycles += 1  # branch is taken
        if 0x80 <= nearlabel and nearlabel <= 0xFF:
            nextPC = self.PC - 255 + nearlabel
        else:
            nextPC = self.PC + 1 + nearlabel # plus one: fetch has read one byte
        if self.e == 1:
            self.cycles += self.p(self.PC + 1, nextPC)  # page boundary check
        return nextPC

    # compute twos complement by hand.
    def sub_twos_complement(self, value, arg, is8BitMode):
        if is8BitMode:
            result = (value + -arg) & 0x0000FF
        else:
            result = (value + -arg) & 0x00FFFF
        return result


    # compute twos complement by hand.
    def add_twos_complement(self, value, arg, is8BitMode):
        if is8BitMode:
            if value <= 0x7F and value + arg > 0x7F:  # MAX_INT (SIGNED)
                self.setV()  # Overflow Flag
            else:
                self.clearV()
            if value <= 0xFF and value + arg > 0xFF:  # MAX_INT (UNSIGNED)
                self.setC()  # Carry Flag
            else:
                self.clearC()
            result = (value + arg) & 0x0000FF
        else:
            if value <= 0x7FFF and value + arg > 0x7FFF:  # MAX_INT (SIGNED)
                self.setV()  # Overflow Flag
            else:
                self.clearV()
            if value <= 0xFFFF and value + arg > 0xFFFF:  # MAX_INT (UNSIGNED)
                self.setC()  # Carry Flag
            else:
                self.clearC()
            result = (value + arg) & 0x00FFFF
        return result


    # compute logic operation with A , operation is passed as argument
    def compute_logic_operation(self, result):
        flag_result = result
        if self.isM():  # A/M 8 Bit
            # Assumes that we have to preserve B part of A
            result = result | (self.A & 0xFF00)
            # in 8 bit mode only the lower byte sets flags
            flag_result = flag_result & 0x00FF
        self.compute_NZflags(flag_result, self.isM())
        return result

    # the n flag reflects the highest bit of the value
    # the v flag reflects the second highest bit of the value
    # the n flag is set if the value and the accumulator is 0
    def compute_bit_flags(self, value):
        if self.isM():          # 8 bit mode
            if value & 0x80:
                self.setN()
            else:
                self.clearN()
            if value & 0x40:
                self.setV()
            else:
                self.clearV()
            if not value & (self.A & 0x00FF):
                self.setZ()
            else:
                self.clearZ()
        else:                   # 16 bit mode
            if value & 0x8000:
                self.setN()
            else:
                self.clearN()
            if value & 0x4000:
                self.setV()
            else:
                self.clearV()
            if not value & self.A:
                self.setZ()
            else:
                self.clearZ()

    # sets the Z flag if (value & accumulator = 0)
    # resets the bits in the data that are 1s in the accumulator
    def compute_trb(self, value):
        if self.isM():
            if not value & (self.A & 0x00FF):
                self.setZ()
            else:
                self.clearZ()
            result = value & (~self.A & 0x00FF)
        else:
            if not value & self.A:
                self.setZ()
            else:
                self.clearZ()
            result = value & ~self.A
        return result

    # sets the Z flag if (value & accumulator = 0)
    # sets the bits in the data that are 1s in the accumulator
    def compute_tsb(self, value):
        if self.isM():
            if not value & (self.A & 0x00FF):
                self.setZ()
            else:
                self.clearZ()
            result = value | (self.A & 0x00FF)
        else:
            if not value & self.A:
                self.setZ()
            else:
                self.clearZ()
            result = value | self.A
        return result

    def fetch_byte(self):
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        return self.memory.read((self.PBR << 16) +self.PC)

    # little endian
    def fetch_twobyte(self):
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = self.memory.read((self.PBR << 16) + self.PC)
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = (self.memory.read((self.PBR << 16) + self.PC) << 8) + addr
        return addr

    # little endian
    def fetch_threebyte(self):
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = self.memory.read((self.PBR << 16) +self.PC)
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = (self.memory.read((self.PBR << 16) +self.PC) << 8) + addr
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = (self.memory.read((self.PBR << 16) +self.PC) << 16) + addr
        return addr

    def read_memory(self, address, byte_num, wrapp=False):
        address = address & 0xFFFFFF
        if byte_num == 1:
            byte0 = self.memory.read(address)
            return byte0
        elif byte_num == 2:
            byte0 = self.memory.read(address)
            if wrapp:
                byte1 = self.memory.read((address + 1) & 0xFFFF)
            else:
                byte1 = self.memory.read(address + 1)
            return byte0 + (byte1 << 8)
        elif byte_num == 3:
            byte0 = self.memory.read(address)
            if wrapp:
                byte1 = self.memory.read((address + 1) & 0xFFFF)
            else:
                byte1 = self.memory.read(address + 1)
            if wrapp:
                byte2 = self.memory.read((address + 2) & 0xFFFF)
            else:
                byte2 = self.memory.read(address + 2)
            return byte0 + (byte1 << 8) + (byte2 << 16)
        return -1

    def write_memory(self, address, value, byte_num, wrapp=False):
        address = address & 0xFFFFFF
        if byte_num == 1:
            self.memory.write(address, value & 0xFF)
        elif byte_num == 2:
            self.memory.write(address, value & 0xFF)
            if wrapp:
                self.memory.write((address + 1) & 0xFFFF, (value & 0xFF00) >> 8)
            else:
                self.memory.write(address + 1, (value & 0xFF00) >> 8)

    def push_stack(self, value):
        self.memory.write(self.SP, (value & 0xFF00) >> 8)
        self.stack.append((value & 0xFF00) >> 8)  # only for debugging
        self.SP = self.SP - 1
        self.memory.write(self.SP, value & 0x00FF)
        self.stack.append(value & 0x00FF)  # only for debugging
        self.SP = self.SP - 1
        #print("push16")
        #for i in range(self.SP, 0x2000):
        #    print(hex(i)+":"+str(self.memory.read(i)))
        #print("end push16")

    def push_stack_8bit(self, value):
        self.memory.write(self.SP, value & 0x00FF)
        self.stack.append(value& 0x00FF) # only for debugging
        self.SP = self.SP - 1
        #print("push8")
        #for i in range(self.SP, 0x2000):
        #    print(hex(i)+":"+str(self.memory.read(i)))
        #print("end push8")

    def pop_stack(self):
        self.SP = self.SP + 1
        low = self.memory.read(self.SP)
        self.stack.pop() # only for debugging
        self.SP = self.SP + 1
        high = self.memory.read(self.SP)
        self.stack.pop()  # only for debugging
        #print("pop16")
        #for i in range(self.SP, 0x2000):
        #    print(hex(i)+":"+str(self.memory.read(i)))
        #print("end pop16")
        return low + (high << 8)

    def pop_stack_8bit(self):
        self.SP = self.SP + 1
        byte = self.memory.read(self.SP)
        self.stack.pop()  # only for debugging
        #print("pop8")
        #for i in range(self.SP, 0x2000):
        #    print(hex(i)+":"+str(self.memory.read(i)))
        #print("end pop8")
        return byte

    def compute_NZflags(self, value, is8BitMode):
        if is8BitMode:
            if value & 0b10000000 != 0: # 8 Bit Mode
                self.setN()
            else:
                self.clearN()
            if value & 0x00FF == 0:
                self.setZ()
            else:
                self.clearZ()
        if not is8BitMode:
            if value & 0b1000000000000000 != 0: # 16 Bit Mode
                self.setN()
            else:
                self.clearN()
            if value & 0xFFFF == 0:
                self.setZ()
            else:
                self.clearZ()



    def w(self):
        if self.DP & 0x00FF != 0:
            return 1
        else:
            return 0

    def m(self):
        if self.isM():
            return 1
        else:
            return 0

    # TODO: what is old and new page in instructions like LDA? Remove 0x0 hack
    # 1 if page boundary is crossed, 0 otherwise
    def p(self, old_page=0x0, new_page=0x0):
        if not (old_page & 0x00FF00) == (new_page & 0x00FF00):
            return 1
        return 0

    def x(self):
        if self.isX():
            return 1
        else:
            return 0

    def c(self):
        if self.isC():
            return 1
        else:
            return 0

    # True = Negative
    # False = Positive
    def isN(self):
        return self.P & 0b10000000 != 0

    # True = Overflow
    # False = no Overflow
    def isV(self):
        return self.P & 0b01000000 != 0

    # True  = 8 Bit Accumulator and Memory
    # False = 16 Bit Accumulator and Memory
    def isM(self):
        return self.P & 0b00100000 != 0

    # True = X and Y 8 Bit
    # False = X and Y 16 Bit
    def isX(self):
        return self.P & 0b00010000 != 0

    # Break in Emulation-Mode
    def isB(self):
        return self.P & 0b00010000 != 0

    # True = BCD
    # False = 'normal' binary arithmetic
    def isD(self):
        return self.P & 0b00001000 != 0

    # IRQ Disbale = True (1)
    # IRQ Enable = False (0)
    def isI(self):
        return self.P & 0b00000100 != 0

    # True = zero
    # False = not zero
    def isZ(self):
        return self.P & 0b00000010 != 0

    # True = carry
    # False = no carry
    def isC(self):
        return self.P & 0b00000001 != 0

    # use if result was negative
    def setN(self):
        self.P = self.P | 0b10000000

    # use if overflow
    def setV(self):
        self.P = self.P | 0b01000000

    # switch to A 8 Bit
    def setM(self):
        self.P = self.P | 0b00100000

    # switch X/Y to 8 Bit
    def setX(self):
        self.P = self.P | 0b00010000

    # switch to BCD from 'normal' binary arithmetic
    def setD(self):
        self.P = self.P | 0b00001000

    # IRQ Disbale
    def setI(self):
        self.P = self.P | 0b00000100

    # use if computation was zero
    def setZ(self):
        self.P = self.P | 0b00000010

    # use if carry
    def setC(self):
        self.P = self.P | 0b00000001

    # use if result was positive
    def clearN(self):
        self.P = self.P & 0b01111111

    # use if no overflow
    def clearV(self):
        self.P = self.P & 0b10111111

    # switch to A 16 Bit
    def clearM(self):
        self.P = self.P & 0b11011111

    # switch X/Y to 16 Bit
    def clearX(self):
        self.P = self.P & 0b11101111

    # switch from BCD to 'normal' binary arithmetic
    def clearD(self):
        self.P = self.P & 0b11110111

    # IRQ enable
    def clearI(self):
        self.P = self.P & 0b11111011

    # clear zero
    def clearZ(self):
        self.P = self.P & 0b11111101

    # clear carry
    def clearC(self):
        self.P = self.P & 0b11111110
