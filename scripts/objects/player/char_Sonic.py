from scripts.base import *
from .character import Character
from .base import PlayerBase


#SonicPalette[1][2] = [249, 255, 169]
#SonicPalette[1][1] = [239, 240, 0]
#SonicPalette[1][0] = [255, 208, 36]




class Sonic(Character):
	# Start

	def load(self:PlayerBase):
		#self.palettes[self.player_num] = load_from_palfile(PALETTESFOLDER+"Characters/"+"Sonic.pal")[16:31]
		self.sprites_cache[self.player_num] =  Character.Spritesload( SPRITESFOLDER+"Players/Sonic.bin", link_SuperForm=SPRITESFOLDER+"Players/SuperSonic.bin")
		self.player_num += 1

	def load_Forms(self:PlayerBase):
		Sonic.normalform_constant(self)
		
		if self.form == "Normal":
			self.sprites = self.sprites_cache[self.player_id][0]
		else:
			self.sprites = self.sprites_cache[self.player_id][1]	

	
	def normalform_constant(self:PlayerBase):
		Sonic.update_constant(
			self,
			{
			"roll_friction_speed": 0.0234375,
			"roll_deceleration_speed": 0.125,

			"acc": 0.046875,
			"dec": 0.5,
			"frc": 0.046875,
			"top": 6,
			"slp": 0.125,
			"slprollup": 0.078125,
			"slprolldown": 0.3125,
			"fall": 2.5,
			"air": 0.09375,
			"jmp": 6.5,
			"grv": 0.21875,
			"limit": 32,
			"air_acc": 0.09375,

			"spindash_up": 2,
			"spindash_limit": 9
		}, 
		SuperForm=(self.form != "Normal"), 
		Underwater=self.is_underwater)
