class PPU(object):
    def __init__(self):
        self.INIDISP_8 = 0    # Screen Display Register
        self.OBSEL_8   = 0    # Object Size and Character Size Register
        self.OAMADDL = 0    # OAM Address Registers(Low)
        self.OAMADDH = 0    # OAM Address Registers(High)
        self.OAMDATA = 0    # OAM Data Write Register
        self.BGMODE_8  = 0    # BG Mode and Character Size Register
        self.MOSAIC_8  = 0    # Mosaic Register
        self.BG1SC_8   = 0    # BG Tilemap Address Registers(BG1)
        self.BG2SC_8   = 0    # BG Tilemap Address Registers(BG2)
        self.BG3SC_8   = 0    # BG Tilemap Address Registers(BG3)
        self.BG4SC_8   = 0    # BG Tilemap Address Registers(BG4)
        self.BG12NBA_8 = 0    # BG Character Address Registers(BG1 & 2)
        self.BG34NBA_8 = 0    # BG Character Address Registers(BG3 & 4)
        self.BG1HOFS_16 = 0    # BG Scroll Registers(BG1)
        self.BG1VOFS_16 = 0    # BG Scroll Registers(BG1)
        self.BG2HOFS_16 = 0    # BG Scroll Registers(BG2)
        self.BG2VOFS_16 = 0    # BG Scroll Registers(BG2)
        self.BG3HOFS_16 = 0    # BG Scroll Registers(BG3)
        self.BG3VOFS_16 = 0    # BG Scroll Registers(BG3)
        self.BG4HOFS_16 = 0    # BG Scroll Registers(BG4)
        self.BG4VOFS_16 = 0    # BG Scroll Registers(BG4)
        self.VMAIN   = 0    # Video Port Control Register
        self.VMADDL  = 0    # VRAM Address Registers(Low)
        self.VMADDH  = 0    # VRAM Address Registers(High)
        self.VMDATAL = 0    # VRAM Data Write Registers(Low)
        self.VMDATAH = 0    # VRAM Data Write Registers(High)
        self.M7SEL_8   = 0    # Mode 7 Settings Register
        self.M7A_16     = 0    # Mode 7 Matrix Registers
        self.M7B_16     = 0    # Mode 7 Matrix Registers
        self.M7C_16     = 0    # Mode 7 Matrix Registers
        self.M7D_16     = 0    # Mode 7 Matrix Registers
        self.M7X_16     = 0    # Mode 7 Matrix Registers
        self.M7Y_16     = 0    # Mode 7 Matrix Registers
        self.CGADD   = 0    # CGRAM Address Register
        self.CGDATA  = 0    # CGRAM Data Write Register
        self.W12SEL_8  = 0    # Window Mask Settings Registers
        self.W34SEL_8  = 0    # Window Mask Settings Registers
        self.WOBJSEL_8 = 0    # Window Mask Settings Registers
        self.WH0     = 0    # Window Position Registers(WH0)
        self.WH1     = 0    # Window Position Registers(WH1)
        self.WH2     = 0    # Window Position Registers(WH2)
        self.WH3     = 0    # Window Position Registers(WH3)
        self.WBGLOG_8  = 0    # Window Mask Logic Registers(BG)
        self.WOBJLOG_8 = 0    # Window Mask Logic Registers(OBJ)
        self.TM_8      = 0    # Screen Destination Registers
        self.TS_8      = 0    # Screen Destination Registers
        self.TMW_8     = 0    # Window Mask Destination Registers
        self.TSW_8     = 0    # Window Mask Destination Registers
        self.CGWSEL_8  = 0    # Color Math Registers
        self.CGADSUB_8 = 0    # Color Math Registers
        self.COLDATA_8 = 0    # Color Math Registers
        self.SETINI_8  = 0    # Screen Mode Select Register
        self.MPYL    = 0    # Multiplication Result Registers
        self.MPYM    = 0    # Multiplication Result Registers
        self.MPYH    = 0    # Multiplication Result Registers
        self.SLHV    = 0    # Software Latch Register
        self.OAMDATAREAD = 0 # OAM Data Read Register
        self.VMDATALREAD = 0 # VRAM Data Read Register(Low)
        self.VMDATAHREAD = 0 # VRAM Data Read Register(High)
        self.CGDATAREAD  = 0 # CGRAM Data Read Register
        self.OPHCT   = 0    # Scanline Location Registers(Horizontal)
        self.OPVCT   = 0    # Scanline Location Registers(Vertical)
        self.STAT77  = 0    # PPU Status Register
        self.STAT78  = 0    # PPU Status Register
        self.APUIO0  = 0    # APU IO Registers
        self.APUIO1  = 0    # APU IO Registers
        self.APUIO2  = 0    # APU IO Registers
        self.APUIO3  = 0    # APU IO Registers
        self.WMDATA  = 0    # WRAM Data Register
        self.WMADDL  = 0    # WRAM Address Registers
        self.WMADDM  = 0    # WRAM Address Registers
        self.WMADDH  = 0    # WRAM Address Registers

    # called by the memory mapper
    def read(self, address):
        if address == 0x2100:
            return self.INIDISP_8 # Screen Display Register
        elif address == 0x2101:
            return self.OBSEL_8   # Object Size and Character Size Register
        elif address == 0x2102:
            return self.OAMADDL     # OAM Address Registers(Low)
        elif address == 0x2103:
            return self.OAMADDH     # OAM Address Registers(High)
        elif address == 0x2104:
            return self.OAMDATA     # OAM Data Write Register
        elif address == 0x2105:
            return self.BGMODE_8      # BG Mode and Character Size Register
        elif address == 0x2106:
            return self.MOSAIC_8      # Mosaic Register
        elif address == 0x2107:
            return self.BG1SC_8       # BG Tilemap Address Registers(BG1)
        elif address == 0x2108:
            return self.BG2SC_8       # BG Tilemap Address Registers(BG2)
        elif address == 0x2109:
            return self.BG3SC_8       # BG Tilemap Address Registers(BG3)
        elif address == 0x210A:
            return self.BG4SC_8       # BG Tilemap Address Registers(BG4)
        elif address == 0x210B:
            return self.BG12NBA_8     # BG Character Address Registers(BG1 & 2)
        elif address == 0x210C:
            return self.BG34NBA_8     # BG Character Address Registers(BG3 & 4)
        elif address == 0x210D:
            return self.BG1HOFS_16     # BG Scroll Registers(BG1)
        elif address == 0x210E:
            return self.BG1VOFS_16     # BG Scroll Registers(BG1)
        elif address == 0x210F:
            return self.BG2HOFS_16     # BG Scroll Registers(BG2)
        elif address == 0x2110:
            return self.BG2VOFS_16     # BG Scroll Registers(BG2)
        elif address == 0x2111:
            return self.BG3HOFS_16     # BG Scroll Registers(BG3)
        elif address == 0x2112:
            return self.BG3VOFS_16     # BG Scroll Registers(BG3)
        elif address == 0x2113:
            return self.BG4HOFS_16     # BG Scroll Registers(BG4)
        elif address == 0x2114:
            return self.BG4VOFS_16     # BG Scroll Registers(BG4)
        elif address == 0x2115:
            return self.VMAIN       # Video Port Control Register
        elif address == 0x2116:
            return self.VMADDL      # VRAM Address Registers(Low)
        elif address == 0x2117:
            return self.VMADDH      # VRAM Address Registers(High)
        elif address == 0x2118:
            return self.VMDATAL     # VRAM Data Write Registers(Low)
        elif address == 0x2119:
            return self.VMDATAH     # VRAM Data Write Registers(High)
        elif address == 0x211A:
            return self.M7SEL_8       # Mode 7 Settings Register
        elif address == 0x211B:
            return self.M7A_16         # Mode 7 Matrix Registers
        elif address == 0x211C:
            return self.M7B_16         # Mode 7 Matrix Registers
        elif address == 0x211D:
            return self.M7C_16         # Mode 7 Matrix Registers
        elif address == 0x211E:
            return self.M7D_16         # Mode 7 Matrix Registers
        elif address == 0x211F:
            return self.M7X_16         # Mode 7 Matrix Registers
        elif address == 0x2120:
            return self.M7Y_16         # Mode 7 Matrix Registers
        elif address == 0x2121:
            return self.CGADD       # CGRAM Address Register
        elif address == 0x2122:
            return self.CGDATA      # CGRAM Data Write Register
        elif address == 0x2123:
            return self.W12SEL_8      # Window Mask Settings Registers
        elif address == 0x2124:
            return self.W34SEL_8      # Window Mask Settings Registers
        elif address == 0x2125:
            return self.WOBJSEL_8     # Window Mask Settings Registers
        elif address == 0x2126:
            return self.WH0         # Window Position Registers(WH0)
        elif address == 0x2127:
            return self.WH1         # Window Position Registers(WH1)
        elif address == 0x2128:
            return self.WH2         # Window Position Registers(WH2)
        elif address == 0x2129:
            return self.WH3         # Window Position Registers(WH3)
        elif address == 0x212A:
            return self.WBGLOG_8      # Window Mask Logic Registers(BG)
        elif address == 0x212B:
            return self.WOBJLOG_8     # Window Mask Logic Registers(OBJ)
        elif address == 0x212C:
            return self.TM_8          # Screen Destination Registers
        elif address == 0x212D:
            return self.TS_8          # Screen Destination Registers
        elif address == 0x212E:
            return self.TMW_8         # Window Mask Destination Registers
        elif address == 0x212F:
            return self.TSW_8         # Window Mask Destination Registers
        elif address == 0x2130:
            return self.CGWSEL_8      # Color Math Registers
        elif address == 0x2131:
            return self.CGADSUB_8     # Color Math Registers
        elif address == 0x2132:
            return self.COLDATA_8     # Color Math Registers
        elif address == 0x2133:
            return self.SETINI_8      # Screen Mode Select Register
        elif address == 0x2134:
            return self.MPYL        # Multiplication Result Registers
        elif address == 0x2135:
            return self.MPYM        # Multiplication Result Registers
        elif address == 0x2136:
            return self.MPYH        # Multiplication Result Registers
        elif address == 0x2137:
            return self.SLHV        # Software Latch Register
        elif address == 0x2138:
            return self.OAMDATAREAD # OAM Data Read Register
        elif address == 0x2139:
            return self.VMDATALREAD # VRAM Data Read Register(Low)
        elif address == 0x213A:
            return self.VMDATAHREAD # VRAM Data Read Register(High)
        elif address == 0x213B:
            return self.CGDATAREAD  # CGRAM Data Read Register
        elif address == 0x213C:
            return self.OPHCT       # Scanline Location Registers(Horizontal)
        elif address == 0x213D:
            return self.OPVCT       # Scanline Location Registers(Vertical)
        elif address == 0x213E:
            return self.STAT77      # PPU Status Register
        elif address == 0x213F:
            return self.STAT78      # PPU Status Register
        elif address == 0x2140:
            return self.APUIO0      # APU IO Registers
        elif address == 0x2141:
            return self.APUIO1      # APU IO Registers
        elif address == 0x2142:
            return self.APUIO2      # APU IO Registers
        elif address == 0x2143:
            return self.APUIO3      # APU IO Registers
        elif address == 0x2180:
            return self.WMDATA      # WRAM Data Register
        elif address == 0x2181:
            return self.WMADDL      # WRAM Address Registers
        elif address == 0x2182:
            return self.WMADDM      # WRAM Address Registers
        elif address == 0x2183:
            return self.WMADDH      # WRAM Address Registers
        print("Error read PPU Address: "+ hex(address))
        return 0

    # called by the memory mapper
    def write(self, address, value):
        if address == 0x2100:
            self.INIDISP_8 = value    # Screen Display Register
            return
        elif address == 0x2101:
            self.OBSEL_8  = value     # Object Size and Character Size Register
            return
        elif address == 0x2102:
            self.OAMADDL  = value   # OAM Address Registers(Low)
            return
        elif address == 0x2103:
            self.OAMADDH = value    # OAM Address Registers(High)
            return
        elif address == 0x2104:
            self.OAMDATA = value    # OAM Data Write Register
            return
        elif address == 0x2105:
            self.BGMODE_8  = value    # BG Mode and Character Size Register
            return
        elif address == 0x2106:
            self.MOSAIC_8  = value    # Mosaic Register
            return
        elif address == 0x2107:
            self.BG1SC_8   = value    # BG Tilemap Address Registers(BG1)
            return
        elif address == 0x2108:
            self.BG2SC_8   = value    # BG Tilemap Address Registers(BG2)
            return
        elif address == 0x2109:
            self.BG3SC_8   = value    # BG Tilemap Address Registers(BG3)
            return
        elif address == 0x210A:
            self.BG4SC_8   = value    # BG Tilemap Address Registers(BG4)
            return
        elif address == 0x210B:
            self.BG12NBA_8 = value    # BG Character Address Registers(BG1 & 2)
            return
        elif address == 0x210C:
            self.BG34NBA_8 = value    # BG Character Address Registers(BG3 & 4)
            return
        elif address == 0x210D:
            self.BG1HOFS_16 = value    # BG Scroll Registers(BG1)
            return
        elif address == 0x210E:
            self.BG1VOFS_16 = value    # BG Scroll Registers(BG1)
            return
        elif address == 0x210F:
            self.BG2HOFS_16 = value    # BG Scroll Registers(BG2)
            return
        elif address == 0x2110:
            self.BG2VOFS_16 = value    # BG Scroll Registers(BG2)
            return
        elif address == 0x2111:
            self.BG3HOFS_16 = value    # BG Scroll Registers(BG3)
            return
        elif address == 0x2112:
            self.BG3VOFS_16 = value    # BG Scroll Registers(BG3)
            return
        elif address == 0x2113:
            self.BG4HOFS_16 = value    # BG Scroll Registers(BG4)
            return
        elif address == 0x2114:
            self.BG4VOFS_16 = value    # BG Scroll Registers(BG4)
            return
        elif address == 0x2115:
            self.VMAIN   = value    # Video Port Control Register
            return
        elif address == 0x2116:
            self.VMADDL  = value    # VRAM Address Registers(Low)
            return
        elif address == 0x2117:
            self.VMADDH  = value    # VRAM Address Registers(High)
            return
        elif address == 0x2118:
            self.VMDATAL = value    # VRAM Data Write Registers(Low)
            return
        elif address == 0x2119:
            self.VMDATAH = value    # VRAM Data Write Registers(High)
            return
        elif address == 0x211A:
            self.M7SEL_8   = value    # Mode 7 Settings Register
            return
        elif address == 0x211B:
            self.M7A_16     = value    # Mode 7 Matrix Registers
            return
        elif address == 0x211C:
            self.M7B_16     = value    # Mode 7 Matrix Registers
            return
        elif address == 0x211D:
            self.M7C_16     = value    # Mode 7 Matrix Registers
            return
        elif address == 0x211E:
            self.M7D_16     = value    # Mode 7 Matrix Registers
            return
        elif address == 0x211F:
            self.M7X_16     = value    # Mode 7 Matrix Registers
            return
        elif address == 0x2120:
            self.M7Y_16     = value    # Mode 7 Matrix Registers
            return
        elif address == 0x2121:
            self.CGADD   = value    # CGRAM Address Register
            return
        elif address == 0x2122:
            self.CGDATA  = value    # CGRAM Data Write Register
            return
        elif address == 0x2123:
            self.W12SEL_8  = value    # Window Mask Settings Registers
            return
        elif address == 0x2124:
            self.W34SEL_8  = value    # Window Mask Settings Registers
            return
        elif address == 0x2125:
            self.WOBJSEL_8 = value    # Window Mask Settings Registers
            return
        elif address == 0x2126:
            self.WH0     = value    # Window Position Registers(WH0)
            return
        elif address == 0x2127:
            self.WH1     = value   # Window Position Registers(WH1)
            return
        elif address == 0x2128:
            self.WH2     = value    # Window Position Registers(WH2)
            return
        elif address == 0x2129:
            self.WH3     = value    # Window Position Registers(WH3)
            return
        elif address == 0x212A:
            self.WBGLOG_8  = value    # Window Mask Logic Registers(BG)
            return
        elif address == 0x212B:
            self.WOBJLOG_8 = value    # Window Mask Logic Registers(OBJ)
            return
        elif address == 0x212C:
            self.TM_8      = value    # Screen Destination Registers
            return
        elif address == 0x212D:
            self.TS_8      = value    # Screen Destination Registers
            return
        elif address == 0x212E:
            self.TMW_8     = value    # Window Mask Destination Registers
            return
        elif address == 0x212F:
            self.TSW_8     = value    # Window Mask Destination Registers
            return
        elif address == 0x2130:
            self.CGWSEL_8  = value    # Color Math Registers
            return
        elif address == 0x2131:
            self.CGADSUB_8 = value    # Color Math Registers
            return
        elif address == 0x2132:
            self.COLDATA_8 = value    # Color Math Registers
            return
        elif address == 0x2133:
            self.SETINI_8  = value    # Screen Mode Select Register
            return
        elif address == 0x2134:
            self.MPYL    = value    # Multiplication Result Registers
            return
        elif address == 0x2135:
            self.MPYM    = value    # Multiplication Result Registers
            return
        elif address == 0x2136:
            self.MPYH    = value    # Multiplication Result Registers
            return
        elif address == 0x2137:
            self.SLHV    = value    # Software Latch Register
            return
        elif address == 0x2138:
            self.OAMDATAREAD = value # OAM Data Read Register
            return
        elif address == 0x2139:
            self.VMDATALREAD = value # VRAM Data Read Register(Low)
            return
        elif address == 0x213A:
            self.VMDATAHREAD = value # VRAM Data Read Register(High)
            return
        elif address == 0x213B:
            self.CGDATAREAD  = value # CGRAM Data Read Register
            return
        elif address == 0x213C:
            self.OPHCT   = value    # Scanline Location Registers(Horizontal)
            return
        elif address == 0x213D:
            self.OPVCT   = value    # Scanline Location Registers(Vertical)
            return
        elif address == 0x213E:
            self.STAT77  = value    # PPU Status Register
            return
        elif address == 0x213F:
            self.STAT78  = value    # PPU Status Register
            return
        elif address == 0x2140:
            self.APUIO0  = value    # APU IO Registers
            return
        elif address == 0x2141:
            self.APUIO1  = value    # APU IO Registers
            return
        elif address == 0x2142:
            self.APUIO2  = value    # APU IO Registers
            return
        elif address == 0x2143:
            self.APUIO3  = value    # APU IO Registers
            return
        elif address == 0x2180:
            self.WMDATA  = value    # WRAM Data Register
            return
        elif address == 0x2181:
            self.WMADDL  = value    # WRAM Address Registers
            return
        elif address == 0x2182:
            self.WMADDM  = value    # WRAM Address Registers
            return
        elif address == 0x2183:
            self.WMADDH  = value    # WRAM Address Registers
            return
        print("Error write PPU Address: " + hex(address)+str(value))
        return