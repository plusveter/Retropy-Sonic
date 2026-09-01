from dataclasses import dataclass
from pygame import (Vector2 as vec2)
from numpy import ndarray

@dataclass
class LayerData:
    offset_position : vec2
    offset_speed    : vec2

    surf_2Darray    : ndarray
    speed_1Darray   : ndarray
    cumul_1Darray   : ndarray
    orientation     : str
    special_flag    : int

    def __init__(self, data):
        self.offset_position    = vec2(data["offset_position"])
        self.offset_speed       = vec2(data["offset_speed"])

        self.surf_2Darray       = data["surf_2Darray"]
        self.speed_1Darray      = data["speed_1Darray"]
        self.cumul_1Darray      = data["cumul_1Darray"]
        self.orientation        = str(data["orientation"])
        self.special_flag       = int(data["special_flag"])
        


@dataclass
class BackgroundData:
    id              : str

    offset_position : vec2
    offset_speed    : vec2

    scroll_position : vec2
    scroll_speed    : vec2

    layers          : list[LayerData]
    pathimages      : list[str]
    colorpalette    : ndarray

    def __init__(self, data):
        self.id                 = str(data["id"])

        self.offset_position    = vec2(data["offset_position"])
        self.offset_speed       = vec2(data["offset_speed"])

        self.scroll_position    = vec2(data["scroll_position"])
        self.scroll_speed       = vec2(data["scroll_speed"])

        self.layers             = [LayerData(layer_data) for layer_data in data["layers"]]
        self.pathimages         = [str(imagepath) for imagepath in data["images_path"]]
        
        self.colorpalette       = data["colorpalette"]


