from scripts.base import *
from ..player.util import player_hurt
from ..player import macros as player_macros

class Spring(TiledObjectEntity):
    yellow_strenght     = 10
    red_strenght        = 10
    diagonal_yield      = 0.725

    namedatas = dict(
        red_spring_up           = dict(state="vertical"     , color = "red"     , flip=0),
        red_spring_down         = dict(state="vertical"     , color = "red"     , flip=1),
        red_spring_left         = dict(state="horizontal"   , color = "red"     , flip=1),
        red_spring_right        = dict(state="horizontal"   , color = "red"     , flip=0),

        red_spring_upleft       = dict(state="diagonal"     , color = "red"     , flip=0),
        red_spring_downleft     = dict(state="diagonal"     , color = "red"     , flip=1),
        red_spring_downright    = dict(state="diagonal"     , color = "red"     , flip=2),
        red_spring_upright      = dict(state="diagonal"     , color = "red"     , flip=3),

    )

    offset_array = numpy.array(
             [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,0,0,0,0,0,0,0,0,0,0],
             dtype=numpy.uint8
        )

    def __init__(self, objectid = -1):
        super().__init__(objectid)
        self.bounce_tracker = AnimationTracker()

    
    def update(self):
        super().update()
        graphic.palette = P_OBJECTS

        self.hitbox = rect(self.tiled_offset.x, self.tiled_offset.y, self.tiled_width, self.tiled_height)
        namedata = self.namedatas.get(self.tiled_name, -1)

        if namedata != -1:
            state = namedata["state"]

            strenght = 0
            color = "Red"
            if namedata["color"] == "red":      strenght = self.red_strenght; color = "Red"
            elif namedata["color"] == "yellow": strenght = self.yellow_strenght; color = "Yellow"

            flip = namedata["flip"]

            if state == "horizontal": self.state_horizontal(strenght, flip, color)
            elif state == "vertical": self.state_vertical(strenght, flip, color)
            elif state == "diagonal": self.state_diagonal(strenght, flip, color)

        else:
            prerender_rect(self.hitbox, 4)
            self.draw()       

    def state_vertical(self, strenght:float, flip:bool, color:str):

        self.hitbox.height  -= 16
        if not flip: self.hitbox.top += 16

        for player in check_object_by_classname("Player"): 
            side = player.Check_Object_Collision_Box(player.hitbox, self, self.hitbox, 1)
            if side == C_TOP and flip == 0: 
                    player.ground_angle = 0
                    player.speed.y  = -strenght
                    player.ground = False
                    player.ground_object = False
                    player.platform_standing = -1
                    player.jump_flag = False
                    player.state = player_macros.ST_SPRING_H
                    play_sound(general.SFX_Spring)

            elif side == C_BOTTOM and flip == 1:
                    player.ground_angle = 0
                    player.speed.y  = strenght
                    player.jump_flag = False
                    player.state = player_macros.ST_SPRING_D
                    play_sound(general.SFX_Spring)

        self.hitbox.height  += 16
        if not flip: self.hitbox.top -= 16

        prerender_name_sprite(general.dynamic_sprites, color+" VerticalSpring", self.bounce_tracker)
        apply_flip_on_prerender(flipY=flip)
        self.draw(vec2(self.hitbox.center))

    def state_horizontal(self, strenght:float, flip:bool, color:str):

        self.hitbox.width  -= 16
        if not flip: self.hitbox.left += 16

        for player in check_object_by_classname("Player"): 
            side = player.Check_Object_Collision_Box(player.hitbox, self, self.hitbox, 1)
            if side == C_LEFT and flip == 0: 
                    player.speed.x  = -strenght
                    player.ground_speed = -strenght
                    play_sound(general.SFX_Spring)

            elif side ==  C_RIGHT and flip == 1:
                    player.speed.x  = strenght
                    player.ground_speed = strenght
                    play_sound(general.SFX_Spring)

        self.hitbox.width  += 16
        if not flip: self.hitbox.left -= 16

        prerender_name_sprite(general.dynamic_sprites, color+" HorizontalSpring", self.bounce_tracker)
        apply_flip_on_prerender(flipX=(not flip))
        self.draw(vec2(self.hitbox.center))

    def state_diagonal(self, strenght:float, rotate:bool, color:str):
        hitbox2 = rect(self.hitbox.left + 8, self.hitbox.top + 8, self.hitbox.width + -16, self.hitbox.height + -16)

        offset_array = self.offset_array
        direction = vec2(1, -1)

        if rotate == 1:     
            offset_array = offset_array * -1
            direction = vec2(1, 1)

        elif rotate == 2:   
            offset_array = offset_array[::-1]
            direction = vec2(-1, 1)

        elif rotate == 3:  
            offset_array = offset_array[::-1] * -1
            direction = vec2(-1, -1)


        for player in check_object_by_classname("Player"):
            offset_index = min(max(player.hitbox.left - self.hitbox.left, offset_array.shape), 0)
            self.hitbox.top += offset_array[offset_index]

            side = player.Check_Object_Collision_Box(player.hitbox, self, self.hitbox, 1)
            if side:
                 if player.Check_Object_Collision_Box(player.hitbox, self, hitbox2, 0):
                      player.speed = direction * strenght * self.diagonal_yield
                      player.ground = False
             
        prerender_name_sprite(general.dynamic_sprites, color+" DiagonalSpring", self.bounce_tracker)
        self.draw(vec2(self.hitbox.center))


        
