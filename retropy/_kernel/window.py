# mainlib
import pygame as pg


class Window:
    def __init__(self, kernel):
        self.kernel = kernel
        self.size   = pg.Vector2(100)
        self.flags  = 0

        self.name   = "Kernel Window"
        self.color  = "black"

        self.does_update = False

        self.focus = False
        self.focus_just_gain = False
        self.focus_just_lost = False

        self.active = pg.display.get_active()
        self.just_active = False
        
    def create(self):
        print("[Kernel] Windows is going to setup")
        self.kernel.screen = pg.display.set_mode(self.size, self.flags)
        pg.display.set_caption(self.name)
        print("[Kernel] Windows has been setup")
    
    def refresh(self):
        self.focus_just_gain = False
        self.focus_just_lost = False

        # window
        if self.does_update:    pg.display.update()
        else:                   pg.display.flip()

        display_is_active = pg.display.get_active()

        self.just_active = display_is_active != self.active and not self.active
        self.active = display_is_active
        self.size = pg.Vector2(pg.display.get_window_size())

    
