from helper import get_two_bytes_little_endian, pow

LO_ROM_HEADER = "007FC0"
HI_ROM_HEADER = "00FFC0"

# data container for ROM header data
class ROMHeader(object):
    makeup_map = {
        32: "LoROM",            # 0x20
        33: "HiROM",            # 0x21
        35: "SA-1ROM",          # 0x23
        48: "LoROM / FastROM",  # 0x30
        49: "HiROM / FastROM",  # 0x31
        50: "ExLoROM",          # 0x32
        53: "ExHiROM"           # 0x35
    }
    rom_type_map = {
        0:  "ROM only",                     # 0x00
        1:  "ROM + RAM",                    # 0x01
        2:  "ROM + RAM + SRAM",             # 0x02
        3:  "ROM + DSP",                    # 0x03
        4:  "ROM + RAM + DSP",              # 0x04
        5:  "ROM + RAM + SRAM + DSP",       # 0x05
        6:  "ROM + SRAM + DSP",             # 0x06
        19: "ROM + SuperFX",                # 0x13
        20: "ROM + RAM + SuperFX",          # 0x14
        21: "ROM + RAM + SRAM + SuperFX",   # 0x15
        22: "ROM + SRAM + SuperFX",         # 0x16
        35: "ROM + OBC1",                   # 0x23
        36: "ROM + RAM + OBC1",             # 0x24
        37: "ROM + RAM + SRAM + OBC1",      # 0x25
        38: "ROM + SRAM + OBC1",            # 0x26
        51: "ROM + SA-1",                   # 0x33
        52: "ROM + RAM + SA-1",             # 0x34
        53: "ROM + RAM + SRAM + SA-1",      # 0x35
        54: "ROM + SRAM + SA-1",            # 0x36
        227:"ROM + OTHER",                  # 0xE3
        228:"ROM + RAM + OTHER",            # 0xE4
        229:"ROM + RAM + SRAM + OTHER",     # 0xE5
        230:"ROM + SRAM + OTHER",           # 0xE6
        243: "ROM + CUSTOM CHIP",               # 0xF3
        244: "ROM + RAM + CUSTOM CHIP",         # 0xF4
        245: "ROM + RAM + SRAM + CUSTOM CHIP",  # 0xF5
        246: "ROM + SRAM + CUSTOM CHIP"         # 0xF6
    }
    rom_size_map = {
        9:  "3~4MBit",          # 0x09
        10: "5~8MBit",          # 0x0A
        11: "9~16MBit",         # 0x0B
        12: "17~32MBit",        # 0x0C
        13: "33~64MBit"         # 0x0D
    }

    def __init__(self, rom_byte_array):
        self.file_size = len(rom_byte_array) # size in byte
        self.has_SCM = self.file_size % 1024 != 0
        self.addr = self.compute_header_start(rom_byte_array)
        self.parse_header(rom_byte_array, self.addr)
        self.parse_header_interrups(rom_byte_array, self.addr)

    def compute_checksum(self, rom_byte_array):
        addr = 0
        if self.has_SCM: # skip header if present
            addr = 512
        sum = 0
        while addr < self.file_size:
            sum += rom_byte_array[addr]
            addr = addr + 1
        self.expected_checksum = hex(sum & int("FFFF", 16))

    def compute_header_start(self, rom_byte_array):
        self.compute_checksum(rom_byte_array)
        addr = int(LO_ROM_HEADER, 16)
        if self.__does_header_match(rom_byte_array, addr):
            if self.has_SCM:
                return addr + 512
            return addr
        addr = int(HI_ROM_HEADER, 16)
        if self.__does_header_match(rom_byte_array, addr):
            if self.has_SCM:
                return addr + 512
            return addr
        raise Exception("Error: can not find ROM header")

    def __does_header_match(self, rom_byte_array, start_addr):
        if self.has_SCM: # skip header if present
            start_addr += 512
        cs1 = hex(rom_byte_array[start_addr + 30])[2:]
        cs1 = (2 - len(cs1)) * "0" + cs1
        cs2 = hex(rom_byte_array[start_addr + 31])[2:]
        cs2 = (2 - len(cs2)) * "0" + cs2
        checksum = cs2 + cs1
        csc1 = hex(rom_byte_array[start_addr + 28])[2:]
        csc1 = (2 - len(csc1)) * "0" + csc1
        csc2 = hex(rom_byte_array[start_addr + 29])[2:]
        csc2 = (2 - len(csc2)) * "0" + csc2
        checksum_complement = csc2 + csc1
        match_complement = (int(checksum, 16) + int(checksum_complement, 16) == 65535)
        return match_complement

    def parse_header(self, rom_byte_array, start_address):
        addr = start_address
        self.name      = rom_byte_array[addr:addr + 21]
        self.makeup    = rom_byte_array[addr + 21]
        self.rom_type  = rom_byte_array[addr + 22]
        self.rom_size  = rom_byte_array[addr + 23]
        self.sram_size = rom_byte_array[addr + 24]
        self.licence_code = get_two_bytes_little_endian(rom_byte_array[addr + 25], rom_byte_array[addr + 26])
        self.version = rom_byte_array[addr + 27]
        self.checksum_complement = get_two_bytes_little_endian(rom_byte_array[addr + 28], rom_byte_array[addr + 29])
        self.checksum = get_two_bytes_little_endian(rom_byte_array[addr + 30], rom_byte_array[addr + 31])

    # Find mem addr of interrupt code
    def parse_header_interrups(self, rom_byte_array, start_address):
        addr = start_address
        self.native_cop_int_addr   = get_two_bytes_little_endian(rom_byte_array[addr + 38], rom_byte_array[addr + 39])
        self.native_brk_int_addr   = get_two_bytes_little_endian(rom_byte_array[addr + 40], rom_byte_array[addr + 41])
        self.native_abort_int_addr = get_two_bytes_little_endian(rom_byte_array[addr + 42], rom_byte_array[addr + 43])
        self.native_reset_int_addr = get_two_bytes_little_endian(rom_byte_array[addr + 44], rom_byte_array[addr + 45])
        self.native_irq_int_addr   = get_two_bytes_little_endian(rom_byte_array[addr + 46], rom_byte_array[addr + 47])
        # co processor enable
        self.cop_int_addr   = get_two_bytes_little_endian(rom_byte_array[addr + 54], rom_byte_array[addr + 55])
        self.abort_int_addr = get_two_bytes_little_endian(rom_byte_array[addr + 56], rom_byte_array[addr + 57])
        self.nmi_int_addr   = get_two_bytes_little_endian(rom_byte_array[addr + 58], rom_byte_array[addr + 59])
        # execution begins at reset code (entry point of game)
        self.reset_int_addr = get_two_bytes_little_endian(rom_byte_array[addr + 60], rom_byte_array[addr + 61])
        self.irq_int_addr   = get_two_bytes_little_endian(rom_byte_array[addr + 62], rom_byte_array[addr + 63]) # TODO BRK

    def dump(self):
        print("HEADER START:       \t"   + hex(self.addr))
        if self.file_size > 1024*1024:
            str_size = str(self.file_size / (1024*1024)) + " MB"
        else:
            str_size = str(self.file_size / 1024)  + " KB"
        print("FILE SIZE:          \t"   + str(self.file_size)+" BYTE" + " (" + str_size + ")")
        print("SCM:                \t"   + str(self.has_SCM))
        print("")
        print("NAME:               \t"   + self.name)
        info = " (" + ROMHeader.makeup_map.get(self.makeup, "UNKNOWN") +  ")"
        print("MAKEUP:             \t"   + hex(self.makeup) + info)
        info = " (" + ROMHeader.rom_type_map.get(self.rom_type, "UNKNOWN")  +  ")"
        print("ROM TYPE:           \t"   + hex(self.rom_type) + info)
        info = " (" + ROMHeader.rom_size_map.get(self.rom_size, "UNKNOWN") +  ")"
        print("ROM SIZE:           \t"   + hex(self.rom_size) + info)
        print("SRAM SIZE:          \t"   + hex(self.sram_size) + " (" + str(2048*pow(2, self.sram_size)) +  " BYTE)")
        print("LICENCE CODE:       \t0x" + self.licence_code)
        print("VERSION:            \t"   + hex(self.version) + " (1." + str(self.version) +  ")")
        print("CHECKSUM COMPLEMENT:\t0x" + self.checksum_complement + " (NOT CHECKSUM)")
        print("CHECKSUM:           \t0x" + self.checksum + " (SUM OF BYTES AND 0xFFFF)")
        print("CHECKSUM STATUS:    \t"   + str(("0x" + self.checksum)==self.expected_checksum))
        print("")
        print("NATIVE COP INTERRUPT ADDR:  \t0x" + self.native_cop_int_addr  )
        print("NATIVE BRK INTERRUPT ADDR:  \t0x" + self.native_brk_int_addr )
        print("NATIVE ABORT INTERRUPT ADDR:\t0x" + self.native_abort_int_addr )
        print("NATIVE RESET INTERRUPT ADDR:\t0x" + self.native_reset_int_addr )
        print("NATIVE IRQ INTERRUPT ADDR:  \t0x" + self.native_irq_int_addr )
        print("COP INTERRUPT ADDR:         \t0x" + self.cop_int_addr)
        print("ABORT INTERRUPT ADDR:       \t0x" + self.abort_int_addr )
        print("NMI INTERRUPT ADDR:         \t0x" + self.nmi_int_addr )
        print("RESET INTERRUPT ADDR:       \t0x" + self.reset_int_addr)
        print("IRQ INTERRUPT ADDR:         \t0x" + self.irq_int_addr )


class Cartrige(object):
    pass


class LoROM(Cartrige):
    pass

class HiROM(Cartrige):
    pass


class CartrigeType(object):
    LOROM = 1
    HIROM = 2
    # TODO: More ...
