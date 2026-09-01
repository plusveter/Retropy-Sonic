from dataclasses import dataclass, field
from retropy import *
from .utils import *

#------------------------------------------------------------------------------------
#   Author: PlusVeter
#------------------------------------------------------------------------------------


@dataclass
class TiledDataLayer:
	id          :int
	name        :str  
	visible     :bool  
	classname	:str
	type 		:str

	datatype	:str
	compression :str
	encoding    :str  
	width       :int
	height      :int
	opacity     :int  
	
	
	x           :int
	y           :int

	parallaxx 	:int
	parallaxy	:int

	offsetx		:int
	offsety		:int

	mode		:int
	draworder 	:str

	properties 	:dict

	def __init__(self, data:dict):
		self.name          	= data.get("name", "")
		self.id            	= data.get("id", -1)

		self.classname		= data.get("class", "")
		self.compression   	= data.get("compression", "")
		self.encoding      	= data.get("encoding", "")
		
		self.width         	= data.get("width"	, -1)
		self.height        	= data.get("height"	, -1)
		self.opacity       	= data.get("opacity", 1)
		self.visible       	= data.get("visible", True)

		self.x             	= data.get("x", 0)
		self.y             	= data.get("y", 0)

		self.type		  	= data.get("type", "")
		self.datatype		= data.get("class", "")

		self.parallaxx		= data.get("parallaxx", 1.0)
		self.parallaxy		= data.get("parallaxy", 1.0)

		self.offsetx		= data.get("offsetx", 0.0)
		self.offsety		= data.get("offsety", 0.0)

		self.draworder 		= data.get("draworder", "") 

		self.properties		= extract_properties(data.get("properties", {}))


		# convert str to idblend
		blendmode = data.get("mode")
		if blendmode == "add": blendmode = pygame.BLEND_ADD
		elif blendmode == "multiply": blendmode = pygame.BLEND_MULT
		else: blendmode = 0

		
		self.mode = blendmode