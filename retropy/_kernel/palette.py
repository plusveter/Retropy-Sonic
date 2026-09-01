# mainlib
import numpy as np
import pygame as pg

class Palette:
    def __init__(self, kernel):
        self.kernel     = kernel

        #FR: ancient system depuis 2023
        self.surface    = pg.Surface(pg.Vector2(2)).convert(8)
        self.array      = np.array(self.surface.get_palette(), dtype=np.uint8)

        self.surface.set_colorkey(0)


        #FR: Le nouveaux system que je vais définir
        self.list:dict[dict[str, np.ndarray | pg.Surface]] = {} # int(pal_id) => [array, surface(=8bit)]

    def reset(self):
        self.list = {} # kills every reference in 

    def new(self, pal_id:int) -> (int | bool):
        if self.list.get(int(pal_id)): return -1
        
        surface =  pg.Surface(pg.Vector2(1)).convert(8)
        surface.set_colorkey(0)

        self.list[int(pal_id)] = dict(
            array = np.array(self.surface.get_palette(), dtype=np.uint8), 
            surface =  surface
        )
        return 0

    def remove(self, pal_id:int):
        if not self.list.get(int(pal_id)): return -1
        self.list.pop(int(pal_id))

    def get_array(self, pal_id:int) -> np.ndarray:
        if not self.list.get(int(pal_id)): return -1
        return self.list[int(pal_id)]["array"]

    def get_surface(self, pal_id:int) -> pg.Surface:
        if not self.list.get(int(pal_id)): return -1
        return self.list[int(pal_id)]["surface"]

    def define_array(self, pal_id:int, palette:list) -> np.ndarray:
        if not self.list.get(int(pal_id)): return -1
        self.list[int(pal_id)]["array"] = np.array(palette, dtype=np.uint8)

    def define_array_at(self, pal_id:int, index:int, color:list[int]) -> np.ndarray:
        if not self.list.get(int(pal_id)): return -1
        self.list[int(pal_id)]["array"][index] = color

    def refresh(self):
        self.surface.set_palette(self.array)

        #FR: Ce 
        for pal_id in self.list: self.get_surface(pal_id).set_palette(self.get_array(pal_id))
