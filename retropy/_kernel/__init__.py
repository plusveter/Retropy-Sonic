# mainlib
import numpy as np
import pygame as pg

# call from inside the kernel directory
from .window import Window
from .palette import Palette
from .controller import Controller
from .soundfx import SoundFX
from .music import Music
from .opengl import OpenGL


class Kernel:
    def __init__(self):
        pg.mixer.init()
        self.version    = 0
        self.running    = False
        self.framerate  = 60

        self.frames     = 0
        self.size       = pg.Vector2(0) 
        
        self.screen     = pg.Surface(self.size)
        self.window     = Window(self)
        self.palette    = Palette(self)
        self.controller = Controller(self)
        self.soundfx    = SoundFX(self)
        self.music      = Music(self)
        self.opengl     = OpenGL(self)
        
        self.clock      = pg.Clock()

        self.bg_color   = pg.Color(0, 0, 0, 0)
        
        self.active_surface:pg.Surface
        self.mixerscale = 10
    
    def setup(self):
        self.window.create()
        self.opengl.create()
        self.running = True

        self.active_surface = self.get_default_active_surface()

    def get_default_active_surface(self) -> pg.Surface:
        return self.screen
    
    def refresh(self):
        self.frames += 1
        self.opengl.refresh()
        self.window.refresh()
        if self.bg_color != -1: self.screen.fill(self.bg_color)
        self.palette.refresh()
        self.controller.refresh()
        self.music.refresh()
        self.soundfx.refresh()

        self.clock.tick(self.framerate)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            elif event.type == pg.WINDOWFOCUSGAINED:
                self.window.focus = True
                self.window.focus_just_gain = True
                
            elif event.type == pg.WINDOWFOCUSLOST:
                self.window.focus = False
                self.window.focus_just_lost = True
    
    def destroy(self):
        print("[Kernel] Run end process")
        pg.quit()
                
