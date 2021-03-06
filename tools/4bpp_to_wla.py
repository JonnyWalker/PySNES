# python 4bpp_to_wla.py BMPPATH
# input Windows 4BPP BMP File width = 128 height 16k (k in 1..n)
# everthing else will break
# e.g. $ python 4bpp_to_wla.py img/pacman/4BPP/PacMan.bmp >tiles.inc 
import sys

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


class Tile8x8Pixel(object):
    def __init__(self, num):
        self.num = num
        self.bit_string = []
        self.SNES_4BPP_encoding = []


def file_to_bmp_obj(name):
    bytes = []
    bmp = BitMap()
    with open(name, "r") as file:
        for data in file:
            bytes+=data
    bmp.type = bytes[0:2]
    bmp.size = ord(bytes[2]) # TODO: read three more bytes
    bmp.pixel_array_offset = ord(bytes[10]) # TODO: read three more bytes
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


# works only with 4BPP Bitmaps
def bmp_to_bit_string(bmp):
    index = 0
    bit_string = []
    line = ""
    for v in bmp.pixel_array:
        high = (ord(v) & 0xF0) >> 4
        low  = ord(v) & 0x0F
        h_string = bin(high)[2:] 
        l_string = bin(low)[2:]
        hp = (4-len(h_string))*"0" # padding
        lp = (4-len(l_string))*"0" # padding
        line += hp+h_string+lp+l_string
        index = index + 1
        if index == bmp.width/2:
            bit_string.append(line)
            index = 0
            line = ""
    # Pixel array starts ins the lower left corner
    bit_string.reverse()
    # Now its the uper left
    return bit_string


def bit_string_to_4BPP(tile):
    bit_string = tile.bit_string
    SNES_4BPP_encoding = []
    # iterate from left:
    # first and second bit plane (every bit 3 and 4)
    for line in bit_string:
        low = ""
        high = ""
        bit_counter = 0
        for i in range(len(line)):
            bit_counter +=1
            if bit_counter == 4:
                low += line[i]
                bit_counter = 0
            elif bit_counter == 3:
                high += line[i]
        h_string = hex(int(high, 2))[2:]
        l_string = hex(int(low,  2))[2:]
        hp = (2-len(h_string))*"0" # padding
        lp = (2-len(l_string))*"0" # padding
        SNES_4BPP_encoding.append(lp+l_string)
        SNES_4BPP_encoding.append(hp+h_string)
    # iterate from left:
    # third and fourth bit plane (every bit 1 and 2)
    for line in bit_string:
        low = ""
        high = ""
        bit_counter = 0
        for i in range(len(line)):
            bit_counter +=1
            if bit_counter == 4:
                bit_counter = 0
            if bit_counter == 2:
                low += line[i]
            elif bit_counter == 1:
                high += line[i]
        h_string = hex(int(high, 2))[2:]
        l_string = hex(int(low,  2))[2:]
        hp = (2-len(h_string))*"0" # padding
        lp = (2-len(l_string))*"0" # padding
        SNES_4BPP_encoding.append(lp+l_string)
        SNES_4BPP_encoding.append(hp+h_string)
    return SNES_4BPP_encoding


def color_8Bit_to_color_5Bit(bmp):
     color_5Bit = []
     color_5Bit_bin = []
     for color in bmp.palette:
         R = bin(color[0]/8)[2:] # 32*8=256
         rp = (5-len(R))*"0"     # padding
         G = bin(color[1]/8)[2:] # 32*8=256
         gp = (5-len(G))*"0"     # padding
         B = bin(color[2]/8)[2:] # 32*8=256
         bp = (5-len(B))*"0"     # padding
         bin_string = "0"+bp+B+gp+G+rp+R
         color_5Bit_bin.append(bin_string)
         value = int(bin_string, 2)
         h_string = hex((value & 0xFF00) >> 8)[2:]
         l_string = hex(value & 0x00FF)[2:]
         hp = (2-len(h_string))*"0" # padding
         lp = (2-len(l_string))*"0" # padding
         color_5Bit.append(lp+l_string) # little endian
         color_5Bit.append(hp+h_string)
     return color_5Bit, color_5Bit_bin


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
    print("Palette (BMP / SNES Encoding):")
    for i, color in enumerate(bmp.palette):
        print(str(i)+":"+str(color))


def dump_wla_info(tiles, color_5Bit):
    print("TileData:")
    for tile in tiles:
        print("\n    ;Tile Numer:"+str(tile.num))
        wla_string = "    .db "
        for value in tile.SNES_4BPP_encoding[0:16]:
            wla_string += "$"+value+","
        print(wla_string[:-1])
        wla_string = "    .db "
        for value in tile.SNES_4BPP_encoding[16:]:
            wla_string += "$"+value+","
        print(wla_string[:-1])
    print("Palette:")
    wla_string = "    .db "
    for value in color_5Bit[:16]:
        wla_string += "$"+value+","
    print(wla_string[:-1])
    if len(color_5Bit) > 16:
        wla_string = "    .db "
        for value in color_5Bit[16:32]:
            wla_string += "$"+value+","
        print(wla_string[:-1])


if len(sys.argv) != 2:
    print("python 4bpp_to_wla.py BMPPATH")
else:
    bmp = file_to_bmp_obj(sys.argv[1])
    bit_string = bmp_to_bit_string(bmp)
    tiles = []
    # num of 8x8 tiles  in one row = width / 8
    tile_num = (bmp.width / 8) * (bmp.height / 8)
    for i in range(tile_num):
        tiles.append(Tile8x8Pixel(i))
    for tile_row in range(bmp.height / 8):
        for tile_column in range(bmp.width / 8):
            for line in bit_string[0+(tile_row*8):8+(tile_row*8)]: # process 8 rows
                # one row = 32 Bits
                tiles[tile_column+(tile_row*(bmp.width / 8))].bit_string.append(line[0+(32*tile_column):32+(32*tile_column)])
    for tile in tiles:
        for line in tile.bit_string:
            snes_encoding = bit_string_to_4BPP(tile)
            tile.SNES_4BPP_encoding = snes_encoding
    #dump_bmp_info(bmp)
    color_5Bit, color_5Bit_bin = color_8Bit_to_color_5Bit(bmp)
    dump_wla_info(tiles, color_5Bit)
