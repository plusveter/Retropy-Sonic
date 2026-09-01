from retropy import *


# | Variables |
OPENGL_WINDOW_BUFFERARRAY = numpy.array([
    # position (x, y), uv coords (x, y)
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,   # topright
    -1.0, -1.0, 0.0, 1.0, # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
], dtype='f4')

# [KEYS]

K_LEFT      = 0
K_RIGHT     = 1
K_UP        = 2
K_DOWN      = 3
K_A         = 4
K_B         = 5
K_ESCAPE    = -1
K_S         = -2

# [PALETTES]
P_PLAYERS       = 0
P_OBJECTS       = 1
P_TILES         = 2
P_BACKGROUND    = 3


# [PATH]
DIRECTORY_SAVEFILE      = "retropy"

MUSICFOLDER             = "Data/Musics/"
SOUNDSFOLDER            = "Data/SoundFX/"
SPRITESFOLDER           = "Data/Sprites/"
MAPSFOLDER              = "Data/Maps/"
FONTSFOLDER             = "Data/Fonts/"
SCRIPTESFOLDER          = "Data/Scriptes/"
PALETTESFOLDER          = "Data/Palettes/"

SHADERFOLDER            = SCRIPTESFOLDER+"Shaders/"

# [FONT]
HEXADECIMAL_TABLE = [
    '0', '1', '2', '3', '4', '5', '6', '7', 
    '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', ' '
]

ASCII_TABLE = [
    '\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07',
    '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f',
    '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17',
    '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f',
    ' ', '!', '"', '#', '$', '%', '&', "'",
    '(', ')', '*', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', ':', ';', '<', '=', '>', '?',
    '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
    'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
    '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'x', 'y', 'z', '{', '|', '}', '~', '\x7f'
]

# [CAMERA]
CAM_NULL            = -1
CAM_NORMAL          = 0
CAM_RETURN          = 1
CAM_RETURN_KNUCKLES = 2
CAM_NULL = -1
CAM_NORMAL = 0
CAM_RETURN = 1
CAM_RETURN_KNUCKLES = 2


CAMERA_LERP_NORMAL = 0
CAMERA_LERP_SIN1024 = 1
CAMERA_LERP_SIN1024_2 = 2
CAMERA_LERP_SIN512 = 3

CAMERA_BOUND_TOP = 0
CAMERA_BOUND_BOTTOM = 1
CAMERA_BOUND_LEFT = 2
CAMERA_BOUND_RIGHT = 3