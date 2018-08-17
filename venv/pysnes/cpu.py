class CPU65816(object):
    def __init__(self, memory):
        self.A = 0   # Accumulator           - 8 or 16 Bit (also called A(8Bit) and B(next 8Bit))
        self.X = 0   # Index Register        - 8 or 16 Bit
        self.Y = 0   # Index Register        - 8 or 16 Bit
        self.SP = 0  # Stack Pointer         - 16 Bit
        self.DBR = 0 # Data Bank Register    - 8 Bit (also called B)
        self.DP = 0  # Direct Page Register  - 16 Bit (also called D)
        self.PBR = 0 # Program Bank Register - 8 Bit (also called K)
        self.P = 0   # Flag Register         - 8 Bit #TODO check if init ok
        self.PC = 0  # Program Counter       - 16 Bit
        self.memory = memory
        self.cycles = 0
        self.e = 1  # e-flag = 0 (native 16 Bit) e-flag = 1 (emulation 8 Bit)

    def run_code(self, code):
        while self.PC < len(code):
            self.fetch_decode_execute(code)

    def fetch_decode_execute(self, code):
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        opcode = code[(self.PBR << 16) +self.PC]
        # this meean every address > 0xFF will be wrapped. E.g. 0xFF +1 == 0x00
        # ADC #const
        # TODO: use BCD sub if D Flag is set
        if opcode == 0x69:
            const = self.fetch_byte(code)
            result = self.A + const
            self.compute_flags(result, self.isM())
            self.A = result
            if self.isC():
                self.A += 1
            self.cycles += 2
            self.PC = self.PC + 1
        # AND #const
        elif opcode == 0x29:
            const = self.fetch_byte(code)
            result = self.A & const
            self.compute_flags(result, self.isM())
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # ASL A
        elif opcode == 0x0A:
            self.A = self.A << 1
            self.cycles += 2
            self.PC = self.PC + 1
        # BCC nearlabel
        elif opcode == 0x90:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isC():
                if nearlabel & 0b10000000 == 0:
                    self.PC += nearlabel
                else:
                    self.PC = (self.PC - nearlabel) & 0xFFFF
            else:
                self.PC = self.PC + 1
        # BCS nearlabel
        elif opcode == 0xB0:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if self.isC():
                if nearlabel & 0b10000000 == 0:
                    self.PC += nearlabel
                else:
                    self.PC = (self.PC - nearlabel) & 0xFFFF
            else:
                self.PC = self.PC + 1
        # BEQ nearlabel
        elif opcode == 0xF0:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if self.isZ():
                if nearlabel & 0b10000000 == 0:
                    self.PC += nearlabel
                else:
                    self.PC = (self.PC - nearlabel) & 0xFFFF
            else:
                self.PC = self.PC + 1
        # BIT dp
        elif opcode == 0x24:
            if self.DP & 0b1000000000000000 != 0:
                self.setN()
            # use if second highest bit is set
            if self.DP & 0b0100000000000000 != 0:
                self.setV()
            if self.DP & self.A != 0:
                self.setZ()
            self.cycles += 3
            self.PC = self.PC + 1
        # BMI nearlabel
        elif opcode == 0x30:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if self.isN():
                if nearlabel & 0b10000000 == 0:
                    self.PC += nearlabel
                else:
                    self.PC = (self.PC - nearlabel) & 0xFFFF
            else:
                self.PC = self.PC + 1
        # BNE nearlabel
        elif opcode == 0xD0:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isZ():
                if nearlabel & 0b10000000 == 0:
                    self.PC += nearlabel
                else:
                    self.PC = (self.PC - nearlabel) & 0xFFFF
            else:
                self.PC = self.PC + 1
        # BPL nearlabel
        elif opcode == 0x10:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isN():
                if nearlabel & 0b10000000 == 0:
                    self.PC += nearlabel
                else:
                    self.PC = (self.PC - nearlabel) & 0xFFFF
            else:
                self.PC = self.PC + 1
        # BRA nearlabel
        elif opcode == 0x80:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if nearlabel & 0b10000000 == 0:
                self.PC += nearlabel
            else:
                self.PC = (self.PC - nearlabel) & 0xFFFF
         # BRL label
        elif opcode == 0x82:
            label = self.fetch_twobyte(code)
            self.cycles += 4
            self.PC += label
        # BVC nearlabel
        elif opcode == 0x50:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if self.isV():
                if nearlabel & 0b10000000 == 0:
                    self.PC += nearlabel
                else:
                    self.PC = (self.PC - nearlabel) & 0xFFFF
            else:
                self.PC = self.PC + 1
        # BVS nearlabel
        elif opcode == 0x70:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isV():
                if nearlabel & 0b10000000 == 0:
                    self.PC += nearlabel
                else:
                    self.PC = (self.PC - nearlabel) & 0xFFFF
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
        # CMP #const
        elif opcode == 0xC9:
            const = self.fetch_byte(code)
            result = self.A - const
            self.compute_flags(result, self.isM())
            if self.A >= const:
                self.setC()
            self.cycles += 2
            self.PC = self.PC + 1
        # CPX #const
        elif opcode == 0xE0:
            const = self.fetch_byte(code)
            result = self.X - const
            self.compute_flags(result, self.isM())
            if self.X >= const:
                self.setC()
            self.PC = self.PC + 1
        # CPY #const
        elif opcode == 0xC0:
            const = self.fetch_byte(code)
            result = self.Y - const
            self.compute_flags(result, self.isM())
            if self.Y >= const:
                self.setC()
            self.cycles += 2
            self.PC = self.PC + 1
        # DEC A
        elif opcode == 0x3A:
            result = self.sub_twos_complement(self.A, 1, is8BitMode = self.isM())
            self.compute_flags(result, self.isM())
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # DEC dp
        elif opcode == 0xC6:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP) # direct page wrapping
            mem_value = self.read_memory(wrapped_addr, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.sub_twos_complement(mem_value, 1, is8BitMode = self.isM())
            self.compute_flags(result, self.isM())
            self.write_memory(wrapped_addr, result, byte_num = 2 - self.m(), wrapp=True)  # zero bank wrapping!
            self.cycles += 7 - self.m()*2 + self.w()
            self.PC = self.PC + 1
        # DEC abs
        elif opcode == 0xCE:
            addr = self.fetch_twobyte(code) # no wrapping
            mem_value = self.read_memory((self.DBR << 16) + addr, byte_num = 2 - self.m()) # no wrapping
            result = self.sub_twos_complement(mem_value, 1, is8BitMode = self.isM())
            self.compute_flags(result, self.isM())
            self.write_memory((self.DBR << 16) + addr, result, byte_num = 2 - self.m()) # no wrapping
            self.cycles += 8 - self.m() * 2
            self.PC = self.PC + 1
        # DEC dp, X
        elif opcode == 0xD6:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP + self.X) # direct page wrapping
            mem_value = self.read_memory(wrapped_addr, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            result = self.sub_twos_complement(mem_value, 1, is8BitMode = self.isM())
            self.compute_flags(result, self.isM())
            self.write_memory(wrapped_addr, result, byte_num = 2 - self.m(), wrapp=True)  # zero bank wrapping!
            self.cycles += 8 - self.m() * 2 + self.w()
            self.PC = self.PC + 1
        # DEC abs, X
        elif opcode == 0xDE:
            addr = self.fetch_twobyte(code) # no wrapping
            mem_value = self.read_memory((self.DBR << 16) + (addr + self.X), byte_num = 2 - self.m())
            result = self.sub_twos_complement(mem_value, 1, is8BitMode=self.isM())
            self.compute_flags(result, self.isM())
            self.write_memory((self.DBR << 16) + (addr + self.X), result, byte_num = 2 - self.m())
            self.cycles += 9 - self.m() * 2
            self.PC = self.PC + 1
        # DEX
        elif opcode == 0xCA:
            result = self.sub_twos_complement(self.X, 1, is8BitMode = self.isX())
            self.compute_flags(result, self.isX())
            self.X = result
            self.cycles += 2
            self.PC = self.PC + 1
        # DEY
        elif opcode == 0x88:
            result = self.sub_twos_complement(self.Y, 1, is8BitMode = self.isX())
            self.compute_flags(result, self.isX())
            self.Y = result
            self.cycles += 2
            self.PC = self.PC + 1
        # EOR #const
        elif opcode == 0x49:
            const = self.fetch_byte(code)
            result = self.A ^ const
            self.compute_flags(result, self.isM())
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # INC A
        elif opcode == 0x1A:
            result = self.A + 1
            self.compute_flags(result, self.isM())
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # JMP addr
        elif opcode == 0x4C:
            label = self.fetch_twobyte(code)
            self.cycles += 3
            self.PC = label
        # LDA (dp, X)
        elif opcode == 0xA1:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP + self.X) & 0xFFFF
                addr2 = self.read_memory(wrapped_addr, byte_num=2, wrapp=True)
                value = self.read_memory((self.DBR << 16) + addr2, byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 7 - self.m() + self.w()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP + self.X) & 0xFFFF
                addr2 = self.read_memory(wrapped_addr, byte_num=2, wrapp=True)
                value = self.read_memory((self.DBR << 16) + addr2, byte_num=2)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 7 - self.m() + self.w()
                self.PC = self.PC + 1
        # LDA stk, S
        elif opcode == 0xA3:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.SP) & 0xFFFF
                value = self.read_memory(wrapped_addr, byte_num=1, wrapp=True) # zero bank wrapping
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 5 - self.m()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.SP) & 0xFFFF
                value = self.read_memory(wrapped_addr, byte_num=2, wrapp=True) # zero bank wrapping
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 5 - self.m()
                self.PC = self.PC + 1
        # LDA dp
        elif opcode == 0xA5:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF # direct page wrapping
                value = self.read_memory(wrapped_addr, byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 4 - self.m() + self.w()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF  # direct page wrapping
                value = self.read_memory(wrapped_addr, byte_num=2, wrapp=True) # zero bank wrapping!
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 4 - self.m() + self.w()
                self.PC = self.PC + 1
        # LDA [dp]
        elif opcode == 0xA7:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF  # direct page wrapping
                addr2 = self.read_memory(wrapped_addr, byte_num=3, wrapp=True) # zero bank wrapping!
                value = self.read_memory(addr2, byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 7 - self.m() + self.w()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF  # direct page wrapping
                addr2 = self.read_memory(wrapped_addr, byte_num=3, wrapp=True) # zero bank wrapping!
                value = self.read_memory(addr2, byte_num=2)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 7 - self.m() + self.w()
                self.PC = self.PC + 1
        # LDA #const
        elif opcode == 0xA9:
            if self.isM(): # 8 Bit A/M
                const = self.fetch_byte(code) # M=1 -> 8 Bit A -> one byte
                result = const
                self.compute_flags(result, self.isM())
                self.A = result
                self.cycles += 3 - self.m()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                const = self.fetch_twobyte(code) # M=0 -> 16 Bit A -> two byte
                result = const
                self.compute_flags(result, self.isM())
                self.A = result
                self.cycles += 3 - self.m()
                self.PC = self.PC + 1
        # LDA abs
        elif opcode == 0xAD:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_twobyte(code) # no wrapping
                value = self.read_memory((self.DBR << 16) + addr, byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 5 - self.m()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_twobyte(code) # no wrapping
                value = self.read_memory((self.DBR << 16) + addr, byte_num=2)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 5 - self.m()
                self.PC = self.PC + 1
        # LDA long
        elif opcode == 0xAF:
            addr = self.fetch_threebyte(code)
            if self.isM(): # 8 Bit A/M
                value = self.read_memory(addr, byte_num=1) # no wrapping
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m()
            else: # 16 Bit A/M
                value = self.read_memory(addr, byte_num=2) # no wrapping
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # LDA (dp), Y
        elif opcode == 0xB1:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF
                addr2 = self.read_memory(wrapped_addr, byte_num=2, wrapp=True)
                value = self.read_memory((self.DBR << 16) + addr2 + self.Y, byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 7 - self.m() + self.w() - self.x() + self.x() * self.p()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF
                addr2 = self.read_memory(wrapped_addr, byte_num=2, wrapp=True)
                value = self.read_memory((self.DBR << 16) + addr2 + self.Y, byte_num=2)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 7 - self.m() + self.w() - self.x() + self.x() * self.p()
                self.PC = self.PC + 1
        # LDA (dp)
        elif opcode == 0xB2:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF
                addr2 = self.read_memory(wrapped_addr, byte_num=2, wrapp=True)
                value = self.read_memory((self.DBR << 16) + addr2, byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m() + self.w()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF
                addr2 = self.read_memory(wrapped_addr, byte_num=2, wrapp=True)
                value = self.read_memory((self.DBR << 16) + addr2, byte_num=2)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m() + self.w()
                self.PC = self.PC + 1
        # LDA (stk, S), Y #TODO:  & 0xFFFF
        elif opcode == 0xB3:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_byte(code)
                addr2 = self.read_memory((addr + self.SP) & 0xFFFF, byte_num=2)
                wrapped_addr = (addr2 + self.Y) & 0XFFFF
                value = self.read_memory((self.DBR << 16) + wrapped_addr, byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 8 - self.m()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_byte(code)
                addr2 = self.read_memory((addr + self.SP) & 0xFFFF, byte_num=2)
                wrapped_addr = (addr2 + self.Y) & 0XFFFF
                value = self.read_memory((self.DBR << 16) + wrapped_addr, byte_num=2)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 8 - self.m()
                self.PC = self.PC + 1
        # LDA dp, X
        elif opcode == 0xB5:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP + self.X) & 0xFFFF
                value = self.read_memory(wrapped_addr, byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 5 - self.m() + self.w()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP + self.X) & 0xFFFF
                value = self.read_memory(wrapped_addr,  byte_num=2, wrapp=True) # zero bank wrapping!
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 5 - self.m() + self.w()
                self.PC = self.PC + 1
        # LDA [dp], Y
        elif opcode == 0xB7:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF
                addr2 = self.read_memory(wrapped_addr, byte_num=3, wrapp=True)
                value = self.read_memory(addr2 + self.Y, byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 7 - self.m() + self.w()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_byte(code)
                wrapped_addr = (addr + self.DP) & 0xFFFF
                addr2 = self.read_memory(wrapped_addr, byte_num=3, wrapp=True)
                value = self.read_memory(addr2 + self.Y, byte_num=2)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 7 - self.m() + self.w()
                self.PC = self.PC + 1
        # LDA abs, Y
        elif opcode == 0xB9:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_twobyte(code) # no wrapping
                value = self.read_memory((self.DBR << 16) + addr + self.Y,  byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_twobyte(code) # no wrapping
                value = self.read_memory((self.DBR << 16) + addr + self.Y,  byte_num=2)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
        # LDA abs, X
        elif opcode == 0xBD:
            if self.isM(): # 8 Bit A/M
                addr = self.fetch_twobyte(code) # no wrapping
                value = self.read_memory((self.DBR << 16) + (addr + self.X), byte_num=1)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
                self.PC = self.PC + 1
            else: # 16 Bit A/M
                addr = self.fetch_twobyte(code) # no wrapping
                value = self.read_memory((self.DBR << 16) + (addr + self.X), byte_num=2)
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m() - self.x() + self.x() * self.p()
                self.PC = self.PC + 1
        # LDA long, X
        elif opcode == 0xBF:
            addr = self.fetch_threebyte(code)
            if self.isM(): # 8 Bit A/M
                value = self.read_memory(addr + self.X, byte_num=1) # no wrapping
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m()
            else: # 16 Bit A/M
                value = self.read_memory(addr + self.X, byte_num=2) # no wrapping
                self.compute_flags(value, self.isM())
                self.A = value
                self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # LDX #const
        elif opcode == 0xA2:
            const = self.fetch_byte(code)
            result = const
            self.compute_flags(result, self.isM())
            self.X = result
            self.cycles += 2
            self.PC = self.PC + 1
        # LDY #const
        elif opcode == 0xA0:
            const = self.fetch_byte(code)
            result = const
            self.compute_flags(result, self.isM())
            self.Y = result
            self.cycles += 2
            self.PC = self.PC + 1
        # LSR A
        elif opcode == 0x4A:
            result = self.A >> 1
            self.compute_flags(result, self.isM())
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
        # ORA #const
        elif opcode == 0x09:
            const = self.fetch_byte(code)
            result = self.A | const
            self.compute_flags(result, self.isM())
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # PHA
        elif opcode == 0x48:
            self.push_stack(self.A)
            self.cycles += 3
            self.PC = self.PC + 1
        # PLA
        elif opcode == 0x68:
            self.A = self.pop_stack()
            self.cycles += 3
            self.PC = self.PC + 1
        # REP
        elif opcode == 0xC2:
            const = self.fetch_byte(code)
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
            self.compute_flags(result, self.isM())
            if self.A & 0b10000000 != 0:
                self.setC()
            else:
                self.clearC()
            self.A = result
        # ROR A
        elif opcode == 0x6A:
            result = self.A >> 1
            if self.isC():
                result = result & 0b1111111111111111
            else:
                result = result & 0b0111111111111111
            self.compute_flags(result, self.isM())
            if self.A & 0b00000001 != 0:
                self.setC()
            else:
                self.clearC()
            self.A = result
        # TODO: use BCD sub if D Flag is set
        # SBC #const #TODO: v and c
        elif opcode == 0xE9:
            const = self.fetch_byte(code)
            result = self.A - const - 1
            self.compute_flags(result, self.isM())
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
            const = self.fetch_byte(code)
            self.P = self.P | const;
            self.cycles += 3
            self.PC = self.PC + 1
        # STA (dp, X)
        elif opcode == 0x81:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP + self.X)
            addr2 = self.read_memory(wrapped_addr, byte_num=2, wrapp=True)
            self.write_memory((self.DBR << 16) + addr2, self.A, byte_num = 2 - self.m())
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA stk, S
        elif opcode == 0x83:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.SP)
            self.write_memory(wrapped_addr, self.A, byte_num = 2 - self.m(), wrapp=True) # ISSUE #38
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # STA dp
        elif opcode == 0x85:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP)  # direct page wrapping
            self.write_memory(wrapped_addr, self.A, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA [dp]
        elif opcode == 0x87:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP)  # direct page wrapping
            addr2 = self.read_memory(wrapped_addr, byte_num=3, wrapp=True) # zero bank wrapping!
            self.write_memory(addr2, self.A, byte_num = 2 - self.m())
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA abs
        elif opcode == 0x8D:
            addr = self.fetch_twobyte(code) # no wrapping
            self.write_memory((self.DBR << 16) + addr, self.A, byte_num = 2 - self.m())
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # STA long
        elif opcode == 0x8F:
            addr = self.fetch_threebyte(code)
            self.write_memory(addr, self.A, byte_num = 2 - self.m()) # no wrapping
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # STA (dp), Y
        elif opcode == 0x91:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP)
            addr2 = self.read_memory(wrapped_addr, byte_num=2, wrapp=True)
            self.write_memory((self.DBR << 16) + addr2 + self.Y, self.A, byte_num = 2 - self.m())
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA (dp)
        elif opcode == 0x92:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP)
            addr2 = self.read_memory(wrapped_addr, byte_num=2, wrapp=True)
            self.write_memory((self.DBR << 16) + addr2, self.A,  byte_num = 2 - self.m())
            self.cycles += 6 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA (stk, S), Y
        elif opcode == 0x93:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.SP)
            addr2 = self.read_memory(wrapped_addr, byte_num=2)
            wrapped_addr = self.compute_wrapped_addr(addr2 + self.Y)
            self.write_memory((self.DBR << 16) + wrapped_addr, self.A, byte_num = 2 - self.m())
            self.cycles += 8 - self.m()
            self.PC = self.PC + 1
        # STA dp, X
        elif opcode == 0x95:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP + self.X)
            self.write_memory(wrapped_addr, self.A, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 5 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA [dp], Y
        elif opcode == 0x97:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP)
            addr2 = self.read_memory(wrapped_addr, byte_num=3, wrapp=True)
            self.write_memory(addr2 + self.Y, self.A, byte_num = 2 - self.m())
            self.cycles += 7 - self.m() + self.w()
            self.PC = self.PC + 1
        # STA abs, Y
        elif opcode == 0x99:
            addr = self.fetch_twobyte(code) # no wrapping
            self.write_memory((self.DBR << 16) + addr + self.Y, self.A,  byte_num = 2 - self.m())
            self.cycles += 6 - self.m()
        # STA abs, X
        elif opcode == 0x9D:
            addr = self.fetch_twobyte(code) # no wrapping
            self.write_memory((self.DBR << 16) + addr + self.X, self.A,  byte_num = 2 - self.m())
            self.cycles += 6 - self.m()
        # STA long, X
        elif opcode == 0x9F:
            addr = self.fetch_threebyte(code)
            self.write_memory(addr + self.X, self.A, byte_num = 2 - self.m()) # no wrapping
            self.cycles += 6 - self.m()
            self.PC = self.PC + 1
        # STX dp
        elif opcode == 0x86:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP)  # direct page wrapping
            self.write_memory(wrapped_addr, self.X, byte_num = 2 - self.x(), wrapp=True) # zero bank wrapping!
            self.cycles += 4 - self.x() + self.w()
            self.PC = self.PC + 1
        # STX abs
        elif opcode == 0x8E:
            addr = self.fetch_twobyte(code) # no wrapping
            self.write_memory((self.DBR << 16) + addr, self.X, byte_num = 2 - self.x())
            self.cycles += 5 - self.x()
            self.PC = self.PC + 1
        # STX dp, Y
        elif opcode == 0x96:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP + self.Y)
            self.write_memory(wrapped_addr, self.X, byte_num = 2 - self.x(), wrapp=True) # zero bank wrapping!
            self.cycles += 5 - self.x() + self.w()
            self.PC = self.PC + 1
        # STY dp
        elif opcode == 0x84:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP) # direct page wrapping
            self.write_memory(wrapped_addr, self.Y, byte_num = 2 - self.x(), wrapp=True) # zero bank wrapping!
            self.cycles += 4 - self.x() + self.w()
            self.PC = self.PC + 1
        # STY abs
        elif opcode == 0x8C:
            addr = self.fetch_twobyte(code) # no wrapping
            self.write_memory((self.DBR << 16) + addr, self.Y, byte_num = 2 - self.x())
            self.cycles += 5 - self.x()
            self.PC = self.PC + 1
        # STY dp, X
        elif opcode == 0x94:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP + self.X)
            self.write_memory(wrapped_addr, self.Y, byte_num = 2 - self.x(), wrapp=True) # zero bank wrapping!
            self.cycles += 5 - self.x() + self.w()
            self.PC = self.PC + 1
        # STZ dp
        elif opcode == 0x64:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP) # direct page wrapping
            self.write_memory(wrapped_addr, 0x00, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 4 - self.m() + self.w()
            self.PC = self.PC + 1
        # STZ dp, X
        elif opcode == 0x74:
            addr = self.fetch_byte(code)
            wrapped_addr = self.compute_wrapped_addr(addr + self.DP + self.X)
            self.write_memory(wrapped_addr, 0x00, byte_num = 2 - self.m(), wrapp=True) # zero bank wrapping!
            self.cycles += 5 - self.m() + self.w()
            self.PC = self.PC + 1
        # STZ abs
        elif opcode == 0x9C:
            addr = self.fetch_twobyte(code)  # no wrapping
            self.write_memory((self.DBR << 16) + addr, 0x00, byte_num=2 - self.m())
            self.cycles += 5 - self.m()
            self.PC = self.PC + 1
        # STZ abs, X
        elif opcode == 0x9E:
            addr = self.fetch_twobyte(code) # no wrapping
            self.write_memory((self.DBR << 16) + addr + self.X, 0x00,  byte_num = 2 - self.m())
            self.cycles += 6 - self.m()
        # TAX
        elif opcode == 0x78:
            self.compute_flags(self.A, self.isM())
            self.X = self.A
            self.cycles += 2
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
            print("unkown opcode:", opcode)
            raise NotImplementedError()


    # compute twos complement by hand.
    def sub_twos_complement(self, value, arg, is8BitMode):
        if value - arg < 0:
            if is8BitMode:
                result = 0xFF - arg + 1
            else:
                result = 0xFFFF - arg + 1
        else:
            result = value - arg
        return result


    # some addresses are wrapped at the bank XX boundery (64 KB - 16 Bit addr)
    # so if you read two bytes from XXFFFF the second byte will be read
    # from XX0000 and not from X100000!
    # There are mixed address modes. For example the computation of an
    # address pointer using dp register is wrapped
    # while the address itself can cross bank bounderys.
    # Direct page (dp register) and stack pointer are wrapped at the zero bank.
    # Most likely there are bugs in wrapping implementations.
    def compute_wrapped_addr(self, addr):
        return addr & 0x00FFFF

    def fetch_byte(self, code):
        # TODO: use PBR
        self.PC = self.PC + 1
        return code[self.PC]

    # little endian
    def fetch_twobyte(self, code):
        # TODO: use PBR
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = code[self.PC]
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = addr + (code[self.PC] << 8)
        return addr

    # little endian
    def fetch_threebyte(self, code):
        # TODO: use PBR
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = code[self.PC]
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = addr + (code[self.PC] << 8)
        self.PC = self.PC + 1
        # PC wrapping: if PC = 0xFFFF then PC + 1 = 0x0000
        self.PC = self.PC & 0xFFFF
        addr = addr + (code[self.PC] << 16)
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
        self.memory.write(self.SP, value & 0x00FF)
        self.SP = self.SP - 1
        self.memory.write(self.SP, (value & 0xFF00) >> 8)
        self.SP = self.SP - 1

    def pop_stack(self):
        low = self.memory.read(self.SP)
        self.SP = self.SP + 1
        high = self.memory.read(self.SP)
        self.SP = self.SP + 1
        return low + (high << 88)

    def compute_flags(self, value, is8BitMode):
        if value == 0:
            self.setZ()
        if is8BitMode and value & 0b10000000 != 0: # 8 Bit Mode
            self.setN()
        if not is8BitMode and value & 0b1000000000000000 != 0: # 16 Bit Mode
            self.setN()

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

    # TODO: 1 if page boundary is crossed, 0 otherwise
    def p(self):
        return 0

    def x(self):
        if self.isX():
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

    # True = Emulation on (8 Bit Mode) Accumulator and Memory
    # False = Emulation off (16 Bit Mode) Accumulator and Memory
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

    # switch to A 16 Bit
    def setM(self):
        self.P = self.P | 0b00100000

    # switch X/Y to 16 Bit
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

    # switch to A 8 Bit
    def clearM(self):
        self.P = self.P & 0b11011111

    # switch X/Y to 8 Bit
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
