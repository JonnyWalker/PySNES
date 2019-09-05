def get_two_bytes_little_endian(byte0, byte1):
    b0 = hex(byte0)[2:]
    b0 = (2 - len(b0)) * "0" + b0
    b1 = hex(byte1)[2:]
    b1 = (2 - len(b1)) * "0" + b1
    return  int(b1 + b0, 16)

def open_as_byte_array(rom_name):
    file = open(rom_name, 'rb')
    b_array = bytearray(file.read())
    file.close()
    return b_array

# prints a byte array hex-style
def print_hex_dump(rom_byte_array):
    ba = rom_byte_array
    # to hex
    def h(ba):
        d = hex(ba)[2:] # remove 0x prefix
        d = (2-len(d))*"0"+d # fill with leading zeros
        return d
    a = 0
    print("addr\thex")
    while a < len(ba):
        addr = hex(a)[2:]
        addr = (6-len(addr))*"0"+addr # fill with leading zeros
        addr = addr.upper()
        hex_line = h(ba[a])+h(ba[a+1])+h(ba[a+2])+h(ba[a+3]) \
              +h(ba[a+4])+h(ba[a+5])+h(ba[a+6])+h(ba[a+7]) \
              +h(ba[a+8])+h(ba[a+9])+h(ba[a+10])+h(ba[a+11]) \
              +h(ba[a+12])+h(ba[a+13])+h(ba[a+14])+h(ba[a+15])
        hex_line = hex_line.upper()
        ascii = ba[a:a+16]
        ascii = ascii.replace("\n", " ") # remove line breaks
        ascii = ascii.replace("\r", " ")
        print(addr + ":\t"+ hex_line + "\t" + ascii)
        a +=16


def pow(basis, exp):
    result = 1
    for i in range(exp):
        result *= basis
    return result