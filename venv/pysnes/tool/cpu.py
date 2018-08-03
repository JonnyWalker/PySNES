class CPU65816(object):
    def __init__(self):
        self.A = 0   # Accumulator
        self.X = 0   # Index Register
        self.Y = 0   # Index Register
        self.SP = 0  # Stack Pointer
        self.DBR = 0 # Data Bank Register
        self.DP = 0  # Direct Page Register
        self.PBR = 0 # Program Bank Register
        self.P = 0   # Flag Register
        self.PC = 0  # Program Counter

        self.cycles = 0

    def fetch_decode_execute(self, code):
        opcode = code[self.PC]
        # TODO: cycles are longer e.g. if M
        # TODO: ignore Emulation mode for now...fix this some day
        # ADC #const
        if opcode == 0x69:
            const = self.fetch_byte(code)
            self.A = self.A + const
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
                self.PC = nearlabel
            else:
                self.PC = self.PC + 1
        # BCS nearlabel
        elif opcode == 0xB0:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if self.isC():
                self.PC = nearlabel
            else:
                self.PC = self.PC + 1
        # BEQ nearlabel
        elif opcode == 0xF0:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if self.isZ():
                self.PC = nearlabel
            else:
                self.PC = self.PC + 1
        # BIT dp
        elif opcode == 0x24:
            if self.DP & 0b10000000 != 0:
                self.setN()
            # use if second highest bit is set
            if self.DP & 0b01000000 != 0:
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
                self.PC = nearlabel # TODO: maybe self.PC += nearlabel is correct in all cases ...
            else:
                self.PC = self.PC + 1
        # BNE nearlabel
        elif opcode == 0xD0:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isZ():
                self.PC = nearlabel
            else:
                self.PC = self.PC + 1
        # BPL nearlabel
        elif opcode == 0x10:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isN():
                self.PC = nearlabel
            else:
                self.PC = self.PC + 1
        # BRA nearlabel
        elif opcode == 0x80:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            self.PC = nearlabel
         # BRL label
        elif opcode == 0x82:
            label = self.fetch_twobyte(code)
            self.cycles += 4
            self.PC = label
        # BVC nearlabel
        elif opcode == 0x50:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if self.isV():
                self.PC = nearlabel
            else:
                self.PC = self.PC + 1
        # BVS nearlabel
        elif opcode == 0x70:
            nearlabel = self.fetch_byte(code)
            self.cycles += 2
            if not self.isV():
                self.PC = nearlabel
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

    def fetch_byte(self, code):
        self.PC = self.PC + 1
        return code[self.PC]


    def fetch_twobyte(self, code):
        self.PC = self.PC + 1
        addr = code[self.PC]
        self.PC = self.PC + 1
        addr = addr + (code[self.PC] << 8)
        return addr

    def compute_flags(self, value):
        if value == 0:
            self.setZ()
        if value & 0b10000000 != 0:
            self.setN()

    # True = Negative
    # False = Positive
    def isN(self):
        return self.P & 0b10000000 != 0

    # True = Overflow
    # False = no Overflow
    def isV(self):
        return self.P & 0b01000000 != 0

    # True = Emulation on (8 Bit Mode)
    # False = Emulation off (16 Bit Mode)
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

    # IRQ enable?
    def clearI(self):
        self.P = self.P & 0b11111011

    # clear zero
    def clearZ(self):
        self.P = self.P & 0b11111101

    # clear carry
    def clearC(self):
        self.P = self.P & 0b11111110
