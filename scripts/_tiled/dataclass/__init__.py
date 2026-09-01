from .layer import TiledDataLayer
from .map import TiledDataMap
from .tileset import TiledDataTileset
#------------------------------------------------------------------------------------
#   Author: PlusVeter
#------------------------------------------------------------------------------------
from retropy import *
from .utils import *

def load_xml_template(path_template_file):
	with open(path_template_file, "rb") as tilesetsfile:
		template_tree = xmlET.parse(tilesetsfile)
		root = template_tree.getroot()

		# extract
		tileset = root.find("tileset")
		object = root.find("object")

		template = {
			"object": {
				"gid": int(object.get("gid", 0)),
				"height": float(object.get("height", 0)),
				"id": int(object.get("id", 0)),
				"name": object.get("name", ""),
				"opacity": float(object.get("opacity", 1)),
				"rotation": float(object.get("rotation", 0)),
				"type": object.get("type", ""),
				"visible": object.get("visible", "true").lower() == "true",
				"width": float(object.get("width", 0)),
				"properties": []
			},
			"tileset": {
				"firstgid": int(tileset.get("firstgid", 0)),
				"source": tileset.get("source", "")
			},
			"type": root.tag
		}

		properties = object.find("properties")
		if properties is not None:
			for propertie in properties.findall("property"):
				prop_type = propertie.get("type", "string")
				value = propertie.get("value", "")

				# Convert to Python types
				if prop_type == "bool":
					value = value.lower() == "true"
				elif prop_type == "int":
					value = int(value)
				elif prop_type == "float":
					value = float(value)

				template["object"]["properties"].append({
					"name": propertie.get("name"),
					"type": prop_type,
					"value": value
				})

		# end
		tilesetsfile.close()
	return template

