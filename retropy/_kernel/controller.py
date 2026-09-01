import pygame as pg

class Controller:
    def __init__(self, kernel):
        self.kernel = kernel

        # keyboard
        self.pressed    = {}
        self.clicked    = {}
        self.buttons    = {}
        self.cooldown   = 0

        # gamepad
    
    def refresh(self):
        self.pressed    = pg.key.get_pressed()
        self.clicked    = pg.key.get_just_pressed()
        self.cooldown   = max(self.cooldown-1, 0)
    
    def add_button(self, pygame_key:int, index:int):
        self.buttons[index] = pygame_key