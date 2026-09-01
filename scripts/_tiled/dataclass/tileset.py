from dataclasses import dataclass, field
from retropy import *
from .utils import *

#------------------------------------------------------------------------------------
#   Author: PlusVeter
#------------------------------------------------------------------------------------


@dataclass
class TiledDataTileset:
	name            :str
	classtype  		:str
	source          :str
	path            :str

	firstgid        :int
	tilewidth       :int
	tileheight      :int
	spacing         :int
	margin          :int
	tilecount       :int

	image_source    :str
	image_height    :int
	image_width     :int

	tiles           :list

	is_base_on_tilesets     :bool

	def __init__(self, data:dict, path_map, debug=False):
		self.is_base_on_tilesets = False
		self.tiles = {}

		self.source = data.get("source")
		self.firstgid = data["firstgid"]

		if self.source:
			extensionfile = get_extension(self.source).lower()
			if debug: print(path_map, self.source, resolve_relative_path(path_map, self.source))
			self.path = source_path = resolve_relative_path(path_map, self.source)
			
			if extensionfile in ["xml", "tsx"]:   
				self.load_xml_tileset(source_path)

			elif extensionfile in ["json", "tsj"]: 
				self.load_json_tileset(source_path)
			else:
				raise NotImplementedError(
					f"[{self.__class__.__name__}] Can't load your tileset file: \n   => ({source_path})\n"+
					f"Please use other type of file type such as '.TSJ', '.JSON, '.XML', '.TSX'\n"+
					f"Instead of '.{(extensionfile.upper())}'. "
				)
		else:
			self.path = path_map
			self.read_json_tileset(data)
			
		if self.is_base_on_collections:
			self.image_source    = ""
			self.image_height    = 0
			self.image_width     = 0

	@property
	def is_base_on_collections(self):
		return not self.is_base_on_tilesets
	
	@is_base_on_collections.setter
	def is_base_on_collections(self, args): ...
		
	def load_xml_tileset(self, path_tileset):
		with open(path_tileset, "rb") as tilesetsfile:
			self.read_xml_tileset(xmlET.parse(tilesetsfile))
			tilesetsfile.close()
	

	def read_xml_tileset(self, tilesets_tree:xmlET):
		root = tilesets_tree.getroot()
		# [variables]
		self.name       = root.attrib["name"]
		self.classtype 	= root.attrib.get("class", "")
		self.tilewidth  = int(root.attrib["tilewidth"])
		self.tileheight = int(root.attrib["tileheight"])
		self.spacing    = int(root.attrib.get("spacing", 0))
		self.margin     = int(root.attrib.get("margin", 0))
		self.tilecount  = int(root.attrib["tilecount"])


		image_data = root.find("image")
		if not image_data is  None:
			self.is_base_on_tilesets = True
			self.image_source    = resolve_relative_path(self.path, image_data.attrib["source"])
			self.image_height    = int(image_data.attrib["height"])
			self.image_width     = int(image_data.attrib["width"])

		
		for tile in root.findall("tile"):
			tile_id = int(tile.attrib["id"])
			tile_type = tile.attrib.get("type")

			self.tiles[tile_id] = {}
			if tile_type: self.tiles[tile_id]["type"] = tile_type
			if self.is_base_on_collections:
				image = tile.find("image")
				if not image is None:
					source = image.attrib.get("source")
					width = int(image.attrib.get("width"))
					height = int(image.attrib.get("height"))

					if source: self.tiles[tile_id]["image"] = resolve_relative_path(self.path, source)
					if width: self.tiles[tile_id]["imageheight"] = width
					if height: self.tiles[tile_id]["imagewidth"] = height

	
	def load_json_tileset(self, path_tileset):
		with open(path_tileset) as tilesetsfile: 
			self.read_json_tileset(json.load(tilesetsfile))
			tilesetsfile.close()
		
	def read_json_tileset(self, tilesetsdata:dict):
		self.name       = tilesetsdata["name"]
		self.classtype 	= tilesetsdata.get("class", "")
		self.tilewidth  = tilesetsdata["tilewidth"]
		self.tileheight = tilesetsdata["tileheight"]
		self.spacing    = tilesetsdata.get("spacing", 0)
		self.margin     = tilesetsdata.get("margin", 0)
		self.tilecount  = tilesetsdata["tilecount"]


		image_data = tilesetsdata.get("image")
		if image_data:
			self.is_base_on_tilesets = True
			self.image_source    = resolve_relative_path(self.path, image_data)
			self.image_height    = tilesetsdata["imageheight"]
			self.image_width     = tilesetsdata["imagewidth"]


		tiles_data = tilesetsdata.get("tiles")
		if tiles_data:
			for tiledata in tiles_data:
				tile_id = tiledata["id"]
				tile_type = tiledata.get("type")

				self.tiles[tile_id] = {}
				if tile_type: self.tiles[tile_id]["type"] = tile_type
				if self.is_base_on_collections:
					image = tiledata.get("image")
					image_height = tiledata.get("imageheight")
					image_width = tiledata.get("imagewidth")

					if image: self.tiles[tile_id]["image"] = resolve_relative_path(self.path, image)
					if image_height: self.tiles[tile_id]["imageheight"] = image_height
					if image_width: self.tiles[tile_id]["imagewidth"] = image_width