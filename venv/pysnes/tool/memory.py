from cartrige import CartrigeType
from exceptions import CanNotWriteROMExcpetion, IllegalAddressExcpetion

# When the CPU puts a signal on its address bus some bytes can be
# read or written "somewhere" (e.g. ROM, RAM, SRAM or other)
# The Cartirgetype (e.g. LoROM, HiROM, ...) determines what has been addressed.
# This module implements this memory mapping
class MemoryMapper(object):
    def __init__(self, cartrige_type, RAM, ROM, SRAM, use_MAD1_mapping, SRAM_size):
        if cartrige_type == CartrigeType.LOROM:
            self.mapper = LoROMMemoryMapper(RAM, ROM, SRAM, use_MAD1_mapping, SRAM_size)
        else:
            raise NotImplementedError()

    def read(self, address):
        bank = (address & 0xFF0000) >> 16 # get first two bytes
        offset = address & 0x00FFFF
        return self.mapper.read(bank, offset)

    def write(self, address, value):
        bank = (address & 0xFF0000) >> 16 # get first two bytes
        offset = address & 0x00FFFF
        self.mapper.write(bank, offset, value)


class LoROMMemoryMapper(object):
    def __init__(self, RAM, ROM, SRAM, use_MAD1_mapping, SRAM_size):
        self.RAM  = RAM
        self.ROM  = ROM
        self.SRAM = SRAM
        self.use_MAD1_mapping = use_MAD1_mapping
        self.SRAM_size = SRAM_size

    def read(self, bank, offset):
        if   bank >= 0x00 and bank <= 0x3F:
            return self.read_system(bank, offset)
        elif bank >= 0x40 and bank <= 0x6F:
            return self.read_ROM(bank, offset)
        elif bank >= 0x70 and bank <= 0x7D:
            return self.read_SRAM_ROM(bank, offset)
        elif bank >= 0x7E and bank <= 0x7F:
            return self.read_RAM(bank, offset)
        elif bank >= 0x80 and bank <= 0xFF:
            return self.read_upper_mirror(bank, offset)
        else:
            raise IllegalAddressExcpetion()

    # 0x00:0000 - 3F:FFFF read ROM and system stuff
    def read_system(self, bank, offset):
        if offset <= 0x7FFF:
            raise NotImplementedError()
        elif offset >= 0x8000:
            # read ROM
            ROM_bank = (bank) * 0x8000
            return self.ROM[ROM_bank + (offset-0x8000)]
        else:
            raise IllegalAddressExcpetion()

    # 0x40:0000 - 6F:FFFF read ROM (only 32 KB in 64KB, the other half is "maybe" mirrored)
    def read_ROM(self, bank, offset):
        if offset <= 0x7FFF and not self.use_MAD1_mapping:
            # read ROM
            ROM_bank = 0x20000 + (bank-0x40) * 0x10000
            return self.ROM[ROM_bank + offset]
        elif offset >= 0x8000:
            # read ROM
            ROM_bank = 0x20000 + (bank-0x40) * 0x10000
            return self.ROM[ROM_bank + offset]
        else:
            raise IllegalAddressExcpetion()

    # 0x70:0000 - 7D:FFFF reads the SRAM inside the cartirge or the ROM
    def read_SRAM_ROM(self, bank, offset):
        if offset >= 0x0000 and offset <= 0x7FFF:
            # read SRAM
            # if the SRAM is smaller than 32Kbyte it is repeated on and on (SRAM mirror)
            return self.SRAM[offset % self.SRAM_size]
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

    # 0x80:0000 - 0xFF:FFFF mirror (same as self.read except RAM)
    def read_upper_mirror(self, bank, offset):
        if   bank >= (0x00+0x80) and bank <= (0x3F+0x80):
            return self.read_system(bank-0x80, offset)
        elif bank >= (0x40+0x80) and bank <= (0x6F+0x80):
            return self.read_ROM(bank-0x80, offset)
        elif bank >= (0x70+0x80) and bank <= (0x7D+0x80):
            return self.read_SRAM_ROM(bank-0x80, offset)
        elif bank >= (0x7E+0x80) and bank <= (0x7F+0x80):
            return self.read_more_SRAM_ROM(bank, offset) # different to self.read
        else:
            raise IllegalAddressExcpetion()

    # 0xFE:0000 - 0xFF:FFFF read more SRAM and ROM
    def read_more_SRAM_ROM(self, bank, offset):
        if bank == 0xFE:
            if offset >= 0x0000 and offset <= 0x7FFF:
                return self.SRAM[offset]
            elif offset >= 0x8000 and offset <= 0xFFFF:
                return self.ROM[0x3E8000 + offset]
            else:
                raise IllegalAddressExcpetion()
        elif bank == 0xFF:
            if offset >= 0x0000 and offset <= 0x7FFF:
                return self.SRAM[offset]
            elif offset >= 0x8000 and offset <= 0xFFFF:
                return self.ROM[0x3F0000 + offset]
            else:
                raise IllegalAddressExcpetion()
        else:
            raise IllegalAddressExcpetion()

    def write(self, bank, offset, value):
        if   bank >= 0x00 and bank <= 0x3F:
            self.write_system(bank, offset, value)
        elif bank >= 0x40 and bank <= 0x6F:
            raise CanNotWriteROMExcpetion()
        elif bank >= 0x70 and bank <= 0x7D:
            self.write_SRAM_ROM(bank, offset, value)
        elif bank >= 0x7E and bank <= 0x7F:
            self.write_RAM(bank, offset, value)
        elif bank >= 0x80 and bank <= 0xFF:
            self.write_upper_mirror(bank, offset, value)
        else:
            raise IllegalAddressExcpetion()

    # 0x00:0000 - 3F:FFFF read ROM and system stuff
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
            # if the SRAM is smaller than 32Kbyte it is repeated on and on (SRAM mirror)
            self.SRAM[offset % self.SRAM_size] = value
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

    # 0x80:0000 - 0xFF:FFFF mirror (same as self.write except RAM)
    def write_upper_mirror(self, bank, offset, value):
        if   bank >= (0x00+0x80) and bank <= (0x3F+0x80):
            self.write_system(bank-0x80, offset, value)
        elif bank >= (0x40+0x80) and bank <= (0x6F+0x80):
            self.write_ROM(bank-0x80, offset, value)
        elif bank >= (0x70+0x80) and bank <= (0x7D+0x80):
            self.write_SRAM_ROM(bank-0x80, offset, value)
        elif bank >= (0x7E+0x80) and bank <= (0x7F+0x80):
            self.write_more_SRAM_ROM(bank, offset, value) # different to self.write
        else:
            raise IllegalAddressExcpetion()

    # 0xFE:0000 - 0xFF:FFFF read more SRAM and ROM
    def write_more_SRAM_ROM(self, bank, offset, value):
        if bank == 0xFE:
            if offset >= 0x0000 and offset <= 0x7FFF:
                self.SRAM[offset] = value
            elif offset >= 0x8000 and offset <= 0xFFFF:
                # write ROM
                raise CanNotWriteROMExcpetion()
            else:
                raise IllegalAddressExcpetion()
        elif bank == 0xFF:
            if offset >= 0x0000 and offset <= 0x7FFF:
                self.SRAM[offset] = value
            elif offset >= 0x8000 and offset <= 0xFFFF:
                # write ROM
                raise CanNotWriteROMExcpetion()
            else:
                raise IllegalAddressExcpetion()
        else:
            raise IllegalAddressExcpetion()