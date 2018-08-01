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

    def execute(self, opcode):
        pass