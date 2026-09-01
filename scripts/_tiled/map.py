from .dataclass import *
from .macro import *
from .pool import TiledObjectPool
import struct, zlib, gzip 
from base64 import b64decode
import zstandard as zstd



#------------------------------------------------------------------------------------
#   Author: PlusVeter
#------------------------------------------------------------------------------------


class TiledMap:
    def __init__(self):
        # [General]
        self.layers:dict[str, TiledDataLayer] = {}
        self.layers_classname:dict[str, TiledDataLayer] = {}
        self.layer_lastid = 0
        self.offeset_views = {}
        
        # [Tile side]
        self.tilelayers_datachunks = {}
        self.tilelayers_array = {}
        self.ground_angles = {}
        self.tiles = {}
        self.data = None
        self.tilesets = {}

        # [Object side]
        self.objectnames = {}
        self.objecttypes = {}
        self.templates = {}
        self.objects = {}
        self.object_chunks = {}
        self.objectlayers = {}
        self.pool  = TiledObjectPool(self)
        self.object_idorder = 0

        # params
        self.chunk_size = vec2(128)
        self.offscreen_spawn = vec2(64)
        self.objectclass_dict = {}
        self.view_rect = pygame.Rect(0, 0, 0, 0)
        self.offscreen_rect = pygame.Rect(0, 0, 0 ,0)

        self.path = ""
    
    # [DataSets]
    def reset(self, object_is_refreshed=True, tilelayer_array =True):
        # [General]
        self.layer_lastid = 0
        self.layers:dict[str, TiledDataLayer] = {}
        self.layers_classname:dict[str, TiledDataLayer] = {}
        
        # [Tile side]
        self.tilelayers_datachunks = {}
        if tilelayer_array: self.tilelayers_array = {}
        self.ground_angles = {}
        self.tiles = {}
        self.data = None
        self.tilesets:dict[str, TiledDataTileset] = {}

        # [Object side]
        if object_is_refreshed:
            self.objectnames = {}
            self.templates = {}
            self.objects:dict[str, dict] = {}
            self.object_chunks:dict[str, list[int]] = {}
            self.objectlayers:dict[str, list[int]] = {}
            self.pool  = TiledObjectPool(self)
            self.object_idorder = 0

    def load(self,  pathmap:str):
        # put this into annother function, since we can recycle the class
        extensionfile = get_extension(pathmap)
        self.path = pathmap
        if extensionfile in ["tmj", "json"]:
            self.load_json_map(pathmap)
        else:
            raise NotImplementedError(
                f"[{self.__class__.__name__}] Can't load your mapfile: \n   => ({pathmap})\n"+
                f"Please use other type of file type such as '.TMJ' or '.JSON', instead of '.{(extensionfile.upper())}'. "
            )
    
    def get_tile(self, x:int, y:int, tilelayer_id:int) -> int:
        # position & math
        chunk_width, chunk_height = self.data.chunk_width, self.data.chunk_height

        tile_x = x%chunk_width
        tile_y = y%chunk_height

        chunk_x = x - tile_x
        chunk_y = y - tile_y



        # data
        tilesets_chunk = self.tilelayers_datachunks.get(f'{chunk_x}|{chunk_y}')
        if tilesets_chunk:
            chunk_data = tilesets_chunk.get(tilelayer_id)
            if not chunk_data is None:
                return chunk_data[tile_y, tile_x]
        return 0
        
    def set_tile(self, tile_id, x:int, y:int, tilelayer_id:int):
        # position & math
        chunk_width, chunk_height = self.data.chunk_width, self.data.chunk_height

        tile_x = x%chunk_width
        tile_y = y%chunk_height

        chunk_x = x - tile_x
        chunk_y = y - tile_y



        if not self.does_chunk_exist(chunk_x, chunk_y, tilelayer_id):
            self.set_chunk(numpy.zeros((chunk_width * chunk_height)).reshape((chunk_width, chunk_height)), chunk_x, chunk_y, tilelayer_id)
        self.tilelayers_datachunks[f'{chunk_x}|{chunk_y}'][tilelayer_id][tile_y, tile_x] = tile_id

    def set_chunk(self, data:numpy.ndarray, chunk_x:int, chunk_y:int, tilelayer_id:int):

        position = f'{chunk_x}|{chunk_y}'

        if not self.tilelayers_datachunks.get(position): self.tilelayers_datachunks[position] = {}
        self.tilelayers_datachunks[position][tilelayer_id] = data

    def does_chunk_exist(self, chunk_x:int, chunk_y:int, tilelayer_id:int): 
        # position & math
        tilesets_chunk = self.tilelayers_datachunks.get(f'{chunk_x}|{chunk_y}')
        if tilesets_chunk:  return not (tilesets_chunk.get(tilelayer_id) is None)
        else:               return False

    def new_layer(self, data:dict = {}) -> TiledDataLayer:
        tilelayer = TiledDataLayer(data)
        if tilelayer.id < 0: tilelayer.id = self.layer_lastid = (self.layer_lastid + 1)
        return tilelayer

    def add_layer(self, new_layer:TiledDataLayer):
        self.layers[new_layer.id] = new_layer
        self.layers_classname[new_layer.classname] = new_layer
        self.layer_lastid = max(self.layer_lastid, new_layer.id)
        
    def add_object(self, data:dict):
        object_id = data["id"]

        if self.objects.get(object_id): return # skip the entire function cuz of this dilema
        chunk_width, chunk_height = self.chunk_size
        self.object_idorder += 1
        
        
        x, y = data["x"], data["y"]
        template = data.get("template")

        # definitive ??? or not
        template_gid = -1
        template_rotation = 0

        if template:
            template = self.templates[template]["object"]
            width 			= data.get("width"	, template["width"])
            height 			= data.get("height"	, template["height"])
            object_name 	= data.get("name"	, template["name"])
            objecttype 		= data.get("type"	, template["type"])

            template_gid        = template.get("gid", template_gid)
            template_rotation   = template.get("rotation", template_rotation)

            # check in template properties if the value does exist or not
            if template.get("properties"):
                if not data.get("properties"): data["properties"] = {}
                for propertie in template["properties"]:
                    if data["properties"].get(propertie, -1) == -1:
                        data["properties"][propertie] = template["properties"][propertie]

            data.pop("template")
        else:
            width 	= data["width"]
            height 	= data["height"]
            object_name = data.get("name", "")
            objecttype	= data.get("type")

        
        data["name"] = object_name
        data["width"] = width
        data["height"] = height
        data["z"] = self.object_idorder
        data["type"] = objecttype

        data["gid"]        = data.get("gid", template_gid)
        data["rotation"]   = data.get("rotation", template_rotation)

    
        
        if not self.objectnames.get(object_name): self.objectnames[object_name] = []
        self.objectnames[object_name].append(object_id)

        if not self.objecttypes.get(objecttype): self.objecttypes[objecttype] = []
        self.objecttypes[objecttype].append(object_id)

        y -= chunk_height
        chunk_x = int(x /	chunk_width	)
        chunk_y = int(y /	chunk_height)

        width_lenght 	= max(int((x+width)/chunk_width)-chunk_x, 1)
        height_lenght 	= max(int((y+height)/chunk_height)-chunk_y, 1)

        data["chunks"] = []

        for chunk_offset_x in range(width_lenght):
            for chunk_offset_y in range(height_lenght):
                chunk_coord = f"{int(chunk_x+chunk_offset_x)},{int(chunk_y+chunk_offset_y)}"

                if not self.object_chunks.get(chunk_coord): self.object_chunks[chunk_coord] = []
                self.object_chunks[chunk_coord].append(object_id)
                data["chunks"].append(chunk_coord)
        
        #print(data["chunks"], (width, height), (chunk_width, chunk_height) , object_id)
        if not self.objectlayers.get(data["layerid"]): self.objectlayers[data["layerid"]] = []
        self.objectlayers[data["layerid"]].append(object_id)
        self.objects[object_id] = data

    def remove_object(self, object_id:int):
        if object_id < 0 or (not self.objects.get(object_id)): return 

        object_data = dict(self.objects[object_id])

        for chunk_coord in object_data["chunks"]:
            self.object_chunks[chunk_coord].remove(object_id)
            if len(self.object_chunks[chunk_coord]) == 0: self.object_chunks.pop(chunk_coord)

        self.objects.pop(object_id)
        self.objectlayers[object_data["layerid"]].remove(object_id)
        if len(self.objectlayers[object_data["layerid"]]) == 0: self.objectlayers.pop(object_data["layerid"])

    def refresh_object(self, object_data:dict):
        object_id = object_data["id"]
        chunk_width, chunk_height = self.chunk_size

        if object_id < 0: return

        for chunk_coord in object_data["chunks"]:
            self.object_chunks[chunk_coord].remove(object_id)

        x, y, width, height = object_data["x"], object_data["y"], object_data["width"], object_data["height"]

        y -= chunk_height
        chunk_x = int(x /	chunk_width	)
        chunk_y = int(y /	chunk_height)

        width_lenght 	= max(int((x+width)/chunk_width)-chunk_x, 1)
        height_lenght 	= max(int((y+height)/chunk_height)-chunk_y, 1)

        object_data["chunks"] = []

        for chunk_offset_x in range(width_lenght):
            for chunk_offset_y in range(height_lenght):
                chunk_coord = f"{int(chunk_x+chunk_offset_x)},{int(chunk_y+chunk_offset_y)}"

                if not self.object_chunks.get(chunk_coord): self.object_chunks[chunk_coord] = []
                self.object_chunks[chunk_coord].append(object_id)
                object_data["chunks"].append(chunk_coord)

        self.objects[object_id] = object_data
        
    def get_objects_by_name(self, name:str) -> list:
        return self.objectnames.get(name, [])

    def get_objects_by_type(self, type:str) -> list:
        return self.objecttypes.get(type, [])
    
    def load_json_map(self, pathmap:str, debug=False):
        with open(pathmap) as mapfile: 
            mapdata = json.load(mapfile)
            mapfile.close()
        
        if not bool(mapdata["infinite"]):
            raise NotImplementedError(
                f"[{self.__class__.__name__}] Your mapfile: \n   => ({pathmap})\n"+
                f"Isn't setup as infinite."
            )

        if mapdata.get("type") != "map":
            raise TypeError(
                f"[{self.__class__.__name__}] Your mapfile: \n   => ({pathmap})\n"+
                f"Isn't a map"
            )

        self.data = TiledDataMap(mapdata)

        # [Tilesets]
        for raw_tileset in mapdata["tilesets"]:
            tileset = TiledDataTileset(raw_tileset, path_map=pathmap)
            self.tilesets[tileset.path] = tileset

            is_collision = (tileset.classtype.lower() == TILESETS_COLLISIONCLASS)

            if tileset.is_base_on_tilesets:
                #[Base on Tilesets]
                image = pygame.image.load(tileset.image_source)
                image_width = tileset.image_width
                image_height = tileset.image_height

                # check if the information are correct
                if (image_width == image.width) and (image_height == image.height):
                    tilecount = tileset.tilecount

                    x_size = (image_width - 2 * tileset.margin + tileset.spacing) // (tileset.tilewidth + tileset.spacing)
                    y_size = (image_height - 2 * tileset.margin + tileset.spacing) // (tileset.tileheight + tileset.spacing)

                    for y in range(0, y_size):
                        for x in range(0, x_size):
                            count = (y*x_size)+x
                            if count >= tilecount: break

                            tiledata:dict = tileset.tiles.get(count, {})
                            left = tileset.margin + x * (tileset.tilewidth + tileset.spacing)
                            top = tileset.margin + y * (tileset.tileheight + tileset.spacing)
                            try: new_base_tile = image.subsurface(left, top, tileset.tilewidth, tileset.tileheight)
                            except: new_base_tile = pygame.Surface((tileset.tilewidth, tileset.tileheight)).convert(8)

                            for i in range(8):
                                # math
                                is_rotated = int(i >= 4)
                                flipX, flipY = [(0, 0), (0, 1), (1, 1), (1, 0)][i%4]
                                index = (tileset.firstgid + count) + (flipX * 0x80000000) + (flipY * 0x40000000) + (is_rotated * 0x20000000)
                                
                                # surface
                                new_tile = pygame.transform.flip(pygame.transform.rotate(new_base_tile, 90*is_rotated), flipX, (flipY+is_rotated)%2)
                                self.tiles[index] = pygame.surfarray.array2d(new_tile)

                                # [Collision] This is the collision side
                                if is_collision:
                                    ground_angle:str = tiledata.get("type", "")
                                    if is_float(ground_angle):
                                        ground_angle = float(ground_angle)

                                        # check required cuz of how the rotation work
                                        if ground_angle > 90: 
                                            raise AssertionError(
                                                f"[{tileset.__class__.__name__}] "+
                                                f"Tile n°{count} from ({tileset.path}) cannot be supported because it is more than 90°."
                                            )
                                        # rotation
                                        if (is_rotated): ground_angle = -(ground_angle-((int(ground_angle/90)+1) *90))


                                        # flip [1 => V, 2 => VH, 3 => H]
                                        
                                        if i%4 == 1: 	ground_angle = 90 + (90 - ground_angle)
                                        elif i%4 == 2: 	ground_angle = (90 + (90 - (360- ground_angle)))
                                        elif i%4 == 3: 	ground_angle = 360 - ground_angle
                                        

                                        self.ground_angles[index]  = (ground_angle)%360
                                        #print(index, self.ground_angles[index], is_rotated, i%4, [(0, 0), (0, 1), (1, 1), (1, 0)][i%4])

                                    elif ground_angle in ["Y", "X"]:
                                        self.ground_angles[index]  = ground_angle
                                    
            else:
                # [Collection]
                for tileid in tileset.tiles:
                    imagedata = tileset.tiles[tileid]
                    new_base_tile = pygame.image.load(imagedata["image"]).convert(8)
                    
                    for i in range(8):
                        # math
                        is_rotated = int(i >= 4)
                        flipX, flipY = [(0, 0), (0, 1), (1, 1), (1, 0)][i%4]
                        index = (tileset.firstgid + tileid) + (flipX * 0x80000000) + (flipY * 0x40000000) + (is_rotated * 0x20000000)
                        # surface
                        new_tile = pygame.transform.flip(pygame.transform.rotate(new_base_tile, 90*is_rotated), flipX, (flipY+is_rotated)%2)
                        self.tiles[index] = pygame.surfarray.array2d(new_tile)


        # [Layers]
        for layer in mapdata["layers"]:

            new_layer = self.new_layer(layer)
            
            # [TilesLayers]
            if layer["type"] == LAYERTYPE_TILELAYER:
                for chunk in layer["chunks"]:
                    data = chunk["data"]
                    if self.data.chunk_width == -1:     self.data.chunk_width = chunk["width"]
                    if self.data.chunk_height == -1:    self.data.chunk_height = chunk["height"]

                    # decoder
                    if new_layer.encoding == "base64":
                        data = b64decode(data)
                        if new_layer.compression == "gzip":
                            data = gzip.decompress(data)

                        elif new_layer.compression == "zlib":
                            data = zlib.decompress(data)

                        elif new_layer.compression == "zstd":
                            decompressor = zstd.ZstdDecompressor()
                            data = decompressor.decompress(data)

                        elif new_layer.compression:
                            raise TypeError(
                                f"[{self.__class__.__name__}] Your mapfile: \n   => ({pathmap})\n"+
                                f"Contain the layer compression {new_layer.compression} which is not supported."
                            )
                        
                        data = list(struct.unpack(("<%dL" % (len(data) // 4)), data))
                    # save
                    self.set_chunk(numpy.array(data, dtype=numpy.uint32).reshape((self.data.chunk_width, self.data.chunk_height)), chunk["x"], chunk["y"], new_layer.id)

            elif layer["type"] == LAYERTYPE_OBJECTGROUP: 
                for object in layer["objects"]:
                    object_data = object

                    template = object_data.get("template")
                    object_data["layerid"] = new_layer.id
                    if object.get("properties"): object["properties"] = extract_properties(object["properties"])

                    if template:
                        object_data["template"] = resoled_path = resolve_relative_path(pathmap, template)
                        template_extension = get_extension(template)

                        if not self.templates.get(resoled_path): # skip when template has already been founded
                            if template_extension in ["xml", "tx"]:
                                template_data = load_xml_template(resoled_path)
                                if template_data["object"].get("properties"): 
                                    template_data["object"]["properties"] = extract_properties(template_data["object"]["properties"])


                            elif template_extension in ["json", "tj"]:
                                with open(resoled_path) as mapfile: 
                                    template_data = json.load(mapfile)
                                    mapfile.close()
                            else:
                                raise NotImplementedError(
                                    f"[{self.__class__.__name__}] Can't load your template file: \n   => ({pathmap})\n"+
                                    f"Please use other type of file type such as '.TJ' or '.JSON', instead of '.{(template_extension.upper())}'. "
                                )
                            if template_data["object"].get("gid"):
                                tileset_path = resolve_relative_path(resoled_path, template_data["tileset"]["source"])
                                template_data["object"]["gid"] += self.tilesets[tileset_path].firstgid -1

                            self.templates[resoled_path] = template_data
                    self.add_object(object_data)
                
                
            # add layer to the list
            self.add_layer(new_layer)
        if debug: print(self.tilelayers_datachunks)

    # [Tools: Tilelayer]
    def set_view(self, x, y, width, height):

        # define the view (aka the screen coordinate)
        self.view_rect = pygame.Rect(x, y, width, height)

        self.offscreen_rect = pygame.Rect(
            -self.offscreen_spawn.x, 
            -self.offscreen_spawn.y, 
            width  + (self.offscreen_spawn.x*2) -1,
            height + (self.offscreen_spawn.y*2) -1
        )
            
        
        # define  a position for each layer
        for layerid in self.layers:
            layer = self.layers[layerid]
            self.offeset_views[layer.id] = vec2(
                (int(x)*layer.parallaxx) - layer.offsetx + ((width /2) * (layer.parallaxx-1)) , 
                (int(y)*layer.parallaxy) - layer.offsety + ((height/2) * (layer.parallaxy-1))
                )

    def add_tilelayer_2Darray(self, tilelayer_id, width, height):
        width = width*self.data.tilewidth
        height = height*self.data.tileheight
        self.tilelayers_array[tilelayer_id] = numpy.zeros((width*height), dtype=numpy.uint8).reshape(width, height)
        return width, height

    def add_tilelayer_2Darray_by_name(self, tilelayer_name, width, height):
        for tilelayer_id in self.layers:
            if self.layers[tilelayer_id].name == tilelayer_name : 
                # use to stop the entire function
                return self.add_tilelayer_2Darray(tilelayer_id, width, height)
        return 0, 0
    
    def load_visible_tilelayers_2Darray(self, width, height):
        size_array = 0, 0
        for tilelayer_id in self.layers:
            if self.layers[tilelayer_id].visible: size_array = self.add_tilelayer_2Darray(tilelayer_id, width, height)
        return size_array
    def get_chunk_datamask(self, x, y, radius:int, tilelayer_id:int):
        # setup vars
        tilewidth, tileheight = self.data.tilewidth, self.data.tileheight
        x, y, radius = int(x), int(y), int(radius)
        

        Collision = numpy.zeros(radius*radius*tilewidth*tileheight*2*2).reshape(radius*tilewidth*2, radius*tileheight*2)

        for i in range(radius*2):
            for j in range(radius*2):
                tile_id = self.get_tile(int((x - x%tilewidth)/tilewidth) + (i-radius), int((y - y%tileheight)/tileheight) + (j-radius), tilelayer_id)
                if tile_id != 0:
                    Collision[(i*tilewidth): ((i+1)*tilewidth), (j*tileheight): ((j+1)*tileheight)] = self.tiles[tile_id]
    
        return  surface_to_dmask(
            convert_surfarray_to_surface(Collision),
                (
                    (x-(radius*tilewidth))- (x%tilewidth), 
                    (y-(radius*tileheight))-(y%tileheight)
                )
            )

    def get_collision_angle(self, x, y, tilelayer_id:int):
        tilewidth, tileheight = self.data.tilewidth, self.data.tileheight
        x, y = int(x), int(y)
        tile_id = self.get_tile(int((x - (x%tilewidth))/tilewidth), int((y - (y%tileheight))/tileheight), tilelayer_id)
        return self.ground_angles.get(tile_id, "N") , vec2(int((x - x%tilewidth)), int((y - y%tileheight)))

    def refresh_tile(self, x, y):
        # setup vars
        tilewidth = self.data.tilewidth
        tileheight = self.data.tileheight


        # main focus
        for tilelayer_id in self.tilelayers_array:
            sarray:numpy.ndarray = self.tilelayers_array[tilelayer_id]
            offeset_view:vec2 = self.offeset_views[tilelayer_id]

            x1 = int((offeset_view.x/tilewidth)  + x-1)
            y1 = int((offeset_view.y/tileheight) + y-1)

            w, h = sarray.shape
            sarray_width = int(w/tilewidth)
            sarray_height = int(h/tileheight)

            x2 = x1%sarray_width 
            y2 = y1%sarray_height

            tile_index = self.get_tile(x, y, tilelayer_id)
            if tile_index > 0: sarray[(x2*tilewidth):((x2+1)*tilewidth), (y2*tileheight):((y2+1)*tileheight)] = self.tiles[tile_index]
            else: sarray[(x2*tilewidth):((x2+1)*tilewidth), (y2*tileheight):((y2+1)*tileheight)] = numpy.zeros((tilewidth*tileheight)).reshape((tilewidth, tileheight))
    
    def refresh_all_tiles(self):
        # setup vars
        tilewidth = self.data.tilewidth
        tileheight = self.data.tileheight

        # main focus
        for tilelayer_id in self.tilelayers_array:
            sarray:numpy.ndarray = self.tilelayers_array[tilelayer_id]
            offeset_view:vec2 = self.offeset_views[tilelayer_id]

            # get general variables 
            w, h = sarray.shape
            sarray_width = int(w/tilewidth)
            sarray_height = int(h/tileheight)

            for i in range(0, sarray_width):     
                for j in range(0, sarray_height):

                    x = int((offeset_view.x/tilewidth)  + i-1)
                    y = int((offeset_view.y/tileheight) + j-1)

                    x2 = x%sarray_width 
                    y2 = y%sarray_height

                    tile_index = self.get_tile(x, y, tilelayer_id)
                    if tile_index > 0: sarray[(x2*tilewidth):((x2+1)*tilewidth), (y2*tileheight):((y2+1)*tileheight)] = self.tiles[tile_index]
                    else: sarray[(x2*tilewidth):((x2+1)*tilewidth), (y2*tileheight):((y2+1)*tileheight)] = numpy.zeros((tilewidth*tileheight)).reshape((tilewidth, tileheight))
                    
    def render_tilelayer(self, tilelayer_id, position= vec2(0), special_flags:int=0):
        # get data part
        tilelayer_array = self.tilelayers_array.get(tilelayer_id)
        offeset_view:vec2 = self.offeset_views[tilelayer_id]

        # rendering part
        if not tilelayer_array is None:
            tilelayer_array = numpy.roll(tilelayer_array, [-int(offeset_view.x), -int(offeset_view.y)], axis=[0, 1])
            surfarray_blit(tilelayer_array, position, special_flags=special_flags)

    def prerender_tilelayer(self, tilelayer_id, position = vec2(0), special_flags:int=0):
        # get data part
        tilelayer_array = self.tilelayers_array.get(tilelayer_id)
        offeset_view:vec2 = self.offeset_views[tilelayer_id]
        
        if tilelayer_array is None: return 0

        # rendering part
        tilelayer_array = numpy.roll(tilelayer_array, [-int(offeset_view.x), -int(offeset_view.y)], axis=[0, 1])
        prerender(tilelayer_array, position, special_flags=special_flags)
        return 1
        
    
    # [Tools: Object]
    def add_objectclass(self, objectclass:TiledDataLayer):
        # this method simplify so much things
        self.objectclass_dict[objectclass.__name__] = objectclass
    
    def load_objects(self):

        # this static 2D loop isn't definitive
        current_layer_keys = list(self.layers.keys())
        for chunk_x in range(-2, 7):
            for chunk_y in range(-2, 7):
                
                for layerid in current_layer_keys:
                    # check if layer is an object group
                    if self.layers[layerid].type == "objectgroup":
                        offset = self.offeset_views[layerid]
                        x = chunk_x + int(offset.x // self.chunk_size.x)
                        y = chunk_y + int(offset.y // self.chunk_size.y)

                        # check if chunk does exists for this specific layer
                        chunk_ids = self.object_chunks.get(f"{x},{y}")
                        if chunk_ids:
                            
                            for id in chunk_ids: # load a list of data
                                object_data = self.objects.get(id)
                                if object_data and (not self.pool.objects.get(id)):

                                    # Conditions 
                                    check_layer_id =  object_data["layerid"] == layerid
                                    has_collide = self.offscreen_rect.colliderect(pygame.Rect(
                                                            object_data["x"]-offset.x, 
                                                            object_data["y"]-offset.y + (-object_data["height"] * (object_data["gid"] > 0)), 
                                                            object_data["width"], 
                                                            object_data["height"]
                                                        ))
                                    if has_collide and check_layer_id:
                                        objectclass = self.objectclass_dict.get(object_data["type"])
                                        if not objectclass is None: 
                                                objectclass(id)
                                        else:
                                            # object doesn't exist check the placeholder
                                            objectclass = self.objectclass_dict.get("Placeholder")
                                            if not objectclass is None: 
                                                objectclass(id)
                                            else:
                                                raise NotImplementedError(
                                                    f"[{self.__class__.__name__}] The Placeholder does not exist :\n"+
                                                    f"Please create a universal object for placeholder. "
                                                )

                                