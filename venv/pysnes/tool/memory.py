from cartrige import CartrigeType
from exceptions import CanNotWriteROMExcpetion, IllegalAddressExcpetion


class MemoryMapper(object):
    def __init__(self, cartrige_type, RAM, ROM, SRAM, use_MAD1_mapping):
        self.cartrige_type = cartrige_type
        self.RAM  = RAM
        self.ROM  = ROM
        self.SRAM = SRAM
        self.use_MAD1_mapping = use_MAD1_mapping

    def read(self, address):
        bank = (address & 0xFF0000) >> 16
        offset = address & 0x00FFFF
        if self.cartrige_type == CartrigeType.LOROM:
            return self.read_LoROM(bank, offset)
        else:
            raise NotImplementedError()

    def read_LoROM(self, bank, offset):
        if   bank >= 0x00 and bank <= 0x3F:
            return self.read_system(bank, offset)
        elif bank >= 0x40 and bank <= 0x6F:
            return self.read_ROM(bank, offset)
        elif bank >= 0x70 and bank <= 0x7D:
            return self.read_SRAM_ROM(bank, offset)
        elif bank >= 0x7E and bank <= 0x7F:
            return self.read_RAM(bank, offset)
        elif bank >= 0x80 and bank <= 0xFF:
            raise NotImplementedError()
        else:
            raise IllegalAddressExcpetion()

    def read_system(self, bank, offset):
        if offset <= 0x7FFF:
            raise NotImplementedError()
        elif offset >= 0x8000:
            # read ROM
            ROM_bank = (bank) * 0x8000
            return self.ROM[ROM_bank + (offset-0x8000)]
        else:
            raise IllegalAddressExcpetion()

    def read_ROM(self, bank, offset):
        if offset <= 0x7FFF and not self.use_MAD1_mapping:
            # read ROM
            ROM_bank = 0x20000 + (bank-0x40) * 0xFFFF
            return self.ROM[ROM_bank + offset]
        elif offset >= 0x8000:
            # read ROM
            ROM_bank = 0x20000 + (bank-0x40) * 0xFFFF # TODO: maybe 0x10000 is correct
            return self.ROM[ROM_bank + offset]
        else:
            raise IllegalAddressExcpetion()

    # 0x70:0000 - 7D:FFFF reads the SRAM inside the cartirge or the ROM
    def read_SRAM_ROM(self, bank, offset):
        if offset >= 0x0000 and offset <= 0x7FFF:
            # read SRAM
            # TODO: if the SRAM is smaller than 32Kbyte it is repeated on and on (SRAM mirror)
            return self.SRAM[offset]
        elif offset >= 0x8000 and offset <= 0xFFFF:
            # read ROM from 38:XXXX in 32KB chunks
            ROM_bank = 0x380000 + (bank-0x70)*0x8000
            return self.ROM[ROM_bank + (offset-0x8000)]
        else:
            raise IllegalAddressExcpetion()

    # 0x7E:0000 - 0x7F:FFFF read the RAM inside the SNES
    def read_RAM(self, bank, offset):
        if bank == 0x7E:
            return self.RAM[offset]
        elif bank == 0x7F:
            return self.RAM[0x8000 + offset]
        else:
            raise IllegalAddressExcpetion()

    def write(self, address, value):
        bank   = (address & 0xFF0000) >> 16 # get first two bytes
        offset = address & 0x00FFFF
        if self.cartrige_type == CartrigeType.LOROM:
            self.write_LoROM(bank, offset, value)
        else:
            raise NotImplementedError()

    def write_LoROM(self, bank, offset, value):
        if   bank >= 0x00 and bank <= 0x3F:
            self.write_system(bank, offset, value)
        elif bank >= 0x40 and bank <= 0x6F:
            raise CanNotWriteROMExcpetion()
        elif bank >= 0x70 and bank <= 0x7D:
            self.write_SRAM_ROM(bank, offset, value)
        elif bank >= 0x7E and bank <= 0x7F:
            self.write_RAM(bank, offset, value)
        elif bank >= 0x80 and bank <= 0xFF:
            raise NotImplementedError()
        else:
            raise IllegalAddressExcpetion()

    def write_system(self, bank, offset, value):
        if offset <= 0x7FFF:
            raise NotImplementedError()
        elif offset >= 0x8000:
            # write ROM
            raise CanNotWriteROMExcpetion()
        else:
            raise IllegalAddressExcpetion()

    # 0x70:0000 - 7D:FFFF writes the SRAM inside the cartirge or the ROM
    def write_SRAM_ROM(self, bank, offset, value):
        if offset >= 0x0000 and offset <= 0x7FFF:
            # write SRAM
            # TODO: if the SRAM is smaller than 32Kbyte it is repeated on and on (SRAM mirror)
            self.SRAM[offset] = value
        elif offset >= 0x8000 and offset <= 0xFFFF:
            # write ROM
            raise CanNotWriteROMExcpetion()
        else:
            raise IllegalAddressExcpetion()

    # 0x7E:0000 - 0x7F:FFFF writes the RAM inside the SNES
    def write_RAM(self, bank, offset, value):
        if bank == 0x7E:
            self.RAM[offset] = value
        elif bank == 0x7F:
            self.RAM[0x8000 + offset] = value
        else:
            raise IllegalAddressExcpetion()

    def write_upper_mirror(self, bank, offset, value):
        raise NotImplementedError()