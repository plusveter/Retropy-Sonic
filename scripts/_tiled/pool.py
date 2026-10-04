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

        def priority_key(objectid):
            obj = self.objects.get(objectid)
            return (
                getattr(obj, "update_priority", 100),
                objectid
            )

        def sort_ids(object_ids):
            return sorted(
                object_ids,
                key=priority_key
            )

        def update_list(object_list):
            for objectid in sort_ids(object_list):
                if objectid in self.updated_object:
                    continue

                self.updated_object.append(objectid)

                if self.objects_focus.get(objectid):
                    focused_objects = self.objects_focus.pop(objectid)
                    update_list(focused_objects)

                obj = self.objects.get(objectid)
                if obj: obj.update()

        update_list(self.objects.keys())
        

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




        


    

