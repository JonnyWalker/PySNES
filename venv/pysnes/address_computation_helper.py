


# some addresses are wrapped at the bank XX bank boundary (64 KB - 16 Bit addr)
# so if you read two bytes from XXFFFF the second byte will be read
# from XX0000 and not from X100000!
#
# There are mixed address modes. For example the computation of an
# address pointer using dp register is wrapped.
#
# while the address itself can cross bank boundaries.
# Direct page (dp register) and stack pointer are wrapped at the zero bank.
# Most likely there are bugs in wrapping implementations.
def compute_wrapped_addr(address):
    return address & 0x00FFFF

# OPCODE abs
def abs(address, DBR):
    # Address: BANK:OFFSET BB:OOOO with bank in DBR register and OFFSET in address
    return (DBR << 16) + address # no wrapping

# OPCODE abs, Y (used after stack)
def abs_y(address, DBR, Y, is8BitY):
    if is8BitY:
        Y = Y & 0x00FF
    # Address: BANK:OFFSET BB:OOOO with bank in DBR register and OFFSET in address
    return (DBR << 16) + address + Y # no wrapping

# OPCODE abs, X
def abs_x(address, DBR, X, is8BitX):
    if is8BitX:
        X = X & 0x00FF
    # Address: BANK:OFFSET BB:OOOO with bank in DBR register and OFFSET in address
    return (DBR << 16) + address + X # no wrapping

# OPCODE dp
def dp(address, DP):
    wrapped_addr = compute_wrapped_addr(address + DP) # direct page wrapping
    return wrapped_addr # zero bank wrapping!

# OPCODE dp, X
def dp_x(address, DP, X, is8BitX):
    if is8BitX:
        X = X & 0x00FF
    wrapped_addr = compute_wrapped_addr(address + DP + X) # direct page wrapping
    return wrapped_addr # zero bank wrapping!

# OPCODE dp, Y
def dp_y(address, DP, Y, is8BitY):
    if is8BitY:
        Y = Y & 0x00FF
    wrapped_addr = compute_wrapped_addr(address + DP + Y) # direct page wrapping
    return wrapped_addr # zero bank wrapping!

# OPCODE long, X
def long_x(address, X, is8BitY): # TODO: modify DBR when bank boundary is crossed?
    if is8BitY:
        X = X & 0x00FF
    return address + X # no wrapping, no DBR

# OPCODE long, Y (used after dp)
def long_y(address, Y, is8BitY): # TODO: modify DBR when bank boundary is crossed?
    if is8BitY:
        Y = Y & 0x00FF
    return address + Y # no wrapping, no DBR

# OPCODE stk,S
def stack(address, SP):
    wrapped_addr = compute_wrapped_addr(address + SP)
    return wrapped_addr  # zero bank wrapping!