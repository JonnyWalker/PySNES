# TODO: implement me
class DMAController(object):
    def __init__(self):
        self.registers = {}

    # called by the memory mapper
    def read(self, address):
        return self.registers[address]

    # called by the memory mapper
    def write(self, address, value):
        self.registers[address] = value


# TODO: implement me
class HDMAController(object):
    def __init__(self):
        self.registers = {}

    # called by the memory mapper
    def read(self, address):
        return self.registers[address]

    # called by the memory mapper
    def write(self, address, value):
        self.registers[address] = value