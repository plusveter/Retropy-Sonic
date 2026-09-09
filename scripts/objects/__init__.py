from scripts.base import * 

from scripts.objects.placeholder import Placeholder
from scripts.objects.ring import Ring
from scripts.objects.player import Player
from scripts.objects.swapcollisionlayer import SwapCollisionLayer
from scripts.objects.swapbackground import SwapBackground
from scripts.objects.hud import HUD
from scripts.objects.setwaterheight import SetWaterHeight
from scripts.objects.box import Box

from scripts.objects.water.effect import WaterEffect



tiledmap.add_objectclass(Placeholder)
tiledmap.add_objectclass(HUD)
tiledmap.add_objectclass(Player)
tiledmap.add_objectclass(Ring)
tiledmap.add_objectclass(Box)

tiledmap.add_objectclass(SwapBackground)
tiledmap.add_objectclass(SwapCollisionLayer)
tiledmap.add_objectclass(SetWaterHeight)

