from tool.cartrige import ROMHeader
from tool.helper import open_as_byte_array

# .../PySNES/venv/pysnes/$ py.test -k test_parse_header
ROM_DIR = 'rom/'

def test_parse_header0():
    ROM_NAME = 'DonkeyKongCountry.smc'
    ba = open_as_byte_array(ROM_DIR + ROM_NAME)
    header = ROMHeader(ba)
    assert header.name == 'DONKEY KONG COUNTRY  '
    assert hex(header.addr) == '0x81c0'
    assert hex(header.makeup) == '0x31'
    assert header.reset_int_addr == '8000'


def test_parse_header1():
    ROM_NAME = 'SecretofMana.smc'
    ba = open_as_byte_array(ROM_DIR + ROM_NAME)
    header = ROMHeader(ba)
    assert header.name == 'Secret of MANA       '
    assert hex(header.addr) == '0xffc0'
    assert hex(header.makeup) == '0x21'
    assert header.reset_int_addr == '8004'


def test_parse_header2():
    ROM_NAME = 'Terranigma.smc'
    ba = open_as_byte_array(ROM_DIR + ROM_NAME)
    header = ROMHeader(ba)
    assert header.name == 'TERRANIGMA D         '
    assert hex(header.addr) == '0x101c0'
    assert hex(header.makeup) == '0x31'
    assert header.reset_int_addr == '8000'
