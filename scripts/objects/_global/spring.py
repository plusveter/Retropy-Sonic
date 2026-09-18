from scripts.base import *
from ..player.util import player_hurt
from ..player import macros as player_macros

class Spring(TiledObjectEntity):
    diagonal_yield      = 0.725

    color_data = list((
         dict(name="Red"        , strenght=16),
         dict(name="Yellow"     , strenght=10)
    ))

    namedatas = dict(
        red_spring_up           = dict(state="vertical"     , color = 0     , flip=0),
        red_spring_down         = dict(state="vertical"     , color = 0     , flip=1),
        red_spring_left         = dict(state="horizontal"   , color = 0     , flip=1),
        red_spring_right        = dict(state="horizontal"   , color = 0     , flip=0),
 
        red_spring_upleft       = dict(state="diagonal"     , color = 0     , flip=0),
        red_spring_downleft     = dict(state="diagonal"     , color = 0     , flip=1),
        red_spring_downright    = dict(state="diagonal"     , color = 0     , flip=2),
        red_spring_upright      = dict(state="diagonal"     , color = 0     , flip=3),


        yellow_spring_up           = dict(state="vertical"     , color = 1     , flip=0),
        yellow_spring_down         = dict(state="vertical"     , color = 1     , flip=1),
        yellow_spring_left         = dict(state="horizontal"   , color = 1     , flip=1),
        yellow_spring_right        = dict(state="horizontal"   , color = 1     , flip=0),
 
        yellow_spring_upleft       = dict(state="diagonal"     , color = 1     , flip=0),
        yellow_spring_downleft     = dict(state="diagonal"     , color = 1     , flip=1),
        yellow_spring_downright    = dict(state="diagonal"     , color = 1     , flip=2),
        yellow_spring_upright      = dict(state="diagonal"     , color = 1     , flip=3),
    )

    offset_array = numpy.array(
             [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,0,0,0,0,0,0,0,0,0,0],
             dtype=numpy.int8
    )

    def __init__(self, objectid = -1):
        super().__init__(objectid)

        self.bounce_tracker = AnimationTracker(loop=2)
        self.enable_collision = int(self.tiled_properties.get("enable_collision", True))

    def update(self):
        super().update()
        graphic.palette = P_OBJECTS

        self.hitbox = rect(self.tiled_offset.x, self.tiled_offset.y+1, self.tiled_width, self.tiled_height)
        namedata = self.namedatas.get(self.tiled_name, -1)

        if namedata != -1:
            state = namedata["state"]

            strenght = self.color_data[namedata["color"]]["strenght"]
            color = self.color_data[namedata["color"]]["name"]
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

            if player.platform_standing == self.entity_id:
                player.Stand_on_Platform(player.hitbox, self, self.hitbox)

            side = player.Check_Object_Collision_Box(player.hitbox, self, self.hitbox, self.enable_collision)
            if side: 

                if player.Check_Object_Collision_Platform(player.hitbox, self, self.hitbox, 0):
                    player.Stand_on_Platform(player.hitbox, self, self.hitbox)

                if side == C_TOP and flip == 0: 
                        player.ground_angle = 0
                        player.speed.y  = -strenght
                        player.ground = False
                        player.ground_object = False
                        player.platform_standing = -1
                        player.jump_flag = False
                        player.state = player_macros.ST_SPRING_H
                        play_sound(general.SFX_Spring)
                        self.bounce_tracker.loop = 0

                elif side == C_BOTTOM and flip == 1:
                        player.ground_angle = 0
                        player.speed.y  = strenght
                        player.jump_flag = False
                        player.state = player_macros.ST_SPRING_D
                        play_sound(general.SFX_Spring)
                        self.bounce_tracker.loop = 0

        self.hitbox.height  += 16
        if not flip: self.hitbox.top -= 16

        if self.bounce_tracker.loop > 0: self.bounce_tracker.frame = 0
        else: self.bounce_tracker.handle_animation_by_name(general.dynamic_sprites, color+" VerticalSpring")
        prerender_name_sprite(general.dynamic_sprites, color+" VerticalSpring", self.bounce_tracker)
        apply_flip_on_prerender(flipY=flip)
        self.draw(vec2(self.hitbox.center))

    def state_horizontal(self, strenght:float, flip:bool, color:str):

        self.hitbox.width  -= 16
        if not flip: self.hitbox.left += 16

        for player in check_object_by_classname("Player"): 

            if player.platform_standing == self.entity_id:
                player.Stand_on_Platform(player.hitbox, self, self.hitbox)

            side = player.Check_Object_Collision_Box(player.hitbox, self, self.hitbox, self.enable_collision)

            if side: 
                
                if player.Check_Object_Collision_Platform(player.hitbox, self, self.hitbox, 0):
                    player.Stand_on_Platform(player.hitbox, self, self.hitbox)
                    
                if side == C_LEFT and flip == 0: 
                        player.speed.x  = -strenght
                        player.ground_speed = -strenght
                        play_sound(general.SFX_Spring)
                        self.bounce_tracker.loop = 0

                elif side ==  C_RIGHT and flip == 1:
                        player.speed.x  = strenght
                        player.ground_speed = strenght
                        play_sound(general.SFX_Spring)
                        self.bounce_tracker.loop = 0

        self.hitbox.width  += 16
        if not flip: self.hitbox.left -= 16

        if self.bounce_tracker.loop > 0: self.bounce_tracker.frame = 0
        else: self.bounce_tracker.handle_animation_by_name(general.dynamic_sprites, color+" HorizontalSpring")
        prerender_name_sprite(general.dynamic_sprites, color+" HorizontalSpring", self.bounce_tracker)
        apply_flip_on_prerender(flipX=(not flip))
        self.draw(vec2(self.hitbox.center))

    def state_diagonal(self, strenght:float, rotate:bool, color:str):


        speed_cap = False

        offset_array = self.offset_array[::-1]
        direction = vec2(1, -1)

        if rotate == 1:     
            offset_array = self.offset_array[::-1] * -1
            direction = vec2(1, 1)

        elif rotate == 2:   
            offset_array = self.offset_array * -1
            direction = vec2(-1, 1)

        elif rotate == 3:  
            offset_array = self.offset_array 
            direction = vec2(-1, -1)

        lenght = offset_array.shape[0]

        potential_energy = direction * strenght * self.diagonal_yield #kinetic energy

        for player in check_object_by_classname("Player"):

            i = int(max(3 - abs(player.speed.x), 0))
            hitbox2 = rect(self.hitbox.left + i, self.hitbox.top + i, self.hitbox.width + -(i *2), self.hitbox.height + -(i *2))

            if direction.x == -1:
                collision_offset = (player.hitbox.right-self.hitbox.left)
            else:
                collision_offset = (player.hitbox.left - self.hitbox.left)

            offset_index = max(min(player.x - self.x + collision_offset, lenght-1), 0)
            self.hitbox.top += offset_array[int(offset_index)] -1

            if player.platform_standing == self.entity_id:
                player.Stand_on_Platform(player.hitbox, self, self.hitbox)

            side = player.Check_Object_Collision_Box(player.hitbox, self, self.hitbox, self.enable_collision) # Had a param that check collsion

            if side:

                if player.Check_Object_Collision_Platform(player.hitbox, self, self.hitbox, 0):
                    player.Stand_on_Platform(player.hitbox, self, self.hitbox)

            # check if speed_cap is disable
            if not speed_cap:
                potential_energy.x = max(potential_energy.x, player.speed.x) if potential_energy.x > 0 else min(potential_energy.x, player.speed.x)
                potential_energy.y = max(potential_energy.y, player.speed.y) if potential_energy.y > 0 else min(potential_energy.y, player.speed.y)

            if player.Check_Object_Collision_Box(player.hitbox, self, hitbox2, 0):
                player.speed = potential_energy
                player.ground = False
                player.platform_standing = -1
                player.jump_flag = False
                player.state = player_macros.ST_SPRING_D
                player.facing = -direction.y
                play_sound(general.SFX_Spring)
                self.bounce_tracker.loop = 0

            self.hitbox.top -= offset_array[int(offset_index)] -1


        if self.bounce_tracker.loop > 0: self.bounce_tracker.frame = 0
        else: self.bounce_tracker.handle_animation_by_name(general.dynamic_sprites, color+" DiagonalSpring")

        prerender_name_sprite(general.dynamic_sprites, color+" DiagonalSpring", self.bounce_tracker)

        apply_flip_on_prerender(flipX=min(direction.x, 0), flipY=min(-direction.y, 0))
        self.draw(vec2(self.hitbox.center))


        
