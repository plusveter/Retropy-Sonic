from scripts.base import * 

from .offscreenspawner    	import OffscreenSpawner
from .breakabletileregion 	import BreakableTileRegion
from .collision				import (NoSensorDown, NoSensorUp, SetAngle)
from .cameratool			import CameraTool

tiledmap.add_objectclass(OffscreenSpawner)
tiledmap.add_objectclass(BreakableTileRegion)
tiledmap.add_objectclass(NoSensorDown)
tiledmap.add_objectclass(NoSensorUp)
tiledmap.add_objectclass(SetAngle)
tiledmap.add_objectclass(CameraTool)