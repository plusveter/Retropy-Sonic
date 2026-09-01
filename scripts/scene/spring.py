from scripts.base import *
from .player import Player, ST_SPRING_D, ST_SPRING_H

class Ring(TiledObjectEntity):
    def __init__(self, objectid = -1):
        super().__init__(objectid)
        self.animation_tracker = AnimationTracker()
        self.is_boing = False
        self.strenght = 50
        self.direction = [0, 0]

        self.animation_name = ""
        self.strenghts = {"yellow": 11, "red": 20}
        self.flip = []
        self.array = []
        self.isDiagonal = False
        self.setup()

    def setup(self):
        color, anglepos = self.tiled_name.split("_")

        if anglepos == "up":
            self.animation_name = f"{color} VerticalSpring"
            self.flip = [False, False]
            self.isDiagonal = False
            self.array = [0, 16, 32, 16]
            self.direction = [0, -1]

        elif anglepos == "right":
            self.animation_name = f"{color} HorizontalSpring"
            self.flip = [False, False]
            self.isDiagonal = False
            self.array = [0, 0, 16, 32]
            self.direction = [1, 0]

        elif anglepos == "down":
            self.animation_name = f"{color} VerticalSpring" 
            self.flip = [False, True]
            self.isDiagonal = False
            self.array = [0, 0, 32, 16]
            self.direction = [0, 1]

        elif anglepos == "left":
            self.animation_name = f"{color} HorizontalSpring"
            self.flip = [True, False]
            self.isDiagonal = False
            self.array = [16, 0, 16, 36]
            self.direction = [-1, 0]
        

        elif anglepos == "right_up":
            self.animation_name = f"{color} DiagonalSpring"
            self.flip = [False, False]
            self.isDiagonal = True
            self.array = [0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
            self.direction = [0.725, -0.725]

        elif anglepos == "left_up":
            self.animation_name = f"{color} DiagonalSpring"
            self.flip = [True, False]
            self.isDiagonal = True
            self.array = [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,0,0,0,0,0,0,0,0,0,0]
            self.direction = [-0.725, -0.725]

        elif anglepos == "left_down":
            self.animation_name = f"{color} DiagonalSpring"
            self.flip = [True, True]
            self.isDiagonal = True
            self.array = [-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,0,0,0,0,0,0,0,0,0,0]
            self.direction = [-0.725, 0.725]

        elif anglepos == "right_down":
            self.animation_name = f"{color} DiagonalSpring"
            self.flip = [False, True]
            self.isDiagonal = True
            self.array = [0,0,0,0,0,0,0,0,0,0,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20]
            self.direction = [0.725, 0.725]
    
    def update(self):
        super().update()
        flipX, flipY = self.flip
        animation = general.dynamic_sprites
        color, anglepos = self.tiled_name.split("/")
        self.strenght = self.strenghts.get(color, 50)

        
        
        check_player_y = not self.tiled_properties.get("Check_player_yspeed", False)

        for player in []: #check_object(Player)
            if ((not check_player_y) and player.speed[1] >= 0) or check_player_y:
                if self.tiled_properties.get("Collision", True):
                    if self.isDiagonal: self.DiagonalCollisionSet(player)
                    else: self.NormalCollisionSet(player)

                self.Collidewithplayer(player)

        if self.is_boing:
            self.animation_tracker.handle_animation_by_name(animation, self.animation_name)
            if self.animation_tracker.has_looped:self.is_boing = False


        render_name_sprite(general.dynamic_sprites, self.animation_name, self.animation_tracker)
        apply_flip(flipX, flipY)
        self.draw(vec2(16))
    
    def NormalCollisionSet(self, player:Player):
        if False:
            rect_to_rbox(self.array, self.position, self.id, RBOX_ALL_COLLISION)

    def DiagonalCollisionSet(self, player:Player):

        # Managable with property (wont' be activate soon)
        if False:
            rect = collision.rect_to_rbox([0, -1, 32, 32+1], self.position, self.id, RBOX_ALL_COLLISION)
            rect = rect.slope_height(player.position[0], self.array)
            #self.add_rect(rect)

    def Collidewithplayer(self, player:Player):

        if rect_to_rbox([4, 4, 24, 24], self.position, self.id).overlap(player.rect):
            play_sound = False

            if self.isDiagonal:
                player.state = ST_SPRING_D
                if self.direction[0] != 0: player.speed[0] = self.strenght*self.direction[0]
                if self.direction[1] != 0: player.speed[1] = self.strenght*self.direction[1]
                player.ground = False
                player.ground = False
                
            else:
                if self.direction[0] != 0:
                    if player.ground:
                        if (sign(player.ground_speed) != sign(self.strenght*self.direction[0])):
                            player.ground_speed = self.strenght*self.direction[0]
                            play_sound = True
                    else:
                        if (sign(int(player.speed[0]*10)/10) != sign(self.strenght*self.direction[0])):
                            player.speed[0] = self.strenght*self.direction[0]
                            play_sound = True
                            player.ground = False
                
                if self.direction[1] != 0: 
                    player.state = ST_SPRING_H
                    play_sound = True
                    player.ground = False
                    player.speed[1] = self.strenght*self.direction[1]
            

            if play_sound:
                if not self.is_boing:
                    play_sound(general.SFX_Spring)
        
