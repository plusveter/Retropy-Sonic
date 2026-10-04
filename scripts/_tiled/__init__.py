from retropy import *

from .map import TiledMap
from .macro import *

tiledmap = TiledMap()


# FR: Rajoute un nouveau channel 
kernel.soundfx.new_channel(DEFAULT_SOUNDFX_CHANNEL)

#------------------------------------------------------------------------------------
#   Author: PlusVeter
#------------------------------------------------------------------------------------


class TiledObjectEntity(ObjectEntity ):
    
    tiled_id                :int
    tiled_name              :str
    tiled_layerid           :int

    tiled_z                 :int
    tiled_size              :vec2
    tiled_offset            :vec2
    
    tiled_gid               :int
    tiled_template          :str

    tiled_opacity           :int
    tiled_visible           :bool
    

    tiled_properties        :dict

    def __init__(self, objectid:int=-1):
        super().__init__()

        # setup variables
        self.tiled_id               = -1
        self.tiled_layerid          = -1
        self.tiled_name             = "unknowed"

        self.tiled_z                = 0
        self.tiled_size             = vec2(1)
        self.tiled_offset           = vec2(0)

        self.tiled_gid              = -1
        self.tiled_template         = ""

        self.tiled_opacity          = 1
        self.tiled_visible          = True

        self.tiled_properties       = {}
        self.revoke_offscreenlimit  = False

        if objectid < 0: 
            self.tiled_id = tiledmap.data.nextobjectid
            tiledmap.data.nextobjectid += 1
            self.tiled_z = self.tiled_id
        else:
            self.load(tiledmap.objects[objectid])

        self.spawn()

    @property
    def tiled_rotation(self):                 return self.angle

    @tiled_rotation.setter
    def tiled_rotation(self, new_rotation:int):   self.angle = new_rotation 

    @property
    def tiled_width(self):                    return self.tiled_size.x

    @tiled_width.setter
    def tiled_width(self, new_width):         self.tiled_size.x = new_width

    @property
    def tiled_height(self):                   return self.tiled_size.y

    @tiled_height.setter
    def tiled_height(self, new_height):       self.tiled_size.y = new_height

    @property
    def bound(self) -> pygame.Rect: 
        return pygame.Rect(
                    self.x + self.tiled_offset.x, 
                    self.y + self.tiled_offset.y, 
                    self.tiled_width, 
                    self.tiled_width
            )
    
    # [Function]
    def load(self, data:dict=None) -> int:
        if data is None: 
            if not tiledmap.objects.get(self.tiled_id): return 1
            data = tiledmap.objects[self.tiled_id]

        self.position           = vec2(data["x"], data["y"])
        
        self.tiled_name         = data["name"]
        self.tiled_layerid      = data["layerid"]
        self.tiled_z            = data["z"]
        self.tiled_size         = vec2(data["width"], data["height"])
        self.tiled_id           = data["id"] 
        self.tiled_gid          = data["gid"]
        self.tiled_rotation     = data["rotation"]

        self.tiled_properties = data.get("properties", {})

        # Check & correct data
        self.tiled_rotation = (-self.tiled_rotation)%360 
        self.tiled_offset = vec2(0, (-self.tiled_height * (self.tiled_gid > 0)))

        return 0

    def dump(self):
        return dict(
            position   = self.position  ,

            name       = self.tiled_name      ,
            layerid    = self.tiled_layerid   ,
            z          = self.tiled_z         ,

            size       = self.tiled_size      ,
            id         = self.tiled_id        ,
            gid        = self.tiled_gid       ,
            rotation   = self.tiled_rotation  ,
            properties = self.tiled_properties
        )

    def spawn(self):    tiledmap.pool.spawn(self)

    def kill(self):     tiledmap.pool.kill(self)
    
    def save(self):     tiledmap.refresh_object(self.tiled_id)

    def delete(self):   tiledmap.remove_object(self.tiled_id)

    def update(self):
        # check it the object is beyond the offscreen limit
        if (not self.revoke_offscreenlimit):
            offsetview:vec2 = tiledmap.offeset_views[self.tiled_layerid]
            position = self.position - offsetview + self.tiled_offset

            boundrect =  pygame.Rect(position.x , position.y , self.tiled_width, self.tiled_height)
            if not tiledmap.offscreen_rect.colliderect(boundrect): self.kill()
        
        self.revoke_offscreenlimit = False

        # music channel
        kernel.soundfx.select_channel(DEFAULT_SOUNDFX_CHANNEL)
        

    def get_special_flags(self, mode:int = -1):
        if mode < 0: mode = tiledmap.layers[self.tiled_layerid].mode
        return mode

    def draw(self, position:vec2=vec2(0)):
        draworder = self.tiled_z if not tiledmap.layers[self.tiled_layerid].draworder == "topdown" else self.y

        if not tiledmap.pool.prerenders_layers.get(self.tiled_layerid): 
            tiledmap.pool.prerenders_layers[self.tiled_layerid] = {}

        if not tiledmap.pool.prerenders_layers[self.tiled_layerid].get(draworder): 
            tiledmap.pool.prerenders_layers[self.tiled_layerid][draworder] = []

        tiledmap.pool.prerenders_layers[self.tiled_layerid][draworder].append(graphic.get_prerenderpacket(self.position + vec2(position)))


# [Graphic]
def adjust_pivot_to_pygame_y():
    """[Retropy | Graphic | Tiled]"""
    graphic.pivot.y -= graphic.image.height

def render_gid(gid, blendmode = 0):
    """[Retropy | Graphic | Tiled]"""
    if gid >= 0:
        graphic.image = convert_surfarray_to_surface(tiledmap.tiles[(gid)], blendmode)
        graphic.pivot = vec2(0)
        graphic.rotation_id    = 1

        return True
    return False

def prerender_gid(gid, blendmode = 0):
    """[Retropy | Graphic | Tiled]"""
    if gid >= 0:
        graphic.surfarray = tiledmap.tiles[(gid)]
        graphic.special_flags = blendmode
        graphic.pivot = vec2(0)
        graphic.rotation_id    = 1

        return True
    return False

# [Functions]
T = typing.TypeVar("T") # [Objects]

def check_object(class_: type[T]) -> list[T]:
    return tiledmap.pool.objects_type.get(class_.__name__, [])

def check_object_by_classname(classname) ->list[TiledObjectEntity]:
    return tiledmap.pool.objects_type.get(classname, [])

def check_layer_by_name(name:str):
    for layer in tiledmap.layers.values():
        if layer.name == name:
            return layer
    return -1
