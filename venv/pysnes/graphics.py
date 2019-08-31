from rsdl import RSDL, RSDL_helper  # , RMix
from rpython.rtyper.lltypesystem import lltype, rffi

class PictureProcessingUnit(object):
    COLOR_MAP = [(0xff, 0xff, 0xff), (0xCC, 0xCC, 0xCC), (0x66, 0x66, 0x66), (0, 0, 0)]

    def init(self):
        self.scale = 4
        self.width = 256
        self.height = 240
        self.init_sdl()
        self.create_screen()
        #self.update_display()
        get_ticks = RSDL.GetTicks
        def delay(secs):
            return RSDL.Delay(int(secs * 1000))
        self.poll_event()
        self.update_display()
        #while True:
        #     pass

    def init_sdl(self):
        assert RSDL.Init(RSDL.INIT_VIDEO) >= 0
        self.event = lltype.malloc(RSDL.Event, flavor='raw')

    def create_screen(self):
        # 32 bits per pixel
        # 0 no flags
        self.screen = RSDL.SetVideoMode(self.width*self.scale, self.height*self.scale, 32, 0)
        fmt = self.screen.c_format
        self.colors = []
        for color in self.COLOR_MAP:
            color = RSDL.MapRGB(fmt, *color)
            self.colors.append(color)
        self.blit_rect = RSDL_helper.mallocrect(0, 0, self.scale, self.scale)

    def update_display(self):
        RSDL.LockSurface(self.screen)
        self.draw_pixel(0,0,0)
        RSDL.UnlockSurface(self.screen)
        RSDL.Flip(self.screen)

    def draw_pixel(self, x, y, color):
        color = self.colors[color]
        start_x = x * self.scale
        start_y = y * self.scale
        dstrect = self.blit_rect
        rffi.setintfield(dstrect, 'c_x',  start_x)
        rffi.setintfield(dstrect, 'c_y',  start_y)
        RSDL.FillRect(self.screen, dstrect, color)

    def handle_execution_error(self, error):
        lltype.free(self.event, flavor='raw')
        RSDL.Quit()

    def poll_event(self):
        ok = rffi.cast(lltype.Signed, RSDL.PollEvent(self.event))
        return ok > 0