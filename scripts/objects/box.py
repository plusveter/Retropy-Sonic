from scripts.base import *


class Box(TiledObjectEntity):
    
    def update(self):
        super().update()

        graphic.palette = P_OBJECTS

        self.hitbox = rect(self.tiled_offset.x, self.tiled_offset.y, self.tiled_width, self.tiled_height)

        color = 1
        for player in check_object_by_classname("Player"):
            if player.platform_standing == self.entity_id:
                player.Stand_on_Platform(player.hitbox, self, self.hitbox)
                color = 16

            
            if player.Check_Object_Collision_Box(player.hitbox, self, self.hitbox, 1):
                if color != 16 : color = 8

                if player.platform_standing == -1 :
                    
                    if player.Check_Object_Collision_Platform(player.hitbox, self, self.hitbox, 0):
                        player.Stand_on_Platform(player.hitbox, self, self.hitbox)
                
            

        prerender_rect(self.hitbox, color)
        self.draw()
