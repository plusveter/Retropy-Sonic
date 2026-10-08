from scripts.base import *

from scripts.objects._global.particle import Particle
from scripts.objects.player.macros  import *

class Monitor(TiledObjectEntity):
    namedatas = {
        "monitor": "Monitor",
        "monitor_icon": "MonitorIcon",
    }

    icon_frames = {
        "Rings10": 0,
        "Invincibility": 1,
        "SpeedUp": 2,
        "Bubble": 3,
        "Fire": 4,
        "Electric": 5,
        "Life": 6,
    }

    brokens = []

    def __init__(self, objectid: int = -1):
        self.speed = vec2(0)

        self.destroyed = False
        self.ground = True
        self.culling = True

        self.icons_end = 50
        self.icon_frame = 0

        self.static_tracker = AnimationTracker()
        self.monitor_tracker = AnimationTracker()
        self.player_object = None

        super().__init__(objectid)

        self.monitor_type = self.tiled_properties.get("monitor_type", "Rings10")

        if self.tiled_name in self.icon_frames:
            self.monitor_type = self.tiled_name
            self.tiled_properties["monitor_type"] = self.monitor_type
            self.tiled_name = "Monitor"

        layer = tiledmap.layers_classname.get(self.tiled_properties.get("collision_layer", -1), -1)
        self.collision_layer = layer.id if layer != -1 else -1

        if self.tiled_name == "monitor_icon":
            self.icon_frame = self.icon_frames.get(self.monitor_type, 0)
            self.icons_end = 50
            self.speed.y = -20

        else:
            self.destroyed = self.tiled_properties.get("destroyed", False)
            self.ground = self.tiled_properties.get("ground", True)
            self.culling = self.tiled_properties.get("culling", True)

            self.icon_frame = self.icon_frames.get(self.monitor_type, 0)

            self.static_tracker.timer = ((self.tiled_id % 5) + 1) * 100
            self.static_tracker.frame = ((self.tiled_id % 5) + 1)

    def kill(self):
        if self.tiled_name != "monitor_icon":
            self.tiled_properties["monitor_type"] = self.monitor_type
            self.tiled_properties["destroyed"] = self.destroyed
            self.save()
        return super().kill()
    
    def update(self):
        super().update()

        graphic.palette = P_OBJECTS

        if self.tiled_name == "monitor_icon":
            self.update_icon()
        else:
            self.update_monitor_collision()
            self.update_monitor_render()

    def update_icon(self):
        self.icons_end -= 1
        self.speed.y = self.speed.y / 1.2
        self.position.y += self.speed.y / 5

        if self.icons_end <= 0:
            self.kill()
            return

        if self.icons_end == 10:
            self.apply_powerup()

        prerender_name_sprite(general.dynamic_sprites, "MonitorIcons", AnimationTracker(frame=self.icon_frame))
        self.draw(vec2(16, 16))

    def apply_powerup(self):
        if self.monitor_type == "Rings10":
            general.rings += 10
            play_sound(general.SFX_Ring)

        elif self.monitor_type == "Invincibility":
            self.player_object.invincible_timer = 512

        elif self.monitor_type == "SpeedUp":
            self.player_object.speedup_timer = 512

        elif self.monitor_type == "Bubble":
            self.player_object.shield = S_BUBBLE

        elif self.monitor_type == "Fire":
            self.player_object.shield = S_FIRE

        elif self.monitor_type == "Electric":
            self.player_object.shield = S_ELECTRIC

        elif self.monitor_type == "Life":
            general.lives += 1
            play_sound(general.SFX_1Up)

    def check_ground(self):
        if self.ground:
            self.position.y += self.speed.y
            self.speed.y += 0.2

            chunk_mask = tiledmap.get_chunk_datamask(
                self.position.x,
                self.position.y + 32,
                2,
                self.collision_layer
            )

            sensor_Down = rect_to_dmask(
                [0, 32, 25, 1],
                self.position
            )

            if sensor_Down.collide(chunk_mask) and self.speed.y > 0:
                self.position.y += -(sensor_Down.repel_floor(chunk_mask))
                self.ground = True
                self.speed.y = 0
                self.position.y = math.floor(self.position.y)

        else:
            self.position.y = math.floor(self.position.y)

    def update_monitor_collision(self):
        self.hitbox = rect(
            4,
            self.tiled_offset.y,
            25,
            32
        )

        collision_flag = False
        image_yscale = 1

        if not self.destroyed:
            
            for player in check_object_by_classname("Player"):
                cond = not (player.state in [ST_JUMP, ST_ROLL])
                collision_side = player.Check_Object_Collision_Box(
                    player.hitbox,
                    self,
                    self.hitbox,
                    cond
                )

                if (
                    collision_side == C_TOP
                    and image_yscale == 1
                    and player.speed.y <= 0
                ):
                    collision_flag = True
                    self.ground = False
                    self.speed.y = -2
                    player.speed.y = 1

                if player.state in [ST_JUMP, ST_ROLL, ST_DROPDASH, ST_SPINDASH]:
                    if collision_side and not collision_flag:
                        self.destroy_monitor(player, image_yscale)
                        break

        else:
            collision_flag = False
            image_yscale = 1

        if not self.tiled_properties.get("gravity", False):
            self.ground = True

        self.check_ground()


    def destroy_monitor(self, player:TiledObjectEntity, image_yscale=1):
        self.destroyed = True
        self.tiled_properties["destroyed"] = True
        self.tiled_properties["monitor_type"] = self.monitor_type
        self.ground = False

        self.speed.y = -2 * sign(image_yscale)
        self.check_ground()

        player.speed.y = max(abs(player.speed.y), 4) * -sign(image_yscale)

        icon = Monitor()
        icon.tiled_name = "monitor_icon"
        icon.position = vec2(self.position)
        icon.monitor_type = self.monitor_type
        icon.icon_frame = self.icon_frame
        icon.speed.y = -20
        icon.player_object = player
        icon.tiled_layerid = self.tiled_layerid

        particle = Particle()
        particle.position = vec2(self.position) + (self.tiled_size/2)
        particle.specification = 0
        particle.tiled_layerid = self.tiled_layerid
        particle.animation_name = "Explosion 0"

        play_sound(general.SFX_Destroy)

    def update_monitor_render(self):
        if not self.destroyed:
            prerender_name_sprite(general.dynamic_sprites, "MonitorIcons", AnimationTracker(frame=self.icon_frame))
            self.draw(vec2(16, 16))

            self.static_tracker.handle_animation_by_name(
                general.dynamic_sprites,
                "MonitorStatic"
            )
            prerender_name_sprite(
                general.dynamic_sprites,
                "MonitorStatic",
                self.static_tracker
            )
            self.draw(vec2(16, 16))

        self.monitor_tracker.frame = int(self.destroyed)
        prerender_name_sprite(
            general.dynamic_sprites,
            "Monitor",
            self.monitor_tracker
        )
        self.draw(vec2(16, 16))