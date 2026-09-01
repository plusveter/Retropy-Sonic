from retropy import *

from scripts import _wrapper  as wrapper
from scripts.macro import *
from ._dataclass import BackgroundData
from .simple import bg_simple

class Background:
    def __init__(self):
        self.dictionnary:dict[str, BackgroundData]  = {}
        self.current:BackgroundData                 = None
        self.camera_position:vec2                   = vec2(0)
        self.camera_size:vec2                       = vec2(100)
        self.namelist                               = []

    def use(self, bg_id:int):
        if not self.dictionnary.get(bg_id): return -1
        self.current = self.dictionnary[bg_id]

    def unloads(self):
        self.dictionnary = []

    def load(self, path, bg_id:int):
        if not datapack.check_filepath(path): return
        data                                    = datapack.load_jsonfile(path)
        data["pathfile"]                        = path

        if data["type"] == "simple": new_data   = bg_simple(data)

        new_data["id"]                          = bg_id
        self.dictionnary[bg_id]                 = BackgroundData(new_data)
        self.namelist.append(bg_id)

    def render(self):
        
        if self.current is None: return -1
        frame = kernel.frames

        offset = vec2(
            self.camera_position.x * -self.current.offset_speed.x, 
            self.camera_position.y * -self.current.offset_speed.y
            ) + self.current.offset_position

        scroll = vec2(
            self.camera_position.x * -self.current.scroll_speed.x, 
            self.camera_position.y * -self.current.scroll_speed.y
            ) + self.current.scroll_position

        for layer in self.current.layers:
            prerender(layer.surf_2Darray, vec2(
                self.camera_position.x * -layer.offset_speed.x, 
                self.camera_position.y * -layer.offset_speed.y
                ) + layer.offset_position + offset,
                layer.special_flag
                
            )
            if layer.orientation == "v":
                graphic.surfarray = wrapper.surfarray.perfect_vertical_scroll(
                        graphic.surfarray, 
                        ((layer.speed_1Darray*scroll.x) + (layer.cumul_1Darray*frame)), 
                        0
                    )
            elif layer.orientation == "h":
                graphic.surfarray = wrapper.surfarray.perfect_horizontal_scroll(
                        graphic.surfarray, 
                        ((layer.speed_1Darray*scroll.y) + (layer.cumul_1Darray*frame)), 
                        0
                    )
            
                
            constrain_prerender()
            draw_prerender()

        

