from scripts.base import *


class SetWaterHeight(TiledObjectEntity):
    def update(self):
        super().update()
        
        if not camera.has_collided_with_screen(self.bound): return 0

        posY = self.y - self.tiled_height/2
        if general.water_height == posY: return

        general.water_visible = self.tiled_properties.get("visible", False)

       

        general.water_height = posY


        