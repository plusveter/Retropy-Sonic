from scripts.base import *
from .base import PlayerBase
from .macros import *

def player_hurt(self:TiledObjectEntity, player:PlayerBase, center):

    player.hurt_position = center
    if player.knockout_type == 0: player.knockout_type = K_HURT
