from scripts.base import * 

from .placeholder import Placeholder
from .ring import Ring
from .player import Player
from .swapcollisionlayer import SwapCollisionLayer
from .swapbackground import SwapBackground
from .hud import HUD
from .setwaterheight import SetWaterHeight
from .box import Box

from .water.effect import WaterEffect

tiledmap.add_objectclass(Placeholder)
tiledmap.add_objectclass(HUD)
tiledmap.add_objectclass(Player)
tiledmap.add_objectclass(Ring)
tiledmap.add_objectclass(Box)

tiledmap.add_objectclass(SwapBackground)
tiledmap.add_objectclass(SwapCollisionLayer)
tiledmap.add_objectclass(SetWaterHeight)

from ._global import *

tiledmap.add_objectclass(Spikes)

