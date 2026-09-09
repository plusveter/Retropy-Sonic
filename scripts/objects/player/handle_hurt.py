from retropi import *
from .base import PlayerBase
from .macros import *

from ..objects_list.items.ring_loss import create_ringloss
from ..hud import HUD as HUD_
from ..camera import Camera
from ..macro import *


def player_handle_hurt(self:PlayerBase):
	HUD:HUD_ = self.parent.HUD
	camera:Camera = self.parent.camera
	if(self.state != ST_KNOCKOUT):
		if(self.invincible_timer == 0 and not self.invincible):
			if(self.knockout_type == K_HURT):
				# Kill the player if there are no any rings or shields
				if(HUD.rings == 0 and self.shield == S_NONE):
					self.knockout_type = K_DIE
				
				# Hurt the player if they have any rings or shields
				if(HUD.rings != 0 or self.shield != S_NONE):
					# Get the hurt side
					side = 1
					if(sign(self.position[0] - self.hurt_position) != 0):
						side = int(sign(self.position[0] - self.hurt_position))

					# Knockout the player
					self.speed[0] = 2 * side
					self.speed[1] = -4
					self.facing = -side
					self.ground = False
					self.position[1] += -5
					self.deconnect_withOBJ()
					
					# Underwater cases
					if(self.is_underwater):
						self.speed[0] *= 0.5
						self.speed[1] /= 2
					
					# Give player invincibility frames and put the player in knockout self.state
					self.invincible_timer = 120
					self.state = ST_KNOCKOUT
					
					# Commit ring loss when player gets hurt
					if(self.shield == S_NONE):
						create_ringloss(self, HUD.rings, self.position[0], self.position[1])
						self.play_sound(self.SFX_RingSpill)
						HUD.rings = 0
					
					# Remove the self.shield when player gets hurt
					if(self.shield != S_NONE):
						self.shield = S_NONE
						self.play_sound(self.SFX_Hurt)
					
	
	# Fix so player can die at any time
	# self.has_died = False
	
	# Reset the flag
	if(self.state != ST_KNOCKOUT):
		self.has_died = False
	
	# Player's death event
	if(self.knockout_type == K_DIE and not self.has_died):
		# Set the die flag
		self.has_died = True

		# Set player to the knockout self.state
		self.state = ST_KNOCKOUT
			
		# Bounce the player out
		self.speed[1] = -7
		self.speed[0] = 0
		self.ground = False
		self.deconnect_withOBJ()
			
		# Disable camera movement
		camera.mode = CAM_NULL
			
		# Play the hurt sound
		self.play_sound(self.SFX_Hurt)
		
	# Kill the player after time has reached the limit
	#if(HUD.timer == 599999):
	#	self.knockout_type = K_DIE
	#	is_time_over = True
	
	if(self.state != ST_KNOCKOUT):
		self.knockout_type = 0
			
	# Bottomless pit death event
	#if(self.position[1] > obj_camera.target_bottom and self.position[1] > obj_camera.limit_bottom and self.knockout_type != K_DIE):
	#	self.knockout_type = K_DIE