from scripts.base import * 

from .spikes    import Spikes
from .spring    import Spring
from .bridge    import Bridge
from .platform  import Platform
from .particle  import Particle


tiledmap.add_objectclass(Spikes)
tiledmap.add_objectclass(Bridge)
tiledmap.add_objectclass(Spring)
tiledmap.add_objectclass(Platform)
tiledmap.add_objectclass(Particle)

