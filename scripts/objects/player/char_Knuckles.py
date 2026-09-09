from scripts.base import *
from .character import Character


class Knuckles(Character):
	# Start

	def load(self):
		#self.palettes[self.player_num] = load_from_palfile(PALETTESFOLDER+"Characters/"+"Knuckles.pal")[16:31]
		self.sprites_cache[self.player_num] = Character.Spritesload(SPRITESFOLDER+"Players/Knuckles.bin")
		self.player_num += 1
	
	def load_Forms(self):
		Knuckles.normalform_constant(self)
		if self.form == "Normal":
			
			self.sprites = self.sprites_cache[self.player_id][0]
		else:
			self.sprites = self.sprites_cache[self.player_id][0]

	
	def normalform_constant(self):
		conv = 1.25
		Knuckles.update_constant(
			self,
			{
			"roll_friction_speed": 0.0234375,
			"roll_deceleration_speed": 0.125,

			"acc": 0.049875,
			"dec": 0.3,
			"frc": 0.046875,
			"top": 7,
			"slp": 0.125,
			"slprollup": 0.078125,
			"slprolldown": 0.3125,
			"fall": 2.5,
			"air": 0.09375,
			"jmp": 6,
			"grv": 0.21875,
			"limit": 16,
			"air_acc": 0.09375,

			"spindash_up": 2,
			"spindash_limit": 9
		}, 
		SuperForm=(self.form != "Normal"), 
		Underwater=self.is_underwater)
