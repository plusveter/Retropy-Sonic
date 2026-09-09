from scripts.base import *
from .base import PlayerBase
from ..water.effect import WaterEffect
from .macros import *


def player_water(self:PlayerBase):
	# Stop executing if theres no water
	
	if(not general.water_visible or not self.collision_allow): return None
	
	# Entering water
	if(self.position[1] >= general.water_height):
		# Player hitting the water
		if(not self.is_underwater):
			# Slow down the player
			self.speed[0] *= 0.5
			self.speed[1] *= 0.25
			
			# Create effects
			effect = WaterEffect()
			effect.position = vec2(self.position[0], general.water_height-14)
			effect.layerid = self.layerid
			effect.animation = "Splash"
			
			# Play sound
			play_sound(self.SFX_WaterSplash, channel_name=DEFAULT_SOUNDFX_CHANNEL)
		
		# Trigger the flag
		self.is_underwater = True
		self.player_list[self.player_id].normalform_constant(self)
	
	# Exiting water
	else:
		# Player hitting the water
		if(self.is_underwater):
			# Speed up the player
			self.speed[1] *= 1.25
			
			# Create effects
			effect = WaterEffect()
			effect.position = vec2(self.position[0], general.water_height-14)
			effect.layerid = self.layerid
			effect.animation = "Splash"

			# play sound
			play_sound(self.SFX_WaterSplash, channel_name=DEFAULT_SOUNDFX_CHANNEL)
		
		# Trigger the flag
		self.is_underwater = False
		self.player_list[self.player_id].normalform_constant(self)
	
	mouth_pos = vec2(self.position[0], self.position[1]+2)
	
	# Aquaphobia
	if(self.is_underwater):
		# Add self.air timer
		self.air += 1
			
		# Play warning sound
		if(self.air == 6*60 or  self.air == 12*60 or  self.air == 18*60): play_sound(self.SFX_WaterWarning)
			
		# Uh oh drowning music
		# if(!audio_is_playing(j_drowning) and self.air == 20 * 60){
		# 	var jing = audio_play_sound(j_drowning, 0, false);
		# 	audio_sound_gain(jing, global.bgm_volume, 0);
		# }
		# 	
		if (self.air % 60) == 0 or (self.air % 60) == 40:
			effect = WaterEffect()
			effect.position = mouth_pos
			effect.layerid = self.layerid
			effect.animation = "Small Bubble"
			
	else: self.air = 0
	
	if(self.air < 20*60): "audio_stop_sound(j_drowning);"
	
	# Drown!
	if(self.air > 32*60 and self.knockout_type != K_DROWN):
		play_sound(self.SFX_Drown)
		camera.mode = CAM_NULL
		self.state = ST_KNOCKOUT
		self.knockout_type = K_DROWN

	# Create the countdown
	if   self.air == (20*60):
			effect = WaterEffect()
			effect.position = mouth_pos
			effect.layerid = self.layerid
			effect.target_player = self
			effect.animation = "Countdown 5"

			play_sound(self.SFX_DrownAlert)
				
	elif self.air == (22*60):
			effect = WaterEffect()
			effect.position = mouth_pos
			effect.layerid = self.layerid
			effect.target_player = self
			effect.animation = "Countdown 4"

			play_sound(self.SFX_DrownAlert)
				
	elif self.air == (24*60):
			effect = WaterEffect()
			effect.position = mouth_pos
			effect.layerid = self.layerid
			effect.target_player = self
			effect.animation = "Countdown 3"

			play_sound(self.SFX_DrownAlert)
				
	elif self.air == (26*60):
			effect = WaterEffect()
			effect.position = mouth_pos
			effect.layerid = self.layerid
			effect.target_player = self
			effect.animation = "Countdown 2"

			play_sound(self.SFX_DrownAlert)
				
	elif self.air == (28*60):
			effect = WaterEffect()
			effect.position = mouth_pos
			effect.layerid = self.layerid
			effect.target_player = self
			effect.animation = "Countdown 1"
	
			play_sound(self.SFX_DrownAlert)
				
	elif self.air == (30*60):
			effect = WaterEffect()
			effect.position = mouth_pos
			effect.layerid = self.layerid
			effect.target_player = self
			effect.animation = "Countdown 5"
			
			play_sound(self.SFX_DrownAlert)	
