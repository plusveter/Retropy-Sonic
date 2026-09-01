from scripts.base import *
from .player import Player

class SwapCollisionLayer(TiledObjectEntity):
    def __init__(self, objectid = -1):
        super().__init__(objectid)

        # need to ask about a feature with BJORN 
        layer = tiledmap.layers_classname.get(self.tiled_properties.get("layer_class", -1), -1)
        self.specific_layerid = layer.id if layer != -1 else -1

        layer = tiledmap.layers_classname.get(self.tiled_properties.get("red", -1), -1)
        self.layer_class_red = layer.id if layer != -1 else -1

        layer = tiledmap.layers_classname.get(self.tiled_properties.get("blue", -1), -1)
        self.layer_class_blue = layer.id if layer != -1 else -1

    
    def update(self):
        # [IMPORTANT] this feature is required for the system
        super().update()

        # 
        self.handle_direction()

        # make a new rectbox which is basically a rect
        rectbox  = rect_to_rbox([0, -self.tiled_height * (self.tiled_gid > 0), self.tiled_width, self.tiled_height], self.position, self.tiled_id)

        # draw on screen the rectbox
        #render_rect(rectbox.rect, [255, 128, 0], special_flags=pygame.BLEND_ADD)	;self.draw(-self.position)


        # look for object with the same class type 
        for player in check_object(Player):
            #
            self.handle_mouvement(player)
            
            # skip this player if he had the same layerid value as the swapcollision
            if (player.ground_layer == self.specific_layerid) or (self.specific_layerid == -1): continue # this help skip in the loop 

            # look for collision between the two
            if player.rectbox.overlap(rectbox): player.ground_layer = self.specific_layerid

    def handle_direction(self):
        if self.tiled_name == "direction_up": 
            if get_pressed(K_UP): self.specific_layerid = self.layer_class_red

        elif self.tiled_name == "direction_vertical": 
            if get_pressed(K_UP) : self.specific_layerid = self.layer_class_red
            elif get_pressed(K_DOWN):  self.specific_layerid = self.layer_class_blue 

    def handle_mouvement(self, player:Player):
        if self.tiled_name == "movement_right":
            if player.speed.x > 0: self.specific_layerid = self.layer_class_red

        elif self.tiled_name == "movement_left": 
            if player.speed.x < 0: self.specific_layerid = self.layer_class_red

        elif self.tiled_name == "movement_vertical": 
            if player.speed.x > 0: self.specific_layerid = self.layer_class_red
            elif player.speed.x < 0: self.specific_layerid = self.layer_class_blue


    
    