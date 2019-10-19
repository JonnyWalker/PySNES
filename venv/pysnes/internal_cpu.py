class InternalCPURegisters(object):
    def __init__(self):
        self.NMITIMEN_8 = 0   # Interrupt Enable Register
        self.WRIO = 0       # IO Port Write Register
        self.WRMPYA = 0     # Multiplicand Registers
        self.WRMPYB = 0     # Multiplicand Registers
        self.WRDIVL = 0     # Divisor & Dividend Registers
        self.WRDIVH = 0     # Divisor & Dividend Registers
        self.WRDIVB = 0     # Divisor & Dividend Registers
        self.HTIMEL = 0     # IRQ Timer Registers(Horizontal - Low)
        self.HTIMEH = 0     # IRQ Timer Registers(Horizontal - High)
        self.VTIMEL = 0     # IRQ Timer Registers(Vertical - Low)
        self.VTIMEH = 0     # IRQ Timer Registers(Vertical - High)
        self.MDMAEN_8 = 0     # DMA Enable Register
        self.HDMAEN_8 = 0     # HDMA Enable Register
        self.MEMSEL_8 = 0     # ROM Speed Register
        self.RDNMI  = 0     # Interrupt Flag Registers
        self.TIMEUP = 0     # Interrupt Flag Registers
        self.HVBJOY = 0     # PPU Status Register
        self.RDIO   = 0     # IO Port Read Register
        self.RDDIVL = 0     # Multiplication Or Divide Result Registers(Low)
        self.RDDIVH = 0     # Multiplication Or Divide Result Registers(High)
        self.RDMPYL = 0     # Multiplication Or Divide Result Registers(Low)
        self.RDMPYH = 0     # Multiplication Or Divide Result Registers(High)
        self.JOY1L_8  = 0     # Controller Port Data Registers(Pad1 - Low)
        self.JOY1H_8  = 0     # Controller Port Data Registers(Pad1 - High)
        self.JOY2L_8  = 0     # Controller Port Data Registers(Pad2 - Low)
        self.JOY2H_8  = 0     # Controller Port Data Registers(Pad2 - High)
        self.JOY3L_8  = 0     # Controller Port Data Registers(Pad3 - Low)
        self.JOY3H_8  = 0     # Controller Port Data Registers(Pad3 - High)
        self.JOY4L_8  = 0     # Controller Port Data Registers(Pad4 - Low)
        self.JOY4H_8  = 0     # Controller Port Data Registers(Pad4 - High)


    # called by the memory mapper
    def read(self, address):
        if address == 0x4200 :
            return self.NMITIMEN_8    # Interrupt Enable Register
        elif address == 0x4201:
            return self.WRIO        # IO Port Write Register
        elif address == 0x4202:
            return self.WRMPYA      # Multiplicand Registers
        elif address == 0x4203:
            return self.WRMPYB      # Multiplicand Registers
        elif address == 0x4204:
            return self.WRDIVL      # Divisor & Dividend Registers
        elif address == 0x4205:
            return self.WRDIVH      # Divisor & Dividend Registers
        elif address == 0x4206:
            return self.WRDIVB      # Divisor & Dividend Registers
        elif address == 0x4207:
            return self.HTIMEL      # IRQ Timer Registers(Horizontal - Low)
        elif address == 0x4208:
            return self.HTIMEH      # IRQ Timer Registers(Horizontal - High)
        elif address == 0x4209:
            return self.VTIMEL      # IRQ Timer Registers(Vertical - Low)
        elif address == 0x420A:
            return self.VTIMEH      # IRQ Timer Registers(Vertical - High)
        elif address == 0x420B:
            return self.MDMAEN_8      # DMA Enable Register
        elif address == 0x420C:
            return self.HDMAEN_8      # HDMA Enable Register
        elif address == 0x420D:
            return self.MEMSEL_8      # ROM Speed Register
        elif address == 0x4210:
            return self.RDNMI       # Interrupt Flag Registers
        elif address == 0x4211:
            return self.TIMEUP      # Interrupt Flag Registers
        elif address == 0x4212:
            return self.HVBJOY      # PPU Status Register
        elif address == 0x4213:
            return self.RDIO        # IO Port Read Register
        elif address == 0x4214:
            return self.RDDIVL      # Multiplication Or Divide Result Registers(Low)
        elif address == 0x4215:
            return self.RDDIVH      # Multiplication Or Divide Result Registers(High)
        elif address == 0x4216:
            return self.RDMPYL      # Multiplication Or Divide Result Registers(Low)
        elif address == 0x4217:
            return self.RDMPYH      # Multiplication Or Divide Result Registers(High)
        elif address == 0x4218:
            return self.JOY1L_8       # Controller Port Data Registers(Pad1 - Low)
        elif address == 0x4219:
            return self.JOY1H_8       # Controller Port Data Registers(Pad1 - High)
        elif address == 0x421A:
            return self.JOY2L_8       # Controller Port Data Registers(Pad2 - Low)
        elif address == 0x421B:
            return self.JOY2H_8       # Controller Port Data Registers(Pad2 - High)
        elif address == 0x421C:
            return self.JOY3L_8       # Controller Port Data Registers(Pad3 - Low)
        elif address == 0x421D:
            return self.JOY3H_8       # Controller Port Data Registers(Pad3 - High)
        elif address == 0x421E:
            return self.JOY4L_8       # Controller Port Data Registers(Pad4 - Low)
        elif address == 0x421F:
            return self.JOY4H_8       # Controller Port Data Registers(Pad4 - High)
        print("Error read Internal CPU Address: " + hex(address))
        return 0

    # called by the memory mapper
    def write(self, address, value):
        if address == 0x4200 :
            self.NMITIMEN_8 = value    # Interrupt Enable Register
            return
        elif address == 0x4201:
            self.WRIO = value        # IO Port Write Register
            return
        elif address == 0x4202:
            self.WRMPYA = value      # Multiplicand Registers
            return
        elif address == 0x4203:
            self.WRMPYB = value      # Multiplicand Registers
            return
        elif address == 0x4204:
            self.WRDIVL = value      # Divisor & Dividend Registers
            return
        elif address == 0x4205:
            self.WRDIVH = value      # Divisor & Dividend Registers
            return
        elif address == 0x4206:
            self.WRDIVB = value      # Divisor & Dividend Registers
            return
        elif address == 0x4207:
            self.HTIMEL = value      # IRQ Timer Registers(Horizontal - Low)
            return
        elif address == 0x4208:
            self.HTIMEH = value      # IRQ Timer Registers(Horizontal - High)
            return
        elif address == 0x4209:
            self.VTIMEL = value      # IRQ Timer Registers(Vertical - Low)
            return
        elif address == 0x420A:
            self.VTIMEH = value      # IRQ Timer Registers(Vertical - High)
            return
        elif address == 0x420B:
            self.MDMAEN_8 = value      # DMA Enable Register
            return
        elif address == 0x420C:
            self.HDMAEN_8 = value      # HDMA Enable Register
            return
        elif address == 0x420D:
            self.MEMSEL_8 = value      # ROM Speed Register
            return
        elif address == 0x4210:
            self.RDNMI  = value      # Interrupt Flag Registers
            return
        elif address == 0x4211:
            self.TIMEUP = value      # Interrupt Flag Registers
            return
        elif address == 0x4212:
            self.HVBJOY = value      # PPU Status Register
            return
        elif address == 0x4213:
            self.RDIO = value        # IO Port Read Register
            return
        elif address == 0x4214:
            self.RDDIVL = value      # Multiplication Or Divide Result Registers(Low)
            return
        elif address == 0x4215:
            self.RDDIVH = value      # Multiplication Or Divide Result Registers(High)
            return
        elif address == 0x4216:
            self.RDMPYL = value      # Multiplication Or Divide Result Registers(Low)
            return
        elif address == 0x4217:
            self.RDMPYH = value      # Multiplication Or Divide Result Registers(High)
            return
        elif address == 0x4218:
            self.JOY1L_8 = value       # Controller Port Data Registers(Pad1 - Low)
            return
        elif address == 0x4219:
            self.JOY1H_8 = value       # Controller Port Data Registers(Pad1 - High)
            return
        elif address == 0x421A:
            self.JOY2L_8 = value       # Controller Port Data Registers(Pad2 - Low)
            return
        elif address == 0x421B:
            self.JOY2H_8 = value       # Controller Port Data Registers(Pad2 - High)
            return
        elif address == 0x421C:
            self.JOY3L_8 = value       # Controller Port Data Registers(Pad3 - Low)
            return
        elif address == 0x421D:
            self.JOY3H_8 = value       # Controller Port Data Registers(Pad3 - High)
            return
        elif address == 0x421E:
            self.JOY4L_8 = value       # Controller Port Data Registers(Pad4 - Low)
            return
        elif address == 0x421F:
            self.JOY4H_8 = value       # Controller Port Data Registers(Pad4 - High)
            return
        print("Error write Internal CPU Address: " + hex(address) + value(value))
