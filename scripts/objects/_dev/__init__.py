from scripts.base import * 

from .offscreenspawner    import OffscreenSpawner
from .breakabletileregion import BreakableTileRegion

tiledmap.add_objectclass(OffscreenSpawner)
tiledmap.add_objectclass(BreakableTileRegion)