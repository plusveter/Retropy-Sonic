from scripts.base import *

class SwapBackground(TiledObjectEntity):
    def update(self):
        # [IMPORTANT] this feature is required for the system
        super().update()

        select_bg = self.tiled_properties.get("select", -1)
        if not select_bg in background.namelist: 
            print("Background not defined in the map")
            return 0
        if not camera.has_collided_with_screen(self.bound): return 0
        if not background.current is None:
            if background.current.id == select_bg : return 0
        
        
        background.use(self.tiled_properties["select"])

        if not isinstance(general.backgrounds_pal.get(select_bg, -1), int): 
            set_palette(general.backgrounds_pal[select_bg], P_BACKGROUND)
                
                



    
    