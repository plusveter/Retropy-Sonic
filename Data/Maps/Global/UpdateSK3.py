import pygame, sys, json, math

size = 16
file = "16x16.json"


OUT_SIDE = 0
def collidesensor(sensor1, sensor2):
    return sensor1[0].overlap(sensor2[0], [sensor2[1][0]-sensor1[1][0], sensor2[1][1]-sensor1[1][1]])

def rect_to_sensor(rect, center_point):
    """ INSIDE: MASK, RECT+CENTER_POINT, ORIGINAL_RECT"""
    mask = pygame.mask.from_surface(pygame.Surface((rect[2], rect[3])))
    return [mask, pygame.Rect(rect[0]+center_point[0], rect[1]+center_point[1], rect[2], rect[3]), rect]

def surface_to_sensor(surface, rect):
    mask = pygame.mask.from_surface(surface)
    return [mask, pygame.Rect(rect[0]-OUT_SIDE, rect[1]-OUT_SIDE, surface.get_size()[0], surface.get_size()[1]), pygame.Rect(rect[0], rect[1], surface.get_size()[0], surface.get_size()[1])]

with open(file) as json_file:
    JSON = json.load(json_file)
json_file.close()

def rotation_2point(focus, target):
    return math.atan2(target[1] - focus[1], target[0] - focus[0])*180/math.pi

pygame.init()
screen = pygame.display.set_mode([32,32], pygame.SCALED)


image = (pygame.image.load(JSON["image"])).convert()
FPS = pygame.time.Clock()

S = image.get_size()
S = [int(S[0]/size), int(S[1]/size)]
print(S)


Rot_ID = []
for y in range(S[1]):
    for x in range(S[0]):
        pygame.event.pump()
        tiles = image.subsurface((x*size, y*size, size, size))
        tiles.set_colorkey([0, 255, 0])
        
        


        Mask = surface_to_sensor(tiles, [0, 0])
        pygame.display.update()
        screen.fill([100, 100, 100])
        screen.blit(tiles, (0, 0))
        FPS.tick(10)

        Get_first = [0 ,0]
        Get_end = [0 ,0]
        

        F = False
        E = False

        FIST_TRY = False

        UP = 0
        for h in range(size):
            sensor2 = rect_to_sensor([h, 0, 1, 1], [0, 0])
            if collidesensor(sensor2, Mask):
                UP += 1

        DOWN = 0
        for h in range(size):
            sensor2 = rect_to_sensor([h, (size-1), 1, 1], [0, 0])
            if collidesensor(sensor2, Mask):
                DOWN += 1

        SET = False

        if UP >  DOWN:
            FIST_TRY = True
        else:
            if DOWN <= 2: SET = True


        CORRECTION = False

        for x_tile in range(size):
            for y_tile in range(size):
                X = x_tile

                if not FIST_TRY:

                    X = x_tile
                    Y = y_tile

                    sensor1 = rect_to_sensor([X, Y, 1, 1], [0, 0])
                    if x_tile == 0 and y_tile == 0:
                        if collidesensor(sensor1, Mask):
                            CORRECTION = True

                    if not CORRECTION:
                        if collidesensor(sensor1, Mask) and not F:
                            F = True
                            Get_first = [X, y_tile]
                    else:
                        if not collidesensor(sensor1, Mask):
                            CORRECTION = False

                else:
                    X = (size-1)-x_tile
                    Y = (size-1)-y_tile

                    sensor1 = rect_to_sensor([X, Y, 1, 1], [0, 0])
                    if x_tile == 0 and y_tile == 0:
                        if collidesensor(sensor1, Mask):
                            CORRECTION = True

                    if not CORRECTION:
                        if collidesensor(sensor1, Mask) and not F:
                            F = True
                            Get_first = [X, (size-1)-y_tile]
                    else:
                        if not collidesensor(sensor1, Mask):
                            CORRECTION = False

        CORRECTION = False

        for x_tile in range(size):
            for y_tile in range(size):
                
                

                if not FIST_TRY:
                    X = (size-1)-x_tile
                    Y = y_tile

                    sensor1 = rect_to_sensor([X, Y, 1, 1], [0, 0])
                    if x_tile == 0 and y_tile == 0:
                        if collidesensor(sensor1, Mask):
                            CORRECTION = True

                    if not CORRECTION:
                        if collidesensor(sensor1, Mask) and not E:
                            E = True
                            Get_end = [X, y_tile]
                    else:
                        if not collidesensor(sensor1, Mask):
                            CORRECTION = False

                else:
                    X = x_tile
                    Y = (size-1)-y_tile
                    sensor1 = rect_to_sensor([X, (size-1)-y_tile, 1, 1], [0, 0])
                    if x_tile == 0 and y_tile == 0:
                        if collidesensor(sensor1, Mask):
                            CORRECTION = True

                    if not CORRECTION:
                        if collidesensor(sensor1, Mask) and not E:
                            E = True
                            Get_end = [X, (size-1)-y_tile]
                    else:
                        if not collidesensor(sensor1, Mask):
                            CORRECTION = False

        pygame.draw.rect(screen, [255, 0, 0], [Get_first[0], Get_first[1], 1, 1])
        pygame.draw.rect(screen, [0, 255, 255], [Get_end[0], Get_end[1], 1, 1])

        if SET:
            Get_end[1] = Get_first[1]-1

        U = ROT = round(-rotation_2point(Get_first, Get_end))

        
        if SET:
            ROT = ROT-DOWN
        
        if ROT < 0:
            ROT = 360+ROT

        if ROT > 360:
            ROT = ROT-360 

        if ROT == 0 and not (size == DOWN):
            ROT = 1

        elif abs(ROT) <= 2:
            ROT = "X"

        print(ROT, U)

        Rot_ID.append(ROT)







    #Rot_ID[y] = ROT




tiles_ROT = []

for ID, rot in enumerate(Rot_ID):
    tiles_ROT.append({"id":ID, "class":str(rot)})

    #tiles_ROT[ID] = rot
JSON["tiles"] = tiles_ROT
with open(file, "w+") as json_file:
        json.dump(JSON, json_file)
json_file.close()

try:

    pass
except:
    print(str(tiles_ROT).replace("'", '"'))
