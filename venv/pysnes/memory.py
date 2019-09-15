from cartrige import CartrigeType
from dma import DMAController, HDMAController
from internal_cpu import InternalCPURegisters
from ppu import PPU


# When the CPU puts a signal on its address bus some bytes can be
# read or written from/to "somewhere" (e.g. ROM, RAM, SRAM or other) via the data bus.
# The Cartirgetype (e.g. LoROM, HiROM, ...) determines what has been addressed.
# This module implements this memory mapping
#
# Note: The SNES CPU only puts a signal on the address bus. Where the data
# is coming from is handled by a cartirge mem mapper. Normaly this is
# standardized (LoROM, HiROM, ..) but it can differ from the implementation here
# on some games. Only in rare cases the mapping is done by the SNES
# instead of the cartrige (e.g. RAM access)
class MemoryMapper(object):
    def __init__(self, header, RAM, ROM, SRAM, use_MAD1_mapping, SRAM_size):
        self.header = header
        cartrige_type = header.getCartridgeType()
        if cartrige_type == CartrigeType.LOROM:
            self.mapper = LoROMMemoryMapper(RAM, ROM, SRAM, use_MAD1_mapping, SRAM_size)
        elif cartrige_type == CartrigeType.HIROM:
            self.mapper = HiROMMemoryMapper(RAM, ROM, SRAM, use_MAD1_mapping, SRAM_size)
        else:
            raise NotImplementedError()

    # called by the CPU
    def read(self, address):
        bank = (address & 0xFF0000) >> 16 # get first two bytes (MSB)
        offset = address & 0x00FFFF
        return self.mapper.read(bank, offset)

    # called by the CPU
    def write(self, address, value):
        bank = (address & 0xFF0000) >> 16 # get first two bytes (MSB)
        offset = address & 0x00FFFF
        self.mapper.write(bank, offset, value)


class LoROMMemoryMapper(object):
    def __init__(self, RAM, ROM, SRAM, use_MAD1_mapping, SRAM_size):
        self.RAM  = RAM # TODO: maybe rename to WRAM
        self.ROM  = ROM
        self.SRAM = SRAM
        self.use_MAD1_mapping = use_MAD1_mapping
        self.SRAM_size = SRAM_size
        self.dma = DMAController()
        self.hdm = HDMAController()
        self.internal_cpu_registers = InternalCPURegisters()
        self.ppu = PPU()

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
    # TODO: the doc on the internet is very inconsistent about the memory ranges
    def read_system(self, bank, offset):
        if offset <= 0x1FFF:
            return self.RAM[offset]
        elif offset>= 0x2000 and offset <= 0x2FFF: # maybe 21FF is correct
            # TODO: PPU, APU, Hardware Registers
            # 0x2100 - 0x213F PPU (or PPU2 ?)
            # 0x2180 - 0x2183 (insde RAM?)
            # raise NotImplementedError()
            return self.ppu.read(offset)
        elif offset >= 0x3000 and offset <= 0x3FFF:
            # TODO: Super-FX, DSP
            raise NotImplementedError()
        elif offset >= 0x4000 and offset <= 0x41FF: # maybe 40FF is correct
            # TODO: Joypad Registers / Controller
            # 0x4016 - 0x4017 CPU
            raise NotImplementedError()
        elif offset >= 0x4200 and offset <= 0x5FFF: # maybe 44FF is correct
            # TODO: DMA, PPU2, Hardware Registers
            # 0x4200 - 0x420D CPU
            # 0x4100 - 0x421F CPU
            # 0x4300 - 0x437F CPU
            if offset == 0x4200:
                return self.internal_cpu_registers.read(offset)
            elif offset >= 0x4300 and offset <= 0x43FF:
                return self.dma.read(offset)
            print("Error read Address: " + hex(offset))
            return 0
        elif offset >= 0x6000 and offset <= 0x7FFF:
            # TODO: enhancement chip memory
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
        # 8KB LowRAM, 24KB HighRAM, 96KB ExRAM
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
            raise CanNotWriteROMException()
        elif bank >= 0x70 and bank <= 0x7D:
            self.write_SRAM_ROM(bank, offset, value)
        elif bank >= 0x7E and bank <= 0x7F:
            self.write_RAM(bank, offset, value)
        elif bank >= 0x80 and bank <= 0xFF:
            self.write_upper_mirror(bank, offset, value)
        else:
            raise IllegalAddressExcpetion()

    # 0x00:0000 - 3F:FFFF write system stuff
    # TODO: the doc on the internet is very inconsistent about the memory ranges
    # TODO: do we need the bak arg?
    def write_system(self, bank, offset, value):
        if offset <= 0x1FFF:
            self.RAM[offset] = value
        elif offset>= 0x2000 and offset <= 0x2FFF: # maybe 21FF is correct
            # TODO: PPU, APU, Hardware Registers
            # 0x2100 - 0x213F PPU (or PPU2 ?)
            # 0x2180 - 0x2183 (insde RAM?)
            # raise NotImplementedError()
            self.ppu.write(offset, value)
        elif offset >= 0x3000 and offset <= 0x3FFF:
            # TODO: Super-FX, DSP
            raise NotImplementedError()
        elif offset >= 0x4000 and offset <= 0x41FF: # maybe 40FF is correct
            # TODO: Joypad Registers / Controller
            # 0x4016 - 0x4017 CPU
            raise NotImplementedError()
        elif offset >= 0x4200 and offset <= 0x5FFF: # maybe 44FF is correct
            # TODO: DMA, PPU2, Hardware Registers
            # 0x4200 - 0x420D CPU
            # 0x4100 - 0x421F CPU
            if offset == 0x4200:
                self.internal_cpu_registers.write(offset, value)
                return
            elif offset >= 0x4300 and offset <= 0x43FF:
                self.dma.write(offset, value)
                return
            # 0x4300 - 0x437F CPU
            print("Error write Address: " + hex(offset)+ str(value))
        elif offset >= 0x6000 and offset <= 0x7FFF:
            # TODO: enhancement chip memory
            raise NotImplementedError()
        elif offset >= 0x8000:
            # write ROM
            raise CanNotWriteROMException()
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
            raise CanNotWriteROMException()
        else:
            raise IllegalAddressExcpetion()

    # 0x7E:0000 - 0x7F:FFFF writes the RAM inside the SNES
    def write_RAM(self, bank, offset, value):
        # 8KB LowRAM, 24KB HighRAM, 96KB ExRAM
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
            # write ROM
            raise CanNotWriteROMException()
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
                raise CanNotWriteROMException()
            else:
                raise IllegalAddressExcpetion()
        elif bank == 0xFF:
            if offset >= 0x0000 and offset <= 0x7FFF:
                self.SRAM[offset] = value
            elif offset >= 0x8000 and offset <= 0xFFFF:
                # write ROM
                raise CanNotWriteROMException()
            else:
                raise IllegalAddressExcpetion()
        else:
            raise IllegalAddressExcpetion()

class HiROMMemoryMapper(object):
    def __init__(self, RAM, ROM, SRAM, use_MAD1_mapping, SRAM_size):
        self.RAM  = RAM # WRAM
        self.ROM  = ROM
        self.SRAM = SRAM
        self.use_MAD1_mapping = use_MAD1_mapping
        self.SRAM_size = SRAM_size

    def read(self, bank, offset):
        if   bank >= 0x00 and bank <= 0x1F:
            return self.read_system(bank, offset)
        elif bank >= 0x20 and bank <= 0x3F:
            return self.read_system2(bank, offset)
        elif bank >= 0x40 and bank <= 0x7D:
            return self.read_ROM(bank, offset)
        elif bank >= 0x7E and bank <= 0x7F:
            return self.read_RAM(bank, offset)
        elif bank >= 0x80 and bank <= 0xFF:
            return self.read_upper_mirror(bank, offset)
        else:
            raise IllegalAddressExcpetion()

    # 0x00:0000 - 1F:FFFF read ROM and system stuff
    # TODO: the doc on the internet is very inconsistent about the memory ranges
    def read_system(self, bank, offset):
        if offset <= 0x1FFF:
            return self.RAM[offset]
        elif offset>= 0x2000 and offset <= 0x2FFF: # maybe 21FF is correct
            # TODO: PPU, APU, Hardware Registers
            # 0x2100 - 0x213F PPU (or PPU2 ?)
            # 0x2180 - 0x2183 (inside RAM?)
            raise NotImplementedError()
        elif offset >= 0x3000 and offset <= 0x3FFF:
            # TODO: Super-FX, DSP
            raise NotImplementedError()
        elif offset >= 0x4000 and offset <= 0x41FF: # maybe 40FF is correct
            # TODO: Joypad Registers / Controller
            # 0x4016 - 0x4017 CPU
            raise NotImplementedError()
        elif offset >= 0x4200 and offset <= 0x5FFF: # maybe 44FF is correct
            # TODO: DMA, PPU2, Hardware Registers
            # 0x4200 - 0x420D CPU
            # 0x4100 - 0x421F CPU
            # 0x4300 - 0x437F CPU
            raise NotImplementedError()
        elif offset >= 0x6000 and offset <= 0x7FFF:
            # TODO: enhancement chip memory
            raise NotImplementedError()
        elif offset >= 0x8000:
            # read ROM
            ROM_bank = (bank) * 0x10000
            return self.ROM[ROM_bank + offset]
        else:
            raise IllegalAddressExcpetion()


    # 0x20:0000 - 3F:FFFF read ROM, SRAM and system stuff
    # TODO: the doc on the internet is very inconsistent about the memory ranges
    def read_system2(self, bank, offset):
        if offset <= 0x1FFF:
            return self.RAM[offset]
        elif offset>= 0x2000 and offset <= 0x2FFF: # maybe 21FF is correct
            # TODO: PPU, APU, Hardware Registers
            # 0x2100 - 0x213F PPU (or PPU2 ?)
            # 0x2180 - 0x2183 (insde RAM?)
            raise NotImplementedError()
        elif offset >= 0x3000 and offset <= 0x3FFF:
            # TODO: Super-FX, DSP
            raise NotImplementedError()
        elif offset >= 0x4000 and offset <= 0x41FF: # maybe 40FF is correct
            # TODO: Joypad Registers / Controller
            # 0x4016 - 0x4017 CPU
            raise NotImplementedError()
        elif offset >= 0x4200 and offset <= 0x5FFF: # maybe 44FF is correct
            # TODO: DMA, PPU2, Hardware Registers
            # 0x4200 - 0x420D CPU
            # 0x4100 - 0x421F CPU
            # 0x4300 - 0x437F CPU
            raise NotImplementedError()
        elif offset >= 0x6000 and offset <= 0x7FFF:
            # write SRAM
            SRAM_page = (bank-0x20)*0x1FFF
            # if the SRAM is smaller than 32Kbyte it is repeated on and on (SRAM mirror)
            return self.SRAM[SRAM_page % self.SRAM_size]
        elif offset >= 0x8000:
            # read ROM
            ROM_bank = (bank) * 0x10000
            return self.ROM[ROM_bank + offset]
        else:
            raise IllegalAddressExcpetion()

    # 0x40:0000 - 7D:FFFF read ROM
    def read_ROM(self, bank, offset):
        if offset >= 0x0000  and offset <= 0xFFFF:
            # read ROM
            ROM_bank = (bank-0x40) * 0x10000
            return self.ROM[ROM_bank + offset]
        else:
            raise IllegalAddressExcpetion()

    # 0x7E:0000 - 0x7F:FFFF read the RAM inside the SNES
    def read_RAM(self, bank, offset):
        # 8KB LowRAM, 24KB HighRAM, 96KB ExRAM
        if bank == 0x7E:
            return self.RAM[offset]
        elif bank == 0x7F:
            return self.RAM[0x8000 + offset]
        else:
            raise IllegalAddressExcpetion()

    # 0x80:0000 - 0xFF:FFFF mirror (same as self.read except RAM)
    def read_upper_mirror(self, bank, offset):
        if   bank >= (0x00+0x80) and bank <= (0x1F+0x80):
            return self.read_system(bank-0x80, offset)
        elif bank >= (0x20+0x80) and bank <= (0x3F+0x80):
            return self.read_system2(bank-0x80, offset)
        elif bank >= (0x40+0x80) and bank <= (0x7D+0x80):
            return self.read_ROM(bank-0x80, offset)
        elif bank >= (0x7E+0x80) and bank <= (0x7F+0x80):
            return self.read_more_ROM(bank, offset) # different to self.read
        else:
            raise IllegalAddressExcpetion()

    # 0xFE:0000 - 0xFF:FFFF read more ROM
    def read_more_ROM(self, bank, offset):
        if bank == 0xFE:
            return self.ROM[0x3E0000 + offset]
        elif bank == 0xFF:
            return self.ROM[0x3F0000 + offset]
        else:
            raise IllegalAddressExcpetion()

    def write(self, bank, offset, value):
        if bank >= 0x00 and bank <= 0x1F:
            self.write_system(bank, offset, value)
        elif bank >= 0x20 and bank <= 0x3F:
            self.write_system2(bank, offset, value)
        elif bank >= 0x40 and bank <= 0x7D:
            raise CanNotWriteROMException()
        elif bank >= 0x7E and bank <= 0x7F:
            self.write_RAM(bank, offset, value)
        elif bank >= 0x80 and bank <= 0xFF:
            self.write_upper_mirror(bank, offset, value)
        else:
            raise IllegalAddressExcpetion()


    # 0x00:0000 - 1F:FFFF write system stuff
    # TODO: the doc on the internet is very inconsistent about the memory ranges
    def write_system(self, bank, offset, value):
        if offset <= 0x1FFF:
            self.RAM[offset] = value
        elif offset >= 0x2000 and offset <= 0x2FFF:  # maybe 21FF is correct
            # TODO: PPU, APU, Hardware Registers
            # 0x2100 - 0x213F PPU (or PPU2 ?)
            # 0x2180 - 0x2183 (insde RAM?)
            raise NotImplementedError()
        elif offset >= 0x3000 and offset <= 0x3FFF:
            # TODO: Super-FX, DSP
            raise NotImplementedError()
        elif offset >= 0x4000 and offset <= 0x41FF:  # maybe 40FF is correct
            # TODO: Joypad Registers / Controller
            # 0x4016 - 0x4017 CPU
            raise NotImplementedError()
        elif offset >= 0x4200 and offset <= 0x5FFF:  # maybe 44FF is correct
            # TODO: DMA, PPU2, Hardware Registers
            # 0x4200 - 0x420D CPU
            # 0x4100 - 0x421F CPU
            # 0x4300 - 0x437F CPU
            raise NotImplementedError()
        elif offset >= 0x6000 and offset <= 0x7FFF:
            # TODO: enhancement chip memory
            raise NotImplementedError()
        elif offset >= 0x8000:
            # write ROM
            raise CanNotWriteROMException()
        else:
            raise IllegalAddressExcpetion()


    # 0x20:0000 - 3F:FFFF write SRAM and system stuff
    # TODO: the doc on the internet is very inconsistent about the memory ranges
    def write_system2(self, bank, offset, value):
        if offset <= 0x1FFF:
            self.RAM[offset] = value
        elif offset >= 0x2000 and offset <= 0x2FFF:  # maybe 21FF is correct
            # TODO: PPU, APU, Hardware Registers
            # 0x2100 - 0x213F PPU (or PPU2 ?)
            # 0x2180 - 0x2183 (insde RAM?)
            raise NotImplementedError()
        elif offset >= 0x3000 and offset <= 0x3FFF:
            # TODO: Super-FX, DSP
            raise NotImplementedError()
        elif offset >= 0x4000 and offset <= 0x41FF:  # maybe 40FF is correct
            # TODO: Joypad Registers / Controller
            # 0x4016 - 0x4017 CPU
            raise NotImplementedError()
        elif offset >= 0x4200 and offset <= 0x5FFF:  # maybe 44FF is correct
            # TODO: DMA, PPU2, Hardware Registers
            # 0x4200 - 0x420D CPU
            # 0x4100 - 0x421F CPU
            # 0x4300 - 0x437F CPU
            raise NotImplementedError()
        elif offset >= 0x6000 and offset <= 0x7FFF:
            # write SRAM
            SRAM_page = (bank - 0x20) * 0x1FFF
            # if the SRAM is smaller than 32Kbyte it is repeated on and on (SRAM mirror)
            self.SRAM[SRAM_page % self.SRAM_size] = value
        elif offset >= 0x8000:
            # write ROM
            raise CanNotWriteROMException()
        else:
            raise IllegalAddressExcpetion()

    # 0x7E:0000 - 0x7F:FFFF write the RAM inside the SNES
    def write_RAM(self, bank, offset, value):
        # 8KB LowRAM, 24KB HighRAM, 96KB ExRAM
        if bank == 0x7E:
            self.RAM[offset] = value
        elif bank == 0x7F:
            self.RAM[0x8000 + offset] = value
        else:
            raise IllegalAddressExcpetion()


    # 0x80:0000 - 0xFF:FFFF mirror (same as self.write except RAM)
    def write_upper_mirror(self, bank, offset, value):
        if bank >= (0x00 + 0x80) and bank <= (0x1F + 0x80):
            self.write_system(bank - 0x80, offset, value)
        elif bank >= (0x20 + 0x80) and bank <= (0x3F + 0x80):
            self.write_system2(bank - 0x80, offset, value)
        elif bank >= (0x40 + 0x80) and bank <= (0x7D + 0x80):
            raise CanNotWriteROMException()
        elif bank >= (0x7E + 0x80) and bank <= (0x7F + 0x80):
            raise CanNotWriteROMException() # different to self.write
        else:
            raise IllegalAddressExcpetion()


class SA1ROMMemoryMapper(object):
    pass # low impl. priotity (e.g. Super Mario RPG)


class ExLoROMMemoryMapper(object):
    pass # low impl. priotity (e.g. Star Ocean)


class ExHiROMMemoryMapper(object):
    pass # low impl. priotity (e.g. Tales of Phantasia)

class IllegalAddressExcpetion(Exception):
    pass


class CanNotWriteROMException(Exception):
    '''Internal error: can not write ROM!'''
    pass