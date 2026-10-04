from scripts.base import *
from ..player.util import player_hurt

class Spikes(TiledObjectEntity):
    namedatas = {
        "spikes_top":       dict(frame=0, flipH=False, flipV=False),
        "spikes_bottom":    dict(frame=0, flipH=True, flipV=False),
        "spikes_left":      dict(frame=1, flipH=False, flipV=True),
        "spikes_right":     dict(frame=1, flipH=False, flipV=False),
    }
    
    # This is one of if not the easiest object to work on
    def update(self):
        super().update()
        graphic.palette = P_OBJECTS

        self.hitbox = rect(self.tiled_offset.x, self.tiled_offset.y, self.tiled_width, self.tiled_height)
        transform = self.namedatas.get(self.tiled_name, -1)
        
        color = 1
        for player in check_object_by_classname("Player"):
            tiledmap.pool.add_preceding_obj(player, self.tiled_id)
            if player.platform_standing == self.entity_id:
                player.Stand_on_Platform(player.hitbox, self, self.hitbox)
                color = 16

            collision_side = player.Check_Object_Collision_Box(player.hitbox, self, self.hitbox, 1)
            
            if collision_side == C_TOP:
                if player.speed.y >= 0 and self.tiled_name == "spikes_top":
                    player_hurt(self, player, vec2(self.hitbox.center) + self.position)

                if player.platform_standing == -1 :
                    if player.Check_Object_Collision_Platform(player.hitbox, self, self.hitbox, 0):
                        player.Stand_on_Platform(player.hitbox, self, self.hitbox)

            elif collision_side == C_BOTTOM:
                if player.speed.y <= 0 and self.tiled_name == "spikes_bottom":
                    player_hurt(self, player, vec2(self.hitbox.center) + self.position)

            elif collision_side == C_LEFT:
                if player.speed.x >= 0 and self.tiled_name == "spikes_left":
                    player_hurt(self, player, vec2(self.hitbox.center) + self.position)

            elif collision_side == C_RIGHT:
                if player.speed.x <= 0 and self.tiled_name == "spikes_right":
                    player_hurt(self, player, vec2(self.hitbox.center) + self.position)

        if transform != -1:
            prerender_name_sprite(general.dynamic_sprites, "Spikes", AnimationTracker(frame=transform["frame"]))
            apply_flip_on_prerender(flipY=transform["flipH"], flipX=transform["flipV"])
            self.draw(vec2(self.hitbox.center))

        else:
            prerender_rect(self.hitbox, color)
            self.draw() 
        
