from scripts.base import *
from .base import PlayerBase
from .macros import *

# from ..objects_list.items.ring_loss import create_ringloss


def player_handle_hurt(self:PlayerBase):
	if(self.state != ST_KNOCKOUT):
		if(self.invincible_timer == 0 and not self.invincible):
			if(self.knockout_type == K_HURT):
				# Kill the player if there are no any rings or shields
				if(general.rings == 0 and self.shield == S_NONE):
					self.knockout_type = K_DIE
				
				# Hurt the player if they have any rings or shields
				if(general.rings != 0 or self.shield != S_NONE):
					# Get the hurt side
					side = 1
					if(sign(self.position.x - self.hurt_position.x) != 0):
						side = int(sign(self.position.x - self.hurt_position.x))

					# Knockout the player
					self.speed.x = 2 * side
					self.speed.y = -4
					self.facing = -side
					self.ground = False
					self.position.y += -5
					self.deconnect_withOBJ()
					
					# Underwater cases
					if(self.is_underwater):
						self.speed.x *= 0.5
						self.speed.y /= 2
					
					# Give player invincibility frames and put the player in knockout self.state
					self.invincible_timer = 120
					self.state = ST_KNOCKOUT
					
					# Commit ring loss when player gets hurt
					if(self.shield == S_NONE):
						# create_ringloss(self, general.rings, self.position.x, self.position.y)
						play_sound(self.SFX_RingSpill)
						general.rings = 0
					
					# Remove the self.shield when player gets hurt
					if(self.shield != S_NONE):
						self.shield = S_NONE
						play_sound(self.SFX_Hurt)
					
	
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
		self.speed.y = -7
		self.speed.x = 0
		self.ground = False
		self.deconnect_withOBJ()
			
		# Disable camera movement
		camera.mode = CAM_NULL
			
		# Play the hurt sound
		play_sound(self.SFX_Hurt)
		
	# Kill the player after time has reached the limit
	#if(HUD.timer == 599999):
	#	self.knockout_type = K_DIE
	#	is_time_over = True
	
	if(self.state != ST_KNOCKOUT):
		self.knockout_type = 0
			
	# Bottomless pit death event
	#if(self.position.y > obj_camera.target_bottom and self.position.y > obj_camera.limit_bottom and self.knockout_type != K_DIE):
	#	self.knockout_type = K_DIE