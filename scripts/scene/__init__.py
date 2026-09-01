from scripts.base import * 

from scripts.scene.placeholder import Placeholder
from scripts.scene.ring import Ring
from scripts.scene.player import Player
from scripts.scene.swapcollisionlayer import SwapCollisionLayer
from scripts.scene.swapbackground import SwapBackground
from scripts.scene.hud import HUD
from scripts.scene.setwaterheight import SetWaterHeight
from scripts.scene.box import Box

from scripts.scene.water.effect import WaterEffect



tiledmap.add_objectclass(Placeholder)
tiledmap.add_objectclass(HUD)
tiledmap.add_objectclass(Player)
tiledmap.add_objectclass(Ring)
tiledmap.add_objectclass(Box)

tiledmap.add_objectclass(SwapBackground)
tiledmap.add_objectclass(SwapCollisionLayer)
tiledmap.add_objectclass(SetWaterHeight)

