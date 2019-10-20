class PPU(object):
    def __init__(self):
        self.INIDISP_8 = 0      # Screen Display Register
        self.OBSEL_8   = 0      # Object Size and Character Size Register
        self.OAMADDL_8 = 0      # OAM Address Registers(Low)
        self.OAMADDH_8 = 0      # OAM Address Registers(High)
        self.OAMDATA_8 = 0      # OAM Data Write Register
        self.BGMODE_8  = 0      # BG Mode and Character Size Register
        self.MOSAIC_8  = 0      # Mosaic Register
        self.BG1SC_8   = 0      # BG Tilemap Address Registers(BG1)
        self.BG2SC_8   = 0      # BG Tilemap Address Registers(BG2)
        self.BG3SC_8   = 0      # BG Tilemap Address Registers(BG3)
        self.BG4SC_8   = 0      # BG Tilemap Address Registers(BG4)
        self.BG12NBA_8 = 0      # BG Character Address Registers(BG1 & 2)
        self.BG34NBA_8 = 0      # BG Character Address Registers(BG3 & 4)
        self.BG1HOFS_16 = 0     # BG Scroll Registers(BG1)
        self.BG1VOFS_16 = 0     # BG Scroll Registers(BG1)
        self.BG2HOFS_16 = 0     # BG Scroll Registers(BG2)
        self.BG2VOFS_16 = 0     # BG Scroll Registers(BG2)
        self.BG3HOFS_16 = 0     # BG Scroll Registers(BG3)
        self.BG3VOFS_16 = 0     # BG Scroll Registers(BG3)
        self.BG4HOFS_16 = 0     # BG Scroll Registers(BG4)
        self.BG4VOFS_16 = 0     # BG Scroll Registers(BG4)
        self.VMAIN_8   = 0      # Video Port Control Register
        self.VMADDL_8  = 0      # VRAM Address Registers(Low)
        self.VMADDH_8  = 0      # VRAM Address Registers(High)
        self.VMDATAL_8 = 0      # VRAM Data Write Registers(Low)
        self.VMDATAH_8 = 0      # VRAM Data Write Registers(High)
        self.M7SEL_8   = 0      # Mode 7 Settings Register
        self.M7A_16     = 0     # Mode 7 Matrix Registers
        self.M7B_16     = 0     # Mode 7 Matrix Registers
        self.M7C_16     = 0     # Mode 7 Matrix Registers
        self.M7D_16     = 0     # Mode 7 Matrix Registers
        self.M7X_16     = 0     # Mode 7 Matrix Registers
        self.M7Y_16     = 0     # Mode 7 Matrix Registers
        self.CGADD_8   = 0      # CGRAM Address Register
        self.CGDATA_16  = 0     # CGRAM Data Write Register
        self.W12SEL_8  = 0      # Window Mask Settings Registers
        self.W34SEL_8  = 0      # Window Mask Settings Registers
        self.WOBJSEL_8 = 0      # Window Mask Settings Registers
        self.WH0_8     = 0      # Window Position Registers(WH0)
        self.WH1_8     = 0      # Window Position Registers(WH1)
        self.WH2_8     = 0      # Window Position Registers(WH2)
        self.WH3_8     = 0      # Window Position Registers(WH3)
        self.WBGLOG_8  = 0      # Window Mask Logic Registers(BG)
        self.WOBJLOG_8 = 0      # Window Mask Logic Registers(OBJ)
        self.TM_8      = 0      # Screen Destination Registers
        self.TS_8      = 0      # Screen Destination Registers
        self.TMW_8     = 0      # Window Mask Destination Registers
        self.TSW_8     = 0      # Window Mask Destination Registers
        self.CGWSEL_8  = 0      # Color Math Registers
        self.CGADSUB_8 = 0      # Color Math Registers
        self.COLDATA_8 = 0      # Color Math Registers
        self.SETINI_8  = 0      # Screen Mode Select Register
        self.MPYL_8    = 0      # Multiplication Result Registers
        self.MPYM_8    = 0      # Multiplication Result Registers
        self.MPYH_8    = 0      # Multiplication Result Registers
        self.SLHV_8    = 0      # Software Latch Register
        self.OAMDATAREAD_8 = 0  # OAM Data Read Register
        self.VMDATALREAD_8 = 0  # VRAM Data Read Register(Low)
        self.VMDATAHREAD_8 = 0  # VRAM Data Read Register(High)
        self.CGDATAREAD_16  = 0 # CGRAM Data Read Register
        self.OPHCT_16   = 0     # Scanline Location Registers(Horizontal); actually only 9 bit, rest from PPU2 bus
        self.OPVCT_16   = 0     # Scanline Location Registers(Vertical); atually only 9 bit, rest from PPU2 bus
        self.STAT77_8  = 0      # PPU Status Register
        self.STAT78_8  = 0      # PPU Status Register
        self.APUIO0_8  = 0      # APU IO Registers
        self.APUIO1_8  = 0      # APU IO Registers
        self.APUIO2_8  = 0      # APU IO Registers
        self.APUIO3_8  = 0      # APU IO Registers
        self.WMDATA_8  = 0      # WRAM Data Register
        self.WMADDL_8  = 0      # WRAM Address Registers
        self.WMADDM_8  = 0      # WRAM Address Registers
        self.WMADDH_8  = 0      # WRAM Address Registers

    # called by the memory mapper
    def read(self, address):
        if address == 0x2100:
            return self.INIDISP_8 # Screen Display Register
        elif address == 0x2101:
            return self.OBSEL_8   # Object Size and Character Size Register
        elif address == 0x2102:
            return self.OAMADDL_8     # OAM Address Registers(Low)
        elif address == 0x2103:
            return self.OAMADDH_8     # OAM Address Registers(High)
        elif address == 0x2104:
            return self.OAMDATA_8     # OAM Data Write Register
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
            return self.VMAIN_8       # Video Port Control Register
        elif address == 0x2116:
            return self.VMADDL_8      # VRAM Address Registers(Low)
        elif address == 0x2117:
            return self.VMADDH_8      # VRAM Address Registers(High)
        elif address == 0x2118:
            return self.VMDATAL_8     # VRAM Data Write Registers(Low)
        elif address == 0x2119:
            return self.VMDATAH_8     # VRAM Data Write Registers(High)
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
            return self.CGADD_8       # CGRAM Address Register
        elif address == 0x2122:
            return self.CGDATA_16      # CGRAM Data Write Register
        elif address == 0x2123:
            return self.W12SEL_8      # Window Mask Settings Registers
        elif address == 0x2124:
            return self.W34SEL_8      # Window Mask Settings Registers
        elif address == 0x2125:
            return self.WOBJSEL_8     # Window Mask Settings Registers
        elif address == 0x2126:
            return self.WH0_8         # Window Position Registers(WH0)
        elif address == 0x2127:
            return self.WH1_8         # Window Position Registers(WH1)
        elif address == 0x2128:
            return self.WH2_8         # Window Position Registers(WH2)
        elif address == 0x2129:
            return self.WH3_8         # Window Position Registers(WH3)
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
            return self.MPYL_8        # Multiplication Result Registers
        elif address == 0x2135:
            return self.MPYM_8        # Multiplication Result Registers
        elif address == 0x2136:
            return self.MPYH_8        # Multiplication Result Registers
        elif address == 0x2137:
            return self.SLHV_8        # Software Latch Register
        elif address == 0x2138:
            return self.OAMDATAREAD_8 # OAM Data Read Register
        elif address == 0x2139:
            return self.VMDATALREAD_8 # VRAM Data Read Register(Low)
        elif address == 0x213A:
            return self.VMDATAHREAD_8 # VRAM Data Read Register(High)
        elif address == 0x213B:
            return self.CGDATAREAD_16  # CGRAM Data Read Register
        elif address == 0x213C:
            return self.OPHCT_16       # Scanline Location Registers(Horizontal)
        elif address == 0x213D:
            return self.OPVCT_16       # Scanline Location Registers(Vertical)
        elif address == 0x213E:
            return self.STAT77_8      # PPU Status Register
        elif address == 0x213F:
            return self.STAT78_8      # PPU Status Register
        elif address == 0x2140:
            return self.APUIO0_8      # APU IO Registers
        elif address == 0x2141:
            return self.APUIO1_8      # APU IO Registers
        elif address == 0x2142:
            return self.APUIO2_8      # APU IO Registers
        elif address == 0x2143:
            return self.APUIO3_8      # APU IO Registers
        elif address == 0x2180:
            return self.WMDATA_8      # WRAM Data Register
        elif address == 0x2181:
            return self.WMADDL_8      # WRAM Address Registers
        elif address == 0x2182:
            return self.WMADDM_8      # WRAM Address Registers
        elif address == 0x2183:
            return self.WMADDH_8      # WRAM Address Registers
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
            self.OAMADDL_8  = value   # OAM Address Registers(Low)
            return
        elif address == 0x2103:
            self.OAMADDH_8 = value    # OAM Address Registers(High)
            return
        elif address == 0x2104:
            self.OAMDATA_8 = value    # OAM Data Write Register
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
            self.VMAIN_8   = value    # Video Port Control Register
            return
        elif address == 0x2116:
            self.VMADDL_8  = value    # VRAM Address Registers(Low)
            return
        elif address == 0x2117:
            self.VMADDH_8  = value    # VRAM Address Registers(High)
            return
        elif address == 0x2118:
            self.VMDATAL_8 = value    # VRAM Data Write Registers(Low)
            return
        elif address == 0x2119:
            self.VMDATAH_8 = value    # VRAM Data Write Registers(High)
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
            self.CGADD_8   = value    # CGRAM Address Register
            return
        elif address == 0x2122:
            self.CGDATA_16  = value    # CGRAM Data Write Register
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
            self.WH0_8     = value    # Window Position Registers(WH0)
            return
        elif address == 0x2127:
            self.WH1_8     = value   # Window Position Registers(WH1)
            return
        elif address == 0x2128:
            self.WH2_8     = value    # Window Position Registers(WH2)
            return
        elif address == 0x2129:
            self.WH3_8     = value    # Window Position Registers(WH3)
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
            self.MPYL_8    = value    # Multiplication Result Registers
            return
        elif address == 0x2135:
            self.MPYM_8    = value    # Multiplication Result Registers
            return
        elif address == 0x2136:
            self.MPYH_8    = value    # Multiplication Result Registers
            return
        elif address == 0x2137:
            self.SLHV_8    = value    # Software Latch Register
            return
        elif address == 0x2138:
            self.OAMDATAREAD_8 = value # OAM Data Read Register
            return
        elif address == 0x2139:
            self.VMDATALREAD_8 = value # VRAM Data Read Register(Low)
            return
        elif address == 0x213A:
            self.VMDATAHREAD_8 = value # VRAM Data Read Register(High)
            return
        elif address == 0x213B:
            self.CGDATAREAD_16  = value # CGRAM Data Read Register
            return
        elif address == 0x213C:
            self.OPHCT_16   = value    # Scanline Location Registers(Horizontal)
            return
        elif address == 0x213D:
            self.OPVCT_16   = value    # Scanline Location Registers(Vertical)
            return
        elif address == 0x213E:
            self.STAT77_8  = value    # PPU Status Register
            return
        elif address == 0x213F:
            self.STAT78_8  = value    # PPU Status Register
            return
        elif address == 0x2140:
            self.APUIO0_8  = value    # APU IO Registers
            return
        elif address == 0x2141:
            self.APUIO1_8  = value    # APU IO Registers
            return
        elif address == 0x2142:
            self.APUIO2_8  = value    # APU IO Registers
            return
        elif address == 0x2143:
            self.APUIO3_8  = value    # APU IO Registers
            return
        elif address == 0x2180:
            self.WMDATA_8  = value    # WRAM Data Register
            return
        elif address == 0x2181:
            self.WMADDL_8  = value    # WRAM Address Registers
            return
        elif address == 0x2182:
            self.WMADDM_8  = value    # WRAM Address Registers
            return
        elif address == 0x2183:
            self.WMADDH_8  = value    # WRAM Address Registers
            return
        print("Error write PPU Address: " + hex(address)+str(value))
        return