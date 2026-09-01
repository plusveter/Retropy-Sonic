from ._tiled import *
from .camera import Camera
from . import _wrapper as wrapper
# from .background_old import Background
from ._background import Background
from .macro import *


class General:
    dynamic_sprites:SpritesAnimations = None
    debug_mouse = False
    

    def __init__(self):
        self.musics = {}
        self.zone = ""

        self.rings = 0
        self.lives = 3
        self.extra_live_point = 0

        # SoundFX
        self.SFX_Spring = load_soundfx(SOUNDSFOLDER +"Global/Spring.wav")
        self.SFX_Ring = load_soundfx(SOUNDSFOLDER +"Global/Ring.wav")

        # Animations
        self.hud_sprites = load_RSDKv5Animations(SPRITESFOLDER+"Global/HUD.bin")
        self.water_sprites = load_RSDKv5Animations(SPRITESFOLDER+"Global/Water.bin")
        self.ring_tracker = AnimationTracker()
        self.waterwave_tracker = AnimationTracker()

        # Fonts
        self.dev_font = load_datafont_from_animation(load_RSDKv5Animations("Data\Sprites\Dev\Font.bin"), "Font", ASCII_TABLE)
        self.hud_numbers_font = load_datafont_from_animation(self.hud_sprites, "Numbers", HEXADECIMAL_TABLE)

        # Palettes
        self.mask_array = numpy.ones((int(2), int(2)), dtype=numpy.bool)
        self.backgrounds_pal:dict[numpy.ndarray] = {}

        # Water
        self.water_height = 0
        self.water_visible = False
        

    def reload_map(self):
        self.load_map(self.zone)

    def load_map(self, zone):
        self.zone = zone

        # Palettes
        self.mask_array = numpy.ones((int(kernel.size.x), int(kernel.size.y)), dtype=numpy.uint8)

        if datapack.check_filepath(MAPSFOLDER + zone +"/map.tmj"):
            tiledmap.load(MAPSFOLDER + zone +"/map.tmj")
        else:
            raise FileNotFoundError(
                f"""Your file [{MAPSFOLDER + zone +"/map.tmj"}] doesn't exist """
            )


        
        if datapack.check_filepath(PALETTESFOLDER + zone +"/palette.pal") and False: # Obsolete
            set_palette(load_from_palfile(PALETTESFOLDER + zone +"/palette.pal"))

        if datapack.check_filepath(SPRITESFOLDER + zone +"/Dynamic.bin"):
            general.dynamic_sprites = load_RSDKv5Animations(SPRITESFOLDER + zone +"/Dynamic.bin")
            general.dynamic_sprites.base_on_by_names(load_RSDKv5Animations(SPRITESFOLDER+ "/Global/Dynamic.bin"))
        else:
            general.dynamic_sprites = load_RSDKv5Animations(SPRITESFOLDER+ "/Global/Dynamic.bin")
                        

        # load palette
        players_palfile = PALETTESFOLDER + F"{zone}/players.pal"
        if datapack.check_filepath(players_palfile): set_palette(load_from_palfile(players_palfile), P_PLAYERS)

        objects_palfile = PALETTESFOLDER + F"{zone}/objects.pal"
        if datapack.check_filepath(objects_palfile): set_palette(load_from_palfile(objects_palfile), P_OBJECTS)

        tile_palfile = PALETTESFOLDER + F"{zone}/tiles.pal"
        if datapack.check_filepath(tile_palfile): set_palette(load_from_palfile(tile_palfile), P_TILES)

        # background
        background.camera_size = kernel.size.copy()
        for foldername in tiledmap.data.properties.get("backgrounds", []):
            
            background_palfile = PALETTESFOLDER + F"{zone}/backgrounds/{foldername}.pal"
            if datapack.check_filepath(background_palfile): self.backgrounds_pal[foldername] = load_from_palfile(background_palfile)
    
            background.load(resolve_relative_path(tiledmap.path, f"./{foldername}/data.json"), foldername)

        # verify if player object does exist
        players = tiledmap.get_objects_by_type("Player")
        if len(players) != 0: # set camera_position
            objectdata = tiledmap.objects[players[0]]
            camera.center_x = objectdata["x"]
            camera.center_y = objectdata["y"]

    def update(self):
        # rings
        general.ring_tracker.handle_animation_by_name(general.dynamic_sprites, "Normal Ring")
        if general.rings < 0: general.rings = 0

        # Live
        if self.rings >= self.extra_live_point:
            self.lives += 1
            self.extra_live_point += 100
        

# Universal class
camera = Camera()
general = General()
background = Background()


# [Functions]
def apply_flip_on_prerender(flipX:int|bool=0, flipY:int|bool=0):
    if flipX or flipY:
        graphic.surfarray = wrapper.surfarray.flip(graphic.surfarray.copy(), flip_x=flipX, flip_y=flipY)
        
        if flipX: graphic.pivot.x = -(graphic.pivot.x + graphic.surfarray.shape[0])
        if flipY: graphic.pivot.y = -(graphic.pivot.y + graphic.surfarray.shape[1])


def apply_rotation_on_prerender(angle):
        angle %= 360

        # No rotation allowed
        if graphic.rotation_id == 0 or angle == 0: return 

        # Snap rotation
        if graphic.rotation_id == 2:
            angle = ((angle + 22.5) // 45) * 45
        elif graphic.rotation_id == 3:
            angle = ((angle + 45) // 90) * 90
        elif graphic.rotation_id == 4:
            angle = ((angle + 90) // 180) * 180

        # Rotate surface
        rotated_2Darray = wrapper.surfarray.rotate(graphic.surfarray.copy(), angle)

        # Original and new centers
        old_center = vec2(graphic.surfarray.shape) / 2
        new_center = vec2(rotated_2Darray.shape) / 2

        # Rotate pivot around center
        direction = old_center + graphic.pivot
        direction = direction.rotate(-angle)

        graphic.pivot = -new_center + direction
        graphic.surfarray = rotated_2Darray

def apply_color_offset_on_prerender():
    graphic.surfarray = wrapper.surfarray.apply_color_offset(
        graphic.surfarray.copy(), 
        (graphic.offset + graphic.pivot),
        general.mask_array, 
        vec2(0)
    )

def apply_scale_on_prerender(new_width:int, new_height:int):
        old_size = vec2(graphic.surfarray.shape)   # (h, w)
        new_size = vec2(new_width, new_height)                # (w, h)

        # Match original axis behavior exactly
        scale = vec2(
            old_size.y/new_size.y,  # x uses height
            old_size.x/new_size.x   # y uses width
        )

        graphic.pivot.x *= scale.x
        graphic.pivot.y *= scale.y

        graphic.surfarray = wrapper.surfarray.scale(graphic.surfarray.copy(), new_size.x, new_size.y)

def apply_scale_by_on_prerender(scale):
    new_size = vec2(graphic.surfarray.shape)*scale
    graphic.pivot *= scale
    graphic.surfarray = wrapper.surfarray.scale(graphic.surfarray.copy(), new_size.x, new_size.y)


