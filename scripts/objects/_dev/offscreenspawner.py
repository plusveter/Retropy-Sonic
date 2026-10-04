from scripts.base import *

class OffscreenSpawner(TiledObjectEntity):


    def __init__(self, objectid: int = -1):
        self.spawned_objectid = -1
        self.spawned_object = None
        self.spawn_once = True
        self.keep_alive = True

        super().__init__(objectid)

        
    def setup(self):
        self.spawned_objectid = int(self.tiled_properties.get("spawned_objectid", 0))
        self.spawn_once = self.tiled_properties.get("spawn_once", True)
        self.keep_alive = self.tiled_properties.get("keep_alive", True)
        self.try_spawn_object()

        # cancel this function, once it has load
        def func(): ...
        self.setup = func

    def update(self):
        self.setup()
        super().update()

        self.try_keep_object_alive()


    def try_spawn_object(self):

        if self.spawned_objectid == 0:
            return

        if tiledmap.pool.objects.get(self.spawned_objectid):
            self.spawned_object = tiledmap.pool.objects[self.spawned_objectid]
            return

        object_data = tiledmap.objects.get(self.spawned_objectid)

        if not object_data:
            return

        objectclass = tiledmap.objectclass_dict.get(object_data["type"])

        if objectclass is None:
            objectclass = tiledmap.objectclass_dict.get("Placeholder")

        if objectclass is None:
            raise NotImplementedError(
                f"[{self.__class__.__name__}] The Placeholder does not exist :\n"
                f"Please create a universal object for placeholder. "
            )

        objectclass(self.spawned_objectid)

        self.spawned_object = tiledmap.pool.objects.get(self.spawned_objectid)

    def try_keep_object_alive(self):
        if not self.keep_alive:
            return
        
        current_object = tiledmap.pool.objects.get(self.spawned_objectid)

        if current_object:
            current_object.revoke_offscreenlimit = True
            self.spawned_object = current_object
            return

        if self.spawn_once:
            return

        self.spawned_object = None
        self.try_spawn_object()



    
    