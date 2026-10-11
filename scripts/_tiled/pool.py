from typing import overload, TypeVar
from retropy import *


class TiledObjectPool:
    def __init__(self, tiledmap):
        self.tiledmap = tiledmap
        self.objects = {}
        self.objects_type = {}
        self.prerenders_layers = {}

        self.updated_object = []
        self.objects_focus = {}

        self.rects = {}


    def spawn(self, object:type):
        # Check if object already exist to make sure it won't duplicate attribut
        if self.objects.get(object.tiled_id): return

        self.objects[object.tiled_id] = object
        objectclassname = object.__class__.__name__

        # Create a new list for class_names
        if not self.objects_type.get(objectclassname): self.objects_type[objectclassname] = []
        # add the object into the specific list
        self.objects_type[objectclassname].append(object)

    def kill(self, object):
        # Check if object still exist, before killing it
        if self.objects.get(object.tiled_id): self.objects.pop(object.tiled_id)
        objectclassname = object.__class__.__name__

        if self.objects_type.get(objectclassname):
            #remove the object from the specific list
            if object in self.objects_type[objectclassname]: self.objects_type[objectclassname].remove(object)

            # check if it can delete the specific list for these class_names
            if len(self.objects_type[objectclassname]) == 0: self.objects_type.pop(objectclassname)

    def updates(self):
        self.prerenders_layers = {}
        self.updated_object = []

        pending = list(self.objects.keys())
        queued = set(pending)

        def priority_key(objectid):
            obj = self.objects.get(objectid)
            return (
                getattr(obj, "update_priority", 100),
                objectid
            )

        while pending:
            pending.sort(key=priority_key)
            objectid = pending.pop(0)
            queued.discard(objectid)

            if objectid in self.updated_object:
                continue

            self.updated_object.append(objectid)

            focused_objects = self.objects_focus.pop(objectid, [])
            for focused_id in focused_objects:
                if focused_id in self.updated_object:
                    continue
                if focused_id in queued:
                    continue
                if not self.objects.get(focused_id):
                    continue

                pending.append(focused_id)
                queued.add(focused_id)

            obj = self.objects.get(objectid)
            if obj:
                obj.update()
        

    def add_preceding_obj(self, object:type, preceding_obj_id):
        if object.tiled_id == preceding_obj_id: return 1
        if not self.objects_focus.get(object.tiled_id): self.objects_focus[object.tiled_id] = []
        self.objects_focus[object.tiled_id].append(preceding_obj_id)

    def render(self, layerid:int):
        prerenders_layer = self.prerenders_layers.get(layerid)

        if not prerenders_layer is None: 
            for ordered_list in sorted(prerenders_layer.keys()):
                for data in prerenders_layer[ordered_list]:
                    surfarray, position, special_flags, palette_id = data
                    prerender(surfarray, position-self.tiledmap.offeset_views[layerid], special_flags, palette_id=palette_id)
                    draw_prerender()




        


    

