from dataclasses import dataclass, field
from retropy import *
from .utils import *

#------------------------------------------------------------------------------------
#   Author: PlusVeter
#------------------------------------------------------------------------------------


@dataclass
class TiledDataMap:
	tiledversion:str

	# idk size
	width:int
	height:int

	#tilesize
	tilewidth:int
	tileheight:int

	compressionlevel:int
	orientation:str
	renderorder:str

	nextobjectid:int

	chunk_width:int
	chunk_height:int

	backgroundcolor:list
	properties 	:dict

	@property
	def tilesize(self): return vec2(self.tilewidth, self.tileheight)

	def __init__(self, data:dict):
		self.tiledversion 		= data["tiledversion"]


		# idk size
		self.width 				= data["width"]
		self.height 			= data["height"]

		#tilesize
		self.tilewidth 			= data["tilewidth"]
		self.tileheight 		= data["tileheight"]

		self.compressionlevel 	= data["compressionlevel"]
		self.orientation 		= data["orientation"]
		self.renderorder 		= data["renderorder"]

		self.nextobjectid 		= data["nextobjectid"]

		self.chunk_width 		= -1
		self.chunk_height		= -1

		self.backgroundcolor 	= data.get("backgroundcolor")
		self.properties		= extract_properties(data.get("properties", {}))
		
		# Background color
		bgcolor = 200/255
		if self.backgroundcolor is None: self.backgroundcolor = [255*bgcolor, 255*bgcolor, 255*bgcolor]
		else: self.backgroundcolor = list(pygame.Color.from_hex(self.backgroundcolor))[:3]
