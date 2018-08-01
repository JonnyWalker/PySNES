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
        # ADC #const
        if opcode == 0x69:
            const = self.fetch_byte(code)
            self.A = self.A + const
            if self.isC():
                self.A += 1
            self.cycles += 2
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

    # True = carry
    # False = no carry
    def isC(self):
        return self.P & 0b00000001 != 0
