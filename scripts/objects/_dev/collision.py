
from scripts.base import *


class Collision(TiledObjectEntity):
    def __init__(self, objectid: int = -1):
        super().__init__(objectid)

        self.check_ground = self.tiled_properties.get("check_ground", False)
        self.collision_type = self.tiled_properties.get("collision_type", -1)

    def update(self):
        super().update()

        self.hitbox = rect([
            0,
            -self.tiled_height * (self.tiled_gid > 0),
            self.tiled_width,
            self.tiled_height,
        ])


class SetAngle(Collision):
    def __init__(self, objectid: int = -1):
        super().__init__(objectid)

        self.basecollision = self.tiled_properties.get("angle", "Y")

    def update(self):
        super().update()

        for player in check_object_by_classname("Player"):
            tiledmap.pool.add_preceding_obj(player, self.tiled_id)
            if self.Check_Object_Collision_Box(self.hitbox, player, player.hitbox, 0):
                player.setAngle = self.basecollision


class NoSensorUp(Collision):
    def update(self):
        super().update()

        for player in check_object_by_classname("Player"):
            if self.Check_Object_Collision_Box(self.hitbox, player, player.hitbox, 0):
                player.CONTR_sensor = "0"


class NoSensorDown(Collision):
    def update(self):
        super().update()

        for player in check_object_by_classname("Player"):
            if self.Check_Object_Collision_Box(self.hitbox, player, player.hitbox, 0):
                player.CONTR_sensor = "1"