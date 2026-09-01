from scripts.base import *


class Box(TiledObjectEntity):
    
    def update(self):
        super().update()

        graphic.palette = P_OBJECTS

        self.hitbox = rect(self.tiled_offset.x, self.tiled_offset.y, self.tiled_width, self.tiled_height)

        color = 1
        for player in check_object_by_classname("Player"):
            if check_object_collision_box(self, self.hitbox, player, player.hitbox, 1):
                color = 8
                if check_object_collision_platform(self, self.hitbox, player, player.hitbox, 1):
                    color = 16

        prerender_rect(self.hitbox, color)
        self.draw()
