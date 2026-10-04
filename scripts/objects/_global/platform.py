from scripts.base import *


class Platform(TiledObjectEntity):
        variants = {
                "Normal": dict(width=64, height=32)
        }

        ammount = 4
        height = 16

        def __init__(self, objectid: int = -1):
                super().__init__(objectid)

                self.spawn_coord = self.position.copy()

                if not hasattr(self, "type") or self.type is None:
                        self.type = 0

                self.hitbox = rect(0, 0, 0, 0)

        def update(self):
                super().update()
                print(kernel.frames, self.__class__.__name__)
                graphic.palette = P_OBJECTS

                properties = self.tiled_properties

                
                platform_movement = general.platform_movement

                if properties.get("FlipSync"):
                        platform_movement = (platform_movement + math.pi) % (math.pi * 2)

                movement_value = math.sin(platform_movement)

                move_x = properties.get("MoveX", 0)
                move_y = properties.get("MoveY", 0)

                if move_x:
                        move_x *= 0.5
                        self.position.x = self.spawn_coord.x + (movement_value * move_x) + move_x

                if move_y:
                        move_y *= 0.5
                        self.position.y = self.spawn_coord.y + (movement_value * move_y) + move_y

                self.hitbox = rect(
                        self.tiled_offset.x,
                        self.tiled_offset.y,
                        self.tiled_width,
                        self.tiled_height
                )
                self.refresh_entity_collision()

                animation = properties.get("Animation", "Platforms")

                dynamic_sprites = general.dynamic_sprites
                new_animation_tracker = AnimationTracker(frame=self.type)

                
                prerender_name_sprite(
                        dynamic_sprites,
                        animation,
                        new_animation_tracker
                )

                self.draw(vec2(self.tiled_width / 2, self.tiled_height / 2))

        def refresh_entity_collision(self):
                for player in check_object_by_classname("Player"):
                        tiledmap.pool.add_preceding_obj(player, self.tiled_id)
                        standing_on_platform = player.platform_standing == self.entity_id

                        colliding_with_platform = player.Check_Object_Collision_Platform(
                                player.hitbox,
                                self,
                                self.hitbox,
                                0
                        )

                        if standing_on_platform or colliding_with_platform:
                                # tiledmap.pool.add_preceding_obj(self, player.tiled_id)
                                
                                player.Stand_on_Platform(
                                        player.hitbox,
                                        self,
                                        self.hitbox
                                )