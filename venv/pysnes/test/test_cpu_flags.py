from tool.cpu import CPU65816

def test_SEP0():
    cpu = CPU65816(None)
    assert cpu.P == 0b00000000
    cpu.fetch_decode_execute([0xEA])
    assert cpu.P == 0b00000000

def test_SEP1():
    cpu = CPU65816(None)
    assert cpu.P == 0b00000000
    cpu.fetch_decode_execute([0xE2, 0x00])
    assert cpu.P == 0b00000000

def test_SEP2():
    cpu = CPU65816(None)
    assert cpu.P == 0b00000000
    cpu.fetch_decode_execute([0xE2, 0x01])
    assert cpu.P == 0b00000001

def test_SEP3():
    cpu = CPU65816(None)
    assert cpu.P == 0b00000000
    cpu.fetch_decode_execute([0xE2, 0x81])
    assert cpu.P == 0b10000001

def test_REP0():
    cpu = CPU65816(None)
    assert cpu.P == 0b00000000
    cpu.fetch_decode_execute([0xC2, 0x00])
    assert cpu.P == 0b00000000

def test_REP1():
    cpu = CPU65816(None)
    cpu.P = 0b00100010
    cpu.fetch_decode_execute([0xC2, 0x00])
    assert cpu.P == 0b00100010

def test_REP2():
    cpu = CPU65816(None)
    cpu.P = 0b00100010
    cpu.fetch_decode_execute([0xC2, 0x02])
    assert cpu.P == 0b00100000

def test_SEP_REP():
    cpu = CPU65816(None)
    cpu.run_code([0xE2, 0x02, 0xC2, 0x02])
    assert cpu.P == 0b00000000

def test_CLC():
    cpu = CPU65816(None)
    cpu.P = 0b00000001
    cpu.run_code([0x18])
    assert cpu.P == 0b00000000

def test_CLC1():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.run_code([0x18])
    assert cpu.P == 0b00000000

def test_SEI():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.run_code([0x78])
    assert cpu.P == 0b00000100

def test_SEI1():
    cpu = CPU65816(None)
    cpu.P = 0b00000100
    cpu.run_code([0x78])
    assert cpu.P == 0b00000100

def test_SED():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.run_code([0xF8])
    assert cpu.P == 0b00001000

def test_SED1():
    cpu = CPU65816(None)
    cpu.P = 0b00001000
    cpu.run_code([0xF8])
    assert cpu.P == 0b00001000

def test_CLD():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.run_code([0xD8])
    assert cpu.P == 0b00000000

def test_CLD1():
    cpu = CPU65816(None)
    cpu.P = 0b00001000
    cpu.run_code([0xD8])
    assert cpu.P == 0b00000000

def test_CLI():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.run_code([0x58])
    assert cpu.P == 0b00000000

def test_CLI1():
    cpu = CPU65816(None)
    cpu.P = 0b00000100
    cpu.run_code([0x58])
    assert cpu.P == 0b00000000

def test_CLV():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.run_code([0xB8])
    assert cpu.P == 0b00000000

def test_CLV1():
    cpu = CPU65816(None)
    cpu.P = 0b01000000
    cpu.run_code([0xB8])
    assert cpu.P == 0b00000000

def test_XCE():
    cpu = CPU65816(None)
    cpu.P = 0b00000000
    cpu.e = 1
    cpu.run_code([0xFB])
    assert cpu.e == 0
    assert cpu.P == 0b00000001

def test_XCE1():
    cpu = CPU65816(None)
    cpu.P = 0b00000001
    cpu.e = 1
    cpu.run_code([0xFB])
    assert cpu.e == 1
    assert cpu.P == 0b00000001

def test_XCE2():
    cpu = CPU65816(None)
    cpu.P = 0b00000001
    cpu.e = 0
    cpu.run_code([0xFB])
    assert cpu.e == 1
    assert cpu.P == 0b00000000