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
            self.A = self.A & const
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



    def fetch_byte(self, code):
        self.PC = self.PC + 1
        return code[self.PC]

    # True = Emulation on (8 Bit Mode)
    # False = Emulation off (16 Bit Mode)
    def isM(self):
        return self.P & 0b00100000 != 0

    # True = use binary arithmetic
    # False = use BCD
    def isD(self):
        return self.P & 0b00001000 != 0

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


    # if overflow
    def setV(self):
        self.P = self.P | 0b01000000

    # use if result was zero
    def setZ(self):
        self.P = self.P | 0b00000010
