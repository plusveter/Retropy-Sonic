import numpy, pygame, json, os, math, typing
import xml.etree.ElementTree as xmlET

# import retropy modules
from ._kernel.macro import *
from ._kernel import Kernel
from ._graphic import Graphic
from ._datapack import *
from ._collisions import *
from ._spritesanimations import *
from ._entity import *


# [Variables]
kernel = Kernel()
graphic = Graphic()

vec2 = pygame.Vector2
vec3 = pygame.Vector3
rect = pygame.Rect

def get_view_size() -> vec2: return kernel.size 

# [other]
def is_float(s: str) -> bool:
    """ [Retropy | other] """
    try: float(s) ; return True
    except ValueError: return False

# [Path/File]
def resolve_relative_path(old_path: str, new_path: str) -> str:
    """ [Retropy | Path/File] """
    return os.path.normpath(os.path.join(os.path.dirname(old_path), new_path))

def is_directory(path: str) -> bool:
    """ [Retropy | Path/File] """
    return os.path.isdir(path)

def has_file(path: str) -> bool:
    """ [Retropy | Path/File] """
    return os.path.isfile(path)

def get_extension(file_path: str) -> str:
    """ [Retropy | Path/File] """
    return os.path.splitext(file_path)[1][1:]


# [Palettes]
def set_palette(palette:numpy.ndarray, pal_id:int = 0):
    """ [Retropy | Palettes] """
    kernel.palette.define_array(pal_id, palette)

def set_palette_at(index:int, color:list[int], pal_id:int = 0):
    kernel.palette.define_array_at(pal_id, index, color)

def define_palette_from_image(imagepath:str, pal_id:int = 0):
    """ [Retropy | Palettes] """
    kernel.palette.define_array(pal_id, pygame.image.load(imagepath).get_palette())

def load_palette_from_image(imagepath:str):
    """ [Retropy | Palettes] """
    return numpy.array(pygame.image.load(imagepath).get_palette())

def save_into_palfile(path:str, palette:numpy.ndarray):
    bytedata = b""

    for data in ["JASC-PAL", "0100", "256"]:   
        bytedata += f"{data}\x0d\x0a".encode('utf-8')
        
    for color in palette:
        bytedata += f"{color[0]} {color[1]} {color[2]}\x0d\x0a".encode('utf-8')

    #FR: ce n'est pas définitive je doit encore faire des tests
    with open(path, mode='wb+') as file:
        file.write(bytedata) # b is important -> binary
        file.close()

def load_from_palfile(path_palette) -> numpy.ndarray:
    def CONVERT_ASCII(line):
        ASCII_CODE = {48:0, 49:1, 50:2, 51:3, 52:4, 53:5, 54:6,55:7, 56:8, 57:9}
        number = 0
        while not int(fileContent[line]) in [32, 13]:
            number = (number*10) + ASCII_CODE[int(fileContent[line])]
            line += 1
        return number, line

    PAL_DATA = []

    fileContent = datapack.load_datafile(path_palette)
    line = 21

    for i in range(256):
        r, line = CONVERT_ASCII(line); line += 1
        g, line = CONVERT_ASCII(line); line += 1
        b, line = CONVERT_ASCII(line); line += 1
        line += 1
        PAL_DATA.append([r, g, b])
            
    return numpy.array(PAL_DATA, dtype=numpy.uint8)

# [Keyboard]
def get_pressed(index_key):
    """ [Retropy | Keyboard] """
    return kernel.controller.pressed[
        kernel.controller.buttons[index_key]
    ]

def get_clicked(index_key):
    """ [Retropy | Keyboard] """
    return kernel.controller.clicked[
        kernel.controller.buttons[index_key]
    ]


# [Surfarray]
def load_surfarray_image(imagepath:str):
    """ [Retropy | Surfarray] """
    return pygame.surfarray.array2d(pygame.image.load(imagepath).get_palette())

def convert_surfarray_to_surface(np_2Darray:numpy.ndarray, special_flags = 0, pal_id:int =0):
    """ [Retropy | Surfarray] """
    color = [255, 0, 255]
    if      special_flags == 0                          : ...
    elif    special_flags == pygame.BLEND_ADD           : color = ([0]*3) 
    elif    special_flags == pygame.BLEND_MULT          : color = ([255]*3)
    elif    special_flags == pygame.BLEND_SUB           : color = ([0]*3)
    kernel.palette.get_surface(pal_id=pal_id).set_palette_at(0, color)

    surf = pygame.transform.scale(kernel.palette.get_surface(pal_id), np_2Darray.shape)
    pygame.surfarray.blit_array(surf, np_2Darray)
    return surf

def subsurfarray_rect(surf_array:numpy.ndarray, rect:list[int]) -> numpy.ndarray:
    """ Extract a rectangular sub-surface from a pixel array. """
    return surf_array[rect[0]:rect[0]+rect[2], rect[1]:rect[1]+rect[3]]

# [Active Surface]
def get_default_active_surface():
    """ [Retropy | Active Surface] """
    return kernel.get_default_active_surface()

def set_active_surface(surface):
    """ [Retropy | Active Surface] """
    kernel.active_surface = surface

def reset_active_surface():
    """ [Retropy | Active Surface] """
    kernel.active_surface = get_default_active_surface()

def get_active_surface():
    """ [Retropy | Active Surface] """
    return kernel.active_surface

def blit(source: pygame.Surface, position: vec2, special_flags: int = 0):
    """ [Retropy | Active Surface] """
    try:
        kernel.active_surface.blit(source=source, dest=position, special_flags=max(special_flags, 0))
    except pygame.error:
        raise pygame.error(
            f"source ={source}\n"+
            f"position ={position}\n"+
            f"special_flags ={special_flags}"
            )

def surfarray_blit(np_2Darray:numpy.ndarray, position: vec2, special_flags: int = 0, pal_id:int =0):
    """ [Retropy | Active Surface | Surfarray] """
    blit(convert_surfarray_to_surface(np_2Darray, special_flags=special_flags, pal_id=pal_id), position=vec2(position), special_flags=special_flags)


# [Graphic]
def render(source: pygame.Surface, pivot: vec2 = vec2(0), special_flags: int = 0, offset = vec2(0)):
    """ [Retropy | Graphic] """

    graphic.image = source
    graphic.pivot = vec2(pivot)
    graphic.offset = vec2(offset)
    graphic.special_flags = special_flags

def render_surfarray(source: numpy.ndarray, pivot: vec2 = vec2(0), special_flags: int = 0, offset = vec2(0), palette_id:int = 0):
    """ [Retropy | Graphic | Surfarray] """
    graphic.image = convert_surfarray_to_surface(source, special_flags=special_flags, pal_id=palette_id)
    graphic.pivot = vec2(pivot)
    graphic.offset = vec2(offset)
    graphic.special_flags = special_flags

def prerender(source: numpy.ndarray, pivot: vec2 = vec2(0), special_flags: int = 0, offset = vec2(0), palette_id:int = -1):
    """ [Retropy | Graphic | Surfarray] """
    graphic.surfarray = source
    graphic.pivot = vec2(pivot)
    graphic.offset = vec2(offset)
    graphic.special_flags = special_flags
    if palette_id >= 0: graphic.palette = int(palette_id)

def constrain_prerender():
    """ [Retropy | Graphic | Surfarray] """
    x, y    = graphic.pivot
    sw, sh  = get_active_surface().size

    w, h = graphic.surfarray.shape[:2]

    # Visible region
    left   = int(max(0, -x))
    top    = int(max(0, -y))
    right  = int(min(w, sw - x))
    bottom = int(min(h, sh - y))

    if left >= right or top >= bottom:
        graphic.surfarray   = graphic.surfarray[:0, :0]
        graphic.pivot       = vec2(0, 0)
        return -1

    graphic.surfarray   = graphic.surfarray[left:right, top:bottom]
    graphic.pivot       = vec2( max(x, 0), max(y, 0) )
    

def prerender_rect(rect:pygame.Rect|list, color_id:int, special_flags: int = 0):
    """ [Retropy | Graphic | Surfarray] """
    array2d = numpy.ones((rect[2] * rect[3]), dtype=numpy.uint8).reshape((rect[2], rect[3]))
    array2d[:] = color_id
    prerender(array2d, vec2(rect[0], rect[1]), special_flags=special_flags)

def render_rect(rect:pygame.Rect|list, color:pygame.Color|str|list, special_flags: int = 0):
    """ [Retropy | Graphic | Surfarray] """
    surface = pygame.Surface((rect[2], rect[3]))
    surface.fill(color)
    render(surface, vec2(rect[0], rect[1]), special_flags=special_flags)

def render_prerender():
    """ [Retropy | Graphic | Surfarray] """
    render_surfarray(graphic.surfarray, pivot=graphic.pivot, special_flags=graphic.special_flags, offset=graphic.offset, palette_id=graphic.palette)

def apply_scale(new_width:int, new_height:int):
    """ [Retropy | Graphic] """
    graphic.apply_scale(new_width, new_height)

def apply_scale_by(scale):
    """ [Retropy | Graphic] """
    graphic.apply_scale_by(scale)

def apply_rotation(angle):
    """ [Retropy | Graphic] """
    graphic.apply_rotation(angle)

def apply_flip(flipX:int|bool=0, flipY:int|bool=0):
    """ [Retropy | Graphic] """
    graphic.apply_flip(flipX, flipY)

def draw(position:vec2 = vec2(0)):
    """ [Retropy | Graphic] """
    blit(graphic.image, (vec2(position) + graphic.pivot + graphic.offset), graphic.special_flags)

def draw_prerender(position:vec2 = vec2(0)):
    """ [Retropy | Graphic] """
    render_prerender()
    draw(position)

def draw_renderpacket(renderpacket, position):
    """ [Retropy | Graphic] """
    blit(renderpacket[0], renderpacket[1]+position, renderpacket[2])


# [SpriteAnimation]
def load_RSDKv5Animations(path:str) -> SpritesAnimations:
    """ [Retropy | SpriteAnimation] """
    return SpritesAnimations(load_RSDKv5Animations_Data(path))

def render_name_sprite(data:SpritesAnimations, name:str, tracker:AnimationTracker, special_flags:int=0):
    """ [Retropy | SpriteAnimation | Graphic] """
    # get animation
    animation = data.animation_names[name]

    # extract those data
    graphic.rotation_id = animation.rotation
    graphic.special_flags = special_flags
    renderpacket = animation.frames[tracker.frame]

    # render
    render_surfarray(renderpacket.array, renderpacket.pivot, special_flags)

def render_id_sprite(data:SpritesAnimations, id:int, tracker:AnimationTracker, special_flags:int=0):
    """ [Retropy | SpriteAnimation | Graphic] """
    # get animation
    animation = data.animation_ids[id]

    # extract those data
    graphic.rotation_id = animation.rotation
    graphic.special_flags = special_flags
    renderpacket = animation.frames[tracker.frame]

    # render
    render_surfarray(renderpacket.array, renderpacket.pivot, special_flags)

def render_frame(frame, special_flags:int=0, rotation_id=1):
    graphic.rotation_id = rotation_id
    graphic.special_flags = special_flags
    render_surfarray(frame.array, frame.pivot, special_flags=special_flags)

def prerender_name_sprite(data:SpritesAnimations, name:str, tracker:AnimationTracker, special_flags:int=0, palette_id:int = -1):
    """ [Retropy | SpriteAnimation | Graphic] """
    if palette_id == -1: palette_id = graphic.palette
    # get animation
    animation = data.animation_names[name]

    # extract those data
    graphic.rotation_id = animation.rotation
    graphic.special_flags = special_flags
    renderpacket = animation.frames[tracker.frame]

    # render
    prerender(renderpacket.array, renderpacket.pivot, special_flags, palette_id=palette_id)

def prerender_id_sprite(data:SpritesAnimations, id:int, tracker:AnimationTracker, special_flags:int=0, palette_id:int = -1):
    """ [Retropy | SpriteAnimation | Graphic] """
    if palette_id == -1: palette_id = graphic.palette
    
    # get animation
    animation = data.animation_ids[id]

    # extract those data
    graphic.rotation_id = animation.rotation
    graphic.special_flags = special_flags
    renderpacket = animation.frames[tracker.frame]

    # render
    prerender(renderpacket.array, renderpacket.pivot, special_flags, palette_id=palette_id)

def prerender_frame(frame, special_flags:int=0, rotation_id=1, palette_id:int = -1):
    """ [Retropy | SpriteAnimation | Graphic] """
    if palette_id == -1: palette_id = graphic.palette
    graphic.rotation_id = rotation_id
    graphic.special_flags = special_flags
    prerender(frame.array, frame.pivot, special_flags=special_flags, palette_id=palette_id)

def prerender_rect(rect: pygame.Rect, colorid:int, specials_flag:int = 0, palette_id:int = -1):
    array = numpy.zeros((rect.width*rect.height), dtype=numpy.uint8).reshape((rect.width, rect.height))
    array[:] = colorid
    prerender(array, vec2(rect.topleft), specials_flag, palette_id=palette_id)


# [Fonts]
def load_datafont_from_animation(data:SpritesAnimations, name:str, charlist:list) -> dict[str, FrameData]:
    new_datafont = {} # I'm using a dictionnary for this one
    animation = data.animation_names[name]
    for frame, char in enumerate(charlist): new_datafont[str(char)] = animation.frames[frame]
    return new_datafont

def get_sprite_text(text:str, datafont:dict[str, FrameData], spacex=0, spacey=0):
    chars = []
    position = vec2(0)
    size_y = 0
    for char in text:
        if char == '\n':
            position.y += size_y+spacey
            position.x = 0
        else:
            char_frame = datafont.get(char, -1)
            if not isinstance(char_frame, int):
                # add this into the list
                chars.append((char_frame, vec2(position)))
                
                # update position and Y lenght
                width, height = char_frame.array.shape
                size_y = max(height, size_y)
                
                position.x += width+spacex
    return chars

def draw_text(text, position:vec2):
    for charframe, position_text in text:
        render_frame(charframe)
        draw(position_text+position)

# [SoundFX]
def load_soundfx(pathfile) -> pygame.Sound:
    return datapack.load_soundfile(pathfile)

def new_sound_channel(name:str): kernel.soundfx.new_channel(name)

def select_sound_channel(name:str): kernel.soundfx.select_channel(name)

def get_sound_channel(): kernel.soundfx.get_channel()

def play_sound(sound:pygame.Sound, loop:bool=False, channel_name:str=None):
    kernel.soundfx.play(sound, loop, channel_name)



# [Music]
# FR: C'est encore très rudimentaire, j'avais l'intension de créer un classtype spécial pour les musics
def add_music(pathfile:str, start_end:list[int], volume:int, author:str) -> int:
    return kernel.music.add(pathfile, start_end, volume, author)

def load_musics_from_jsonfile(pathfile:str) -> dict:
    data = datapack.load_jsonfile(pathfile)
    new_dictionnary = {}
    for music in data["list"]:
        new_dictionnary[music["name"]] = add_music(data["folderpath"]+music["filename"], music["start-end"], music["volume"], music["author"])
    return new_dictionnary

def play_music(musicid:int=-1, fade_out:int=0, fade_in=0, special_key:int=SELECTMUSIC_RESET, debug=False):
    kernel.music.select_by_id(musicid, fade_out, fade_in, special_key, debug)

def stop_music():
    """Temporaire"""
    kernel.music.stop()

def pause_music():
    kernel.music.pause()

def unpause_music():
    kernel.music.unpause()

        

# [Maths]
def point_direction(x1, y1, x2, y2): return math.atan2(y2 - y1, x2 - x1)*(180/math.pi)

def clamp(x, low, high): return max(low, min(x, high)) 

def sign(value): return int(math.copysign(1, value))

def approach(value, target, step):
    if value < target:
        return min(value + step, target)
    elif value > target:
        return max(value - step, target)
    return target

def lerp(a, b, t): return a + (b - a) * t

def lerp_normal(percent, start, end):
    t = percent / 256.0
    return lerp(start, end, t)

def lerp_sin1024(percent, start, end):
    t = percent / 256.0
    eased = math.sin(t * math.pi * 0.5)  # ease-out
    return lerp(start, end, eased)

def lerp_sin1024_2(percent, start, end):
    t = percent / 256.0
    eased = 0.5 - 0.5 * math.cos(t * math.pi)  # ease in-out
    return lerp(start, end, eased)

def lerp_sin512(percent, start, end):
    t = percent / 256.0
    eased = math.sin(t * math.pi)
    return lerp(start, end, eased)
    
    
# [DevTools]
def make_palette_viewer(scale = 1):
    palette = numpy.zeros(((16*scale)**2)).reshape(((16*scale), (16*scale))) 
    value = 0
    for x in range(16):
        for y in range(16):
            palette[y*scale : ((y+1)*scale), x*scale : ((x+1)*scale)] = value
            value += 1
    return palette
