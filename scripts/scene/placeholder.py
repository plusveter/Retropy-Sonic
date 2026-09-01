from scripts.base import *


class Placeholder(TiledObjectEntity):
    def update(self):
        super().update()
        graphic.palette = P_OBJECTS
        
        if self.tiled_gid != -1:
            prerender_gid(self.tiled_gid, self.get_special_flags())

            #apply_scale(self.width, self.height)
            adjust_pivot_to_pygame_y()
            #apply_rotation(self.rotation)

            self.draw(vec2(0))
