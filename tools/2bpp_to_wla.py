# https://en.wikipedia.org/wiki/BMP_file_format
class BitMap(object):
    size = 0
    type = ""
    pixel_array_offset = 0
    header_size = 0
    width = 0
    height = 0
    bpp = 0
    color_num = 0
    pixel_array = []
    palette = []


def file_to_bmp_obj(name):
    bytes = []
    bmp = BitMap()
    with open(name, "r") as file:
        for data in file:
            bytes = data
    bmp.type = bytes[0:2]
    bmp.size = ord(bytes[2]) # TODO: read three more bytes
    bmp.pixel_array_offset = ord(bytes[10])
    bmp.header_size = ord(bytes[14])
    bmp.width = ord(bytes[18]) # TODO: read one more byte
    bmp.height = ord(bytes[22]) # TODO: read one more byte
    bmp.bpp = ord(bytes[28]) # TODO: read one more byte
    bmp.color_num = ord(bytes[46]) # TODO: read three more bytes
    bmp.pixel_array = bytes[bmp.pixel_array_offset:] 
    offset = bmp.pixel_array_offset-1 
    for color in range(bmp.color_num):
         A = ord(bytes[offset])
         offset = offset -1
         R = ord(bytes[offset])
         offset = offset -1
         G = ord(bytes[offset])
         offset = offset -1
         B = ord(bytes[offset])
         offset = offset -1 
         bmp.palette.append((R,G,B,A))
    bmp.palette.reverse()    
    return bmp


def dump_bmp_info(bmp):
    print("Bitmap Header")
    print("type:\t\t\t" + str(bmp.type))
    print("size:\t\t\t" + str(bmp.size) + " bytes")
    print("pixel array offset:\t" + str(bmp.pixel_array_offset))
    print("header size:\t\t" + str(bmp.header_size)+" bytes")
    print("width:\t\t\t" + str(bmp.width))
    print("height:\t\t\t" + str(bmp.height))
    print("Bit per pixel:\t\t" + str(bmp.bpp))
    print("Number of Colors:\t" + str(bmp.color_num))


# works only with 2BPP
def bmp_to_bit_string(bmp):
    index = 0
    bit_string = []
    line = ""
    for v in bmp.pixel_array:
        high = (ord(v) & 0xF0) >> 4
        low  = ord(v) & 0x0F
        h_string = bin(high)[2:] 
        l_string = bin(low)[2:]
        hp = (2-len(h_string))*"0" # padding
        lp = (2-len(l_string))*"0" # padding
        line += hp+h_string+lp+l_string
        index = index + 1
        if index == bmp.width/2:
            bit_string.append(line)
            index = 0
            line = ""
    bit_string.reverse()
    return bit_string


def bit_string_to_2BPP(bit_string):
    SNES_2BPP_encoding = []
    for line in bit_string:
        low = ""
        high = ""
        for i in range(len(line)):
            if i % 2 == 0:
                low += line[i]
            else:
                high += line[i]
        h_string = hex(int(high, 2))[2:]
        l_string = hex(int(low,  2))[2:]
        hp = (2-len(h_string))*"0" # padding
        lp = (2-len(l_string))*"0" # padding
        SNES_2BPP_encoding.append(hp+h_string)
        SNES_2BPP_encoding.append(lp+l_string)
    return SNES_2BPP_encoding


def color_8Bit_to_color_5Bit(bmp):
     color_5Bit = []
     for color in bmp.palette:
         R = bin(color[0]/8)[2:] # 32*8=256
         rp = (5-len(R))*"0"     # padding
         G = bin(color[1]/8)[2:] # 32*8=256
         gp = (5-len(G))*"0"     # padding
         B = bin(color[2]/8)[2:] # 32*8=256
         bp = (5-len(B))*"0"     # padding
         bin_string = "0"+bp+B+gp+G+rp+R
         value = int(bin_string, 2)
         h_string = hex((value & 0xFF00) >> 8)[2:]
         l_string = hex(value & 0x00FF)[2:]
         hp = (2-len(h_string))*"0" # padding
         lp = (2-len(l_string))*"0" # padding
         color_5Bit.append(lp+l_string) # little endian
         color_5Bit.append(hp+h_string)
     return color_5Bit


bmp = file_to_bmp_obj("img/pacman/GhostUL.bmp")
dump_bmp_info(bmp)
bit_string = bmp_to_bit_string(bmp)
snes_encoding = bit_string_to_2BPP(bit_string)
color_5Bit = color_8Bit_to_color_5Bit(bmp)

index = 0
for line in bit_string:
    print(line+":"+snes_encoding[index] + snes_encoding[index+1])
    index +=2
print("WLA tile data:")
wla_string = ".db "
for value in snes_encoding:
    wla_string += "$"+value+","
print(wla_string[:-1])
print("WLA palette data:")
wla_string = ".db "
for value in color_5Bit:
    wla_string += "$"+value+","
print(wla_string[:-1])
