from tool.cartrige import CartrigeType
from tool.memory import MemoryMapper


RAM  = [0] * (2 ** 17 - 1)  # 128 KB
ROM  = [0] * (2 ** 22 - 1)  # 4 MB
SRAM = [0] * 0x7FFF         # 32 KB


def test_LoROM_ROM():
    ctype = CartrigeType.LOROM
    SRAM_size = 16384
    mem_map = MemoryMapper(ctype, RAM, ROM, SRAM, False, SRAM_size)
    assert ROM[3670016] == mem_map.read(0x708000)
    ROM[3670016] = 41
    assert ROM[3670016] == mem_map.read(0x708000)
    assert 41 == mem_map.read(0x708000)
    ROM[0] = 44
    assert ROM[0] == mem_map.read(0x008000)
    assert 44 == mem_map.read(0x008000)


def test_LoROM_SRAM():
    ctype = CartrigeType.LOROM
    SRAM_size = 16384
    mem_map = MemoryMapper(ctype, RAM, ROM, SRAM, False, SRAM_size)
    assert SRAM[0] == 0
    assert SRAM[0] == mem_map.read(0x700000)
    mem_map.write(0x700000, 42)
    assert SRAM[0] == 42
    assert SRAM[0] == mem_map.read(0x700000)


def test_LoROM_RAM():
    ctype = CartrigeType.LOROM
    SRAM_size = 16384
    mem_map = MemoryMapper(ctype, RAM, ROM, SRAM, False, SRAM_size)
    assert RAM[0] == mem_map.read(0x7E0000)
    mem_map.write(0x7E0000, 43)
    assert RAM[0] == mem_map.read(0x7E0000)
    assert RAM[0] == 43