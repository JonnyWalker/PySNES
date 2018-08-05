# TODO: the CPU is a 5A22 which is a superset of the 65816
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
        self.e = 1  # e-flag = 0 (native) e-lfag = 1 (emulation)

    def run_code(self, code):
        while self.PC < len(code):
            self.fetch_decode_execute(code)

    def fetch_decode_execute(self, code):
        # TODO: use PBR
        opcode = code[self.PC]
        # TODO: cycles are longer e.g. if M
        # TODO: ignore Emulation mode for now...fix this some day
        # ADC #const
        print("iam:"+hex(opcode))
        if opcode == 0x69:
            const = self.fetch_byte(code)
            result = self.A + const
            self.compute_flags(result)
            self.A = result
            if self.isC():
                self.A += 1
            self.cycles += 2
            self.PC = self.PC + 1
        # AND #const
        elif opcode == 0x29:
            const = self.fetch_byte(code)
            result = self.A & const
            self.compute_flags(result)
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
                self.PC += nearlabel
            else:
                self.PC = self.PC + 1
        # BCS nearlabel
        elif opcode == 0xB0:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if self.isC():
                self.PC += nearlabel
            else:
                self.PC = self.PC + 1
        # BEQ nearlabel
        elif opcode == 0xF0:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if self.isZ():
                self.PC += nearlabel
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
                self.PC += nearlabel
            else:
                self.PC = self.PC + 1
        # BNE nearlabel
        elif opcode == 0xD0:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isZ():
                self.PC += nearlabel
            else:
                self.PC = self.PC + 1
        # BPL nearlabel
        elif opcode == 0x10:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isN():
                self.PC += nearlabel
            else:
                self.PC = self.PC + 1
        # BRA nearlabel
        elif opcode == 0x80:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            self.PC += nearlabel
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
                self.PC += nearlabel
            else:
                self.PC = self.PC + 1
        # BVS nearlabel
        elif opcode == 0x70:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isV():
                self.PC += nearlabel
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
            self.compute_flags(result)
            if self.A >= const:
                self.setC()
            self.cycles += 2
            self.PC = self.PC + 1
        # CPX #const
        elif opcode == 0xE0:
            const = self.fetch_byte(code)
            result = self.X - const
            self.compute_flags(result)
            if self.X >= const:
                self.setC()
            self.PC = self.PC + 1
        # CPY #const
        elif opcode == 0xC0:
            const = self.fetch_byte(code)
            result = self.Y - const
            self.compute_flags(result)
            if self.Y >= const:
                self.setC()
            self.cycles += 2
            self.PC = self.PC + 1
        # DEC A
        elif opcode == 0x3A:
            result = self.A -1
            self.compute_flags(result)
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # DEX
        elif opcode == 0xCA:
            result = self.X -1
            self.compute_flags(result)
            self.X = result
            self.cycles += 2
            self.PC = self.PC + 1
        # DEY
        elif opcode == 0x88:
            result = self.Y -1
            self.compute_flags(result)
            self.Y = result
            self.cycles += 2
            self.PC = self.PC + 1
        # EOR #const
        elif opcode == 0x49:
            const = self.fetch_byte(code)
            result = self.A ^ const
            self.compute_flags(result)
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # INC A
        elif opcode == 0x1A:
            result = self.A + 1
            self.compute_flags(result)
            self.A = result
            self.cycles += 2
            self.PC = self.PC + 1
        # JMP addr
        elif opcode == 0x4C:
            label = self.fetch_twobyte(code)
            self.cycles += 3
            self.PC = label
        # LDA dp
        elif opcode == 0xA5:
            if self.isM():
                addr = self.fetch_byte(code)
                value = self.read_momory(addr + self.DP)
                self.compute_flags(value)
                self.A = value
                self.cycles += 4 - self.m() + self.w()
                self.PC = self.PC + 1
            else:
                addr = self.fetch_byte(code)
                value = self.read_momory(addr + self.DP)
                self.compute_flags(value)
                self.A = value
                self.cycles += 4 - self.m() + self.w()
                self.PC = self.PC + 1
        # LDA #const
        elif opcode == 0xA9:
            if self.isM():
                const = self.fetch_byte(code)
                result = const
                self.compute_flags(result)
                self.A = result
                self.cycles += 3 - self.m()
                self.PC = self.PC + 1
            else:
                const = self.fetch_twobyte(code)
                result = const
                self.compute_flags(result)
                self.A = result
                self.cycles += 3 - self.m()
                self.PC = self.PC + 1
        # LDA abs
        elif opcode == 0xAD:
            if self.isM():
                addr = self.fetch_twobyte(code)
                value = self.read_momory((self.DBR << 16) + addr)
                self.compute_flags(value)
                self.A = value
                self.cycles += 5 - self.m()
                self.PC = self.PC + 1
            else:
                addr = self.fetch_twobyte(code)
                value = self.read_momory((self.DBR << 16) + addr)
                self.compute_flags(value)
                self.A = value
                self.cycles += 5 - self.m()
                self.PC = self.PC + 1
        # LDA long
        elif opcode == 0xAF:
            addr = self.fetch_threebyte(code)
            value = self.read_momory(addr)
            self.compute_flags(value)
            self.A = value
            if self.isM():
                self.cycles += 5
            else:
                self.cycles += 6
            self.PC = self.PC + 1
        # LDA (dp), Y
        elif opcode == 0xB1:
            if self.isM():
                addr = self.fetch_byte(code)
                addr2 = self.read_momory(addr + self.DP)
                value = self.read_momory((self.DBR << 16) + addr2)
                self.compute_flags(value)
                self.A = value
                self.cycles += 4 - self.m() + self.w() - self.x() + self.x() * self.p()
                self.PC = self.PC + 1
            else:
                addr = self.fetch_byte(code)
                addr2 = self.read_momory(addr + self.DP)
                value = self.read_momory((self.DBR << 16) + addr2 + self.Y)
                self.compute_flags(value)
                self.A = value
                self.cycles += 4 - self.m() + self.w()  - self.x() + self.x() * self.p()
                self.PC = self.PC + 1
        # LDX #const
        elif opcode == 0xA2:
            const = self.fetch_byte(code)
            result = const
            self.compute_flags(result)
            self.X = result
            self.cycles += 2
            self.PC = self.PC + 1
        # LDY #const
        elif opcode == 0xA0:
            const = self.fetch_byte(code)
            result = const
            self.compute_flags(result)
            self.Y = result
            self.cycles += 2
            self.PC = self.PC + 1
        # LSR A
        elif opcode == 0x4A:
            result = self.A >> 1
            self.compute_flags(result)
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
            self.compute_flags(result)
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
            self.cycles += 3
            self.PC = self.PC + 1
        # ROL A
        elif opcode == 0x2A:
            result = self.A << 1
            if self.isC():
                result = result & 0b1111111111111111
            else:
                result = result & 0b1111111111111110
            self.compute_flags(result)
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
            self.compute_flags(result)
            if self.A & 0b00000001 != 0:
                self.setC()
            else:
                self.clearC()
            self.A = result
        # SBC #const #TODO: v and c
        elif opcode == 0xE9:
            const = self.fetch_byte(code)
            result = self.A - const - 1
            self.compute_flags(result)
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
        # TAX
        elif opcode == 0x78:
            self.compute_flags(self.A)
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
            if self.e == 1:
                self.setM()
                self.setX()
                self.X = self.X & 0x00FF
                self.Y = self.Y & 0x00FF
            self.cycles += 2
            self.PC = self.PC + 1
        else:
            print("unkown opcode:", opcode)
            raise NotImplementedError()

    def fetch_byte(self, code):
        # TODO: use PBR
        self.PC = self.PC + 1
        return code[self.PC]

    # little endian
    def fetch_twobyte(self, code):
        # TODO: use PBR
        self.PC = self.PC + 1
        addr = code[self.PC]
        self.PC = self.PC + 1
        addr = addr + (code[self.PC] << 8)
        return addr

    # little endian
    def fetch_threebyte(self, code):
        # TODO: use PBR
        self.PC = self.PC + 1
        addr = code[self.PC]
        self.PC = self.PC + 1
        addr = addr + (code[self.PC] << 8)
        self.PC = self.PC + 1
        addr = addr + (code[self.PC] << 16)
        return addr

    def read_momory(self, addr):
        if self.isM(): # 8 Bit
            return self.memory.read(addr)
        else:
            byte0 = self.memory.read(addr)
            byte1 = self.memory.read(addr+1)
            return byte0 + (byte1 << 8)

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

    def compute_flags(self, value):
        if value == 0:
            self.setZ()
        if self.isM() and value & 0b10000000 != 0: # 8 Bit Mode
            self.setN()
        if not self.isM() and value & 0b1000000000000000 != 0: # 16 Bit Mode
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
    # or Break in Emulation-Mode
    def isX(self):
        return self.P & 0b00010000 != 0

    # True = use binary arithmetic
    # False = use BCD
    def isD(self):
        return self.P & 0b00001000 != 0

    # IRQ Disbale?
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

    # switch to BCD encodeing?
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

    # switch from BCD encoding?
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
