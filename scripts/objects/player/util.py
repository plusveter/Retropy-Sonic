from scripts.base import *
from .base import PlayerBase
from .macros import *

def player_hurt(self:TiledObjectEntity, player:PlayerBase, center):

    player.hurt_position = center
    if player.knockout_type == 0: player.knockout_type = K_HURT

def __player_check_flailing__(self:TiledObjectEntity, player:PlayerBase, entity_hitbox:pygame.Rect):
    # Calculate collision position
    col_pos = [0, 0]
    if player.facing > 0:
        col_pos = [(self.position.x + (entity_hitbox.left << 16)), (self.position.x + (entity_hitbox.right << 16))]
    else:
        col_pos = [(self.position.x - (entity_hitbox.left << 16)), (self.position.x - (entity_hitbox.right << 16))]

    # Player sensor positions
    """
    sensor_x1 = player.position.x + player.sensorX[0]
    sensor_x3 = player.position.x + player.sensorX[2]
    sensor_x2 = player.position.x + player.sensorX[1]
    sensor_x4 = player.position.x + player.sensorX[3]
    sensor_x5 = player.position.x + player.sensorX[4]

    # Check each sensor against the platform
    if col_pos[0] <= sensor_x1 <= col_pos[1]:
        player.flailing |= 0x01

    if col_pos[0] <= sensor_x2 <= col_pos[1]:
        player.flailing |= 0x02

    if col_pos[0] <= sensor_x3 <= col_pos[1]:
        player.flailing |= 0x04

    if col_pos[0] <= sensor_x4 <= col_pos[1]:
        player.flailing |= 0x08

    if col_pos[0] <= sensor_x5 <= col_pos[1]:
        player.flailing |= 0x10
    """

    # Vertical collision flag
    # if self.speed.y <= 0: player.collisionFlagV |= 1

def player_check_object_collision_platform(self:TiledObjectEntity, player:PlayerBase, entity_hitbox:pygame.Rect):
    if check_object_collision_platform(self, entity_hitbox, player, player.hitbox, True):
        player.control_lock = 0
        player.MODE = G_MODE_FLOOR
        __player_check_flailing__(self, player, entity_hitbox)
        return True

    return False


def player_check_object_collision_platform(self:TiledObjectEntity, player:PlayerBase, entity_hitbox:pygame.Rect):
 

    # Check collision and handle the resulting side
    side = check_object_collision_box(self, entity_hitbox, player, player.hitbox, True)
    if side == C_NONE: return C_NONE

    # ---------------------------------------------------------
    # Top collision
    # ---------------------------------------------------------
    if side == C_TOP:
        player.control_lock = 0
        player.MODE = G_MODE_FLOOR
        __player_check_flailing__(self, player, entity_hitbox)

        return C_TOP

    # ---------------------------------------------------------
    # Left collision
    # ---------------------------------------------------------
    elif side == C_LEFT:
        player.control_lock = 0

        if player.input_left and player.ground:
            player.ground_speed = -0x8000
            player.position.x &= 0xFFFF0000

        return C_LEFT

    # ---------------------------------------------------------
    # Right collision
    # ---------------------------------------------------------
    elif side == C_RIGHT:
        player.control_lock = 0

        if player.input_right and player.ground:
            player.ground_speed = 0x8000

        return C_RIGHT

    # ---------------------------------------------------------
    # Bottom collision
    # ---------------------------------------------------------
    elif side == C_BOTTOM:
        return C_BOTTOM

    # Should never normally be reached
    return C_NONE