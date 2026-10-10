from .import rsdkv5, default
import os, pygame


if os.path.isfile("Data.rsdk"):
    datapack = rsdkv5.RSDKv5("Data.rsdk")
else:
    datapack = default.Default()


def load_rsdkv5_datapack(path):
    """ [Retropy | DataPack | RSDKv5] """ 

     # loading rsdkv5 data if the file does exist
    global datapack
    if not os.path.exists(path): datapack = rsdkv5.RSDKv5(path)
    return (datapack.type != default.Default.type)


def load_RSDKv5Animations_Data(path:str) -> dict:
    """ [Retropy | DataPack | RSDKv5] """
    sprites_directory = os.path.dirname( os.path.dirname( path ) )
    data = datapack.load_datafile(path)
    reader = rsdkv5.Reader()


    image_list = []
    HitBox_numbers = 0
    Animation_numbers = 0

    reader.pos = 0
    signature = reader.read_string_selectbytes(data, 2)
    unknowed  = reader.read_selectbytes(data, 6)
    
    animation_package = dict(signature=signature, datas=[], imagespath=[])

    N_Texture = reader.read_Uint_1bytes(data)
    for n in range(N_Texture):
        lenght_Link = reader.read_Uint_1bytes(data)
        filepath = os.path.normpath(os.path.join(sprites_directory, reader.read_string_selectbytes(data, lenght_Link)[:lenght_Link - 1]))
        animation_package["imagespath"].append(filepath)
        image_list.append(datapack.load_8b_imagefile(filepath))

    HitBox_numbers = reader.read_Uint_1bytes(data)

    for n in range(HitBox_numbers): 
        lenght = reader.read_Uint_1bytes(data)
        reader.pos += lenght

    Animation_numbers = reader.read_Uint_2bytes(data)
    NumberID = 0
    for i in range(Animation_numbers):
        len_name = reader.read_Uint_1bytes(data)
        Name            = reader.read_string_selectbytes(data, len_name).replace("\x00", "")
        Frame_number    = reader.read_Uint_2bytes(data)
        Speed           = reader.read_Uint_2bytes(data)
        Loop            = reader.read_Uint_1bytes(data)
        RotationID      = reader.read_Uint_1bytes(data)
        

        animation_data = dict(id = NumberID, name = Name, rotation = RotationID, speed = Speed, loop = Loop, frames = [])
        
        for i in range(Frame_number):

            image:pygame.Surface = image_list[reader.read_Uint_1bytes(data)]
            COORD = [0, 0]
            SIZE = [0, 0]
            PIVOT = [0, 0]


            FrameDuration = reader.read_Uint_2bytes(data)
            FrameID = reader.read_Uint_2bytes(data) #ID

            COORD[0]    = reader.read_Uint_2bytes(data)
            COORD[1]    = reader.read_Uint_2bytes(data)
            SIZE[0]     = reader.read_Uint_2bytes(data)
            SIZE[1]     = reader.read_Uint_2bytes(data)
            

            PIVOT[0] = reader.read_int_2bytes(data)
            PIVOT[1] = reader.read_int_2bytes(data)


            reader.pos += 4*HitBox_numbers*2

            if SIZE[0] == 0 or SIZE[1] == 0:
                surface = image.subsurface(0, 0, 1, 1).convert(8)
                surface.fill(surface.get_palette_at(0))
            else:
                surface = image.subsurface(COORD[0], COORD[1], SIZE[0], SIZE[1]).convert(8)
            array2D = pygame.surfarray.array2d(surface)
            animation_data["frames"].append(dict(id=FrameID, array=array2D, size=SIZE, pivot=PIVOT, duration=FrameDuration))
        
        animation_package["datas"].append(animation_data)
        NumberID += 1

    return animation_package

