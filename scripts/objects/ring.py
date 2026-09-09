from scripts.base import *
from .player import Player

class Ring(TiledObjectEntity):
    def __init__(self, objectid = -1):
        super().__init__(objectid)
        self.type = 0
        self.death_timer = 0
        self.isDone = False
        self.sparkles = AnimationTracker()
        
    
    def update(self):
        super().update()
        graphic.palette = P_OBJECTS
        debug = 0
        self.hitbox = rect([8, 8+self.tiled_offset.y, self.tiled_width, self.tiled_height])

        if self.type == "lose":
            chunk_mask = tiledmap.get_chunk_datamask(self.position.x, self.position.y+self.height, 2, 1)


            self.death_timer += 1
            self.speed.y += 0.09375

            sensor_Up = 	rect_to_dmask([-0, -0, 1, 1],   self.position)
            sensor_Down = 	rect_to_dmask([-0, 16, 1, 1], 	self.position)
            sensor_right = 	rect_to_dmask([16, -0, 1, 1], 	self.position)
            sensor_left = 	rect_to_dmask([-0, -0, 1, 1], 	self.position)

            if sensor_right.collide(chunk_mask) and self.speed.x > 0: 
                self.position.x += -(sensor_right.repel_rightside(chunk_mask))
                self.speed.x = -(abs(self.speed.x)*0.9)

            if sensor_left.collide(chunk_mask) and self.speed.x < 0: 
                self.position.x += -(sensor_left.repel_leftside(chunk_mask))
                self.speed.x = (abs(self.speed.x)*0.9) 

            if sensor_Down.collide(chunk_mask) and self.speed.y > 0:
                self.speed.y = self.speed.y*-0.75
                if (self.speed.y) > -1.0: self.speed.y = -1.0
                self.position.y += -(sensor_Down.repel_floor(chunk_mask))

            if sensor_Up.collide(chunk_mask) and self.speed.y < 0:
                self.position.y += -(sensor_Up.repel_ceiling(chunk_mask))
                self.speed.y = 0 

            self.position.x += self.speed.x
            self.position.y += self.speed.y

            if self.death_timer > 130*2:
                self.kill()
                self.delete()

            if debug and False: # no longer renderable
                render(chunk_mask.mask.to_surface(), special_flags=pygame.BLEND_ADD)
                self.draw(-self.position + vec2(chunk_mask.x, chunk_mask.y))

        for player in check_object(Player):
            if self.Check_Object_Collision_Box(self.hitbox, player, player.hitbox, 0) and (not self.type in ["sparkles", "lose"] or self.death_timer > 50) and not self.isDone:
                self.delete()
                general.rings += 1
                play_sound(general.SFX_Ring)
                self.type = "sparkles"
                self.isDone = True

        if self.type == "sparkles":
            Animation_ = f"Sparkle Ring"
            self.sparkles.handle_animation_by_name(general.dynamic_sprites, Animation_)
            if self.sparkles.has_looped: self.kill()
            else:
                prerender_name_sprite(general.dynamic_sprites, Animation_, self.sparkles)
                self.draw(vec2(self.hitbox.x, self.hitbox.y))


        # Check if object is a spakles, otherwise it render the ring sprite

        if  (self.death_timer < 130 or (self.death_timer%2) == 0) and not self.isDone:
            prerender_name_sprite(general.dynamic_sprites, "Normal Ring", general.ring_tracker)
            self.draw(vec2(self.hitbox.x, self.hitbox.y))
    
    