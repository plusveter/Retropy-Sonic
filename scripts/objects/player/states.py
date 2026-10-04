from scripts.base import *
from .base import PlayerBase
from .macros import *

# load Particles
from scripts.objects._global.particle import Particle


def player_state_peelout(self:PlayerBase):
	# ref : https://github.com/DarkD04/Harmony-Framework/blob/app/scripts/player_state_peelout/player_state_peelout.gml
	# If the peelout isn't allowed in-game it won't execute
	#if self.player_id != 0: return None

	# Trigger peel out
	if(self.state == ST_LOOKUP and self.press_action() and self.ground ): # and self.player_id == CHAR_SONIC
		play_sound(self.SFX_SpinCharge) # play_sound(sfx_peelout_charge);
		self.state = ST_PEELOUT
		self.spindashrev = 0
	
	# if its not peel out stop
	if(self.state != ST_PEELOUT): return None

	# //Create dust effect (No Presented)

	# Stop movement
	self.ground_speed = 0
	
	# Change flags
	self.direction_allow = 1 - self.ground
	self.movement_allow = 1 - self.ground
	
	# Add rev value and clamp it
	self.spindashrev += 1
	self.spindashrev = min(self.spindashrev, 300)

	
	# Change animations
	self.anim = ANIM_WALK
	if(self.spindashrev >= 15): self.anim = ANIM_RUN
	if(self.spindashrev == 30): self.anim = ANIM_MAXRUN
	
	
	# Release the peel out
	if(not self.hold_action()):
		# Stop the peelout charge audio
		self.SFX_SpinCharge.stop()
		
		# Play the release sound
		play_sound(self.SFX_PeelRelease) #play_sound(sfx_peelout_release)
		
		# Set player's speed and back to normal state

		self.ground_speed = (2+(self.spindashrev / 2.9)) * self.facing
		if(not self.ground):
			self.speed[0] = (2+(self.spindashrev / 2.9)) * self.facing
		self.state = ST_NORMAL;	

def player_state_dropdash(self:PlayerBase):
	# If global value for dropdash is diabled don't execute
	#if(!global.use_dropdash) exit;
	
	# Add dropdash timer
	if(self.player_id == CHAR_SONIC):
		if(self.press_action() and self.dropdash_timer < 1 and self.state == ST_JUMP or self.hold_action() and self.dropdash_timer != 0 and self.state == ST_JUMP):
			self.dropdash_timer += 1

	# Trigger the dropdash state
	if(self.dropdash_timer >= 8 and self.state != ST_DROPDASH):
		play_sound(self.SFX_DropDash)
		self.state = ST_DROPDASH
	
	# Reset the timer
	if(self.state != ST_JUMP or self.state == ST_DROPDASH or self.shield != S_NONE and self.shield != S_NORMAL):
		self.dropdash_timer = 0
	
	# If not dropdash stop
	if(self.state != ST_DROPDASH): return None
	
	# Animate dropdash
	self.anim = ANIM_DROPDASH
	
	# Make it attack
	self.attacking = True
	
	# Go back to jump when not holding the button
	if (not self.hold_action()):
		self.dropdash_timer = -1
		self.state = ST_JUMP
	
	# Land the dropdash
	if (not self.landed and self.ground):
		# Dropdash speeds
		dashspeed = 8.0
		maxspeed = 12.0
		
		if (self.facing == -1):
			if(self.speed[0] <= 0.0):
				self.ground_speed = max(-maxspeed, -dashspeed + (self.ground_speed / 4.0))
			elif (self.ground_speed != 0):
				self.ground_speed = -dashspeed + (self.ground_speed / 2.0)
			else:
				self.ground_speed = -dashspeed
		else:
			if (self.speed[0] >= 0.0):
				self.ground_speed = min(maxspeed, dashspeed + (self.ground_speed / 4.0))
			elif (self.ground_speed != 0):
				self.ground_speed = dashspeed + (self.ground_speed / 2.0)
			else:
				self.ground_speed = dashspeed
		
		# Roll state
		self.state = ST_ROLL; 
		play_sound(self.SFX_SpinRelease)
		
		# Camera lag
		#obj_camera.h_lag = 8;
		
		# Create effect
		# if(global.chaotix_dust_effect)
		# {
		# 	for (var i = 0; i < 8; ++i) 
		# 	{
		# 		 create_effect(x - hitbox_w * facing, y + hitbox_h, spr_dust_effect, 0.4, depth-1, (2.5 * facing) * dcos(random_range(180, 270)), 2.5 * dsin(random_range(180, 270)));
		# 	}
		# }
		# else
		# {
		# 	var o = create_effect(floor(x) - hitbox_w * facing, floor(y) + hitbox_h, spr_effects_dropdash_dust, 0.4, depth-1);
		# 	o.image_xscale = facing;
		# }
	
def player_state_normal(self:PlayerBase):
	#ref : https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_state_normal/player_state_normal.gml
	# Add the idle timer

	#bpm = self.app.music_bpm[self.app.get_currentmusic_id()]

	if(self.state == ST_NORMAL and self.ground_speed == 0 and not self.input_disable):
		
		self.idle_timer += 1
	else:
		self.idle_timer = 0
	
	
	# Stop executing if its not the specific state:
	if(self.state != ST_NORMAL): return None
	
	# Value for the animation
	self.anim = ANIM_STAND
	
	# Default animation:
	if (self.ground):
		self.anim = ANIM_STAND
	else:
		if self.anim != ANIM_BREATHE:
			self.anim = ANIM_WALK
	
	run_speed = 5
	# Walking animation:
	if(run_speed >= abs(self.ground_speed) > 0): 
		self.anim = ANIM_WALK
		self.animation_tracker.timer += (abs(self.ground_speed)) ** 3
	# Running animation:
	if(abs(self.ground_speed) >= run_speed): 
		self.anim = ANIM_RUN # Update the animation
		#print((abs(self.ground_speed)-7))
		self.animation_tracker.timer += (min(abs(self.ground_speed)-7, 30) ** 5)/10
			
		
	# Running animation:
	if(abs(self.ground_speed) >= 12): self.anim = ANIM_MAXRUN

	if (self.idle_timer > 160):
		self.anim = ANIM_WAIT



	# Ledge animation

	if self.ground and self.ground_speed == 0:
		if self.flailing == 1 or self.flailing == 5:
			self.anim = ANIM_LEDGE2
			self.facing = (((self.flailing > 3) *2) - 1)
			if self.player_id == CHAR_TAILS: self.facing *= -1

		elif self.flailing == 2 or self.flailing == 4:
			self.anim = ANIM_LEDGE1
			self.facing = (((self.flailing < 3) *2) - 1) 

			
	
		'''
		if(!line_check(0, hitbox_h + 16, true) && !check_object(0, 0, 1, hitbox_h + 8, true) and self.ground and self.ground_speed == 0):
			# Change animation
			if(!line_check(hitbox_w, hitbox_h + 16, true) && !check_object(-wall_w, 0, wall_w, hitbox_h + 8, true)):
				anim = facing = 1 ? ANIM.LEDGE2 : ANIM.LEDGE1;
			
			if(!line_check(-hitbox_w, hitbox_h + 16, true) && !check_object(wall_w, 0, -wall_w, hitbox_h + 8, true)):
				anim = facing = -1 ? ANIM.LEDGE2 : ANIM.LEDGE1;
		'''

	if (get_pressed(K_LEFT) or get_pressed(K_RIGHT)) and self.PUSH and self.ground:
		self.anim = ANIM_PUSH
		self.idle_timer = 0
		
	
def player_state_jump(self:PlayerBase):
	# https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_state_jump/player_state_jump.gml
	# List of states that allow for jumping
	can_jump_states = [ST_NORMAL, ST_ROLL, ST_SKID]
	
	jump_strength  = self.constants["jmp"]
	jump_release = 3
	grv         = self.constants["grv"]

	self.can_jump = (self.state in can_jump_states)


	# Trigger jump
	if self.press_action() and self.ground and not self.touching_ceiling and not self.force_roll and self.can_jump:
		# Change animation
		self.anim = ANIM_ROLL

		angle = self.ground_angle %360

		# Jump off the terrain
		self.speed[0] -= jump_strength * math.sin(math.radians(angle))
		self.speed[1] -= jump_strength * math.cos(math.radians(angle))

		# Trigger the jump flag
		self.jump_flag = True

		# Detach player off the ground and change state
		self.ground = False
		self.platform_standing = -1
		self.state = ST_JUMP
		self.deconnect_withOBJ()

		# Change jump animation duration
		self.jump_anim_speed = max(1.0, abs(self.ground_speed))

		# Reset angle and floor mode
		self.ground_angle  = 0
		self.MODE = 0

		# Play the sound
		play_sound(self.SFX_Jump)
	
	# Do the air roll
	if self.press_action() and (not self.ground):
		if (self.state in [ST_SPRING_D, ST_SPRING_H, ST_NORMAL]):
			play_sound(self.SFX_DropDash)
			self.state = ST_JUMP
			self.jump_flag = False
			self.ceiling_lock = 2
			self.jump_anim_speed = max(1.0, 4 - abs(self.ground_speed))
	
	if self.state != ST_JUMP: return None
	
	self.attacking = True

	if (not self.hold_action() and self.speed[1] <= -jump_release and self.jump_flag):
		self.jump_flag = False
		self.speed[1] = -jump_release

	self.anim = ANIM_ROLL
	
	if self.ground: 
		
		self.state = ST_NORMAL

		self.on_object_positionx += 1



def player_state_spindash(self:PlayerBase):
	#  ref : https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_state_spindash/player_state_spindash.gml
	# Trigger the spindash
	if self.state == ST_LOOKDOWN and self.press_action():
		# Reset the spindash pitch
		play_sound(self.SFX_SpinCharge) #audio_sound_pitch(sfx_spindash, 1)
		
		# Change animation
		self.anim = ANIM_SPINDASH
	
		# Reset variables
		self.spindashrev = 0
		self.spindashpitch = 0
		
		# Update the state


		self.state = ST_SPINDASH

		particle = Particle()

		particle.position = vec2(self.position) + vec2(20*-self.facing, 13)
		particle.specification = 0
		particle.animation_name = "Spindash Dust"
		particle.tiled_layerid = self.tiled_layerid
		particle.flipX = min(0, self.facing)
		particle.can_die = False

		self.spindash__part_object = particle
		
		
		

		

	# Stop executing if not spindashing
	if self.state != ST_SPINDASH:
		return None
	
	# Stop the movement
	self.ground_speed = 0
	
	# Change flags
	self.direction_allow = 1 - self.ground
	self.movement_allow = 1 - self.ground
	self.attacking = True

	# Change animation
	self.anim = ANIM_SPINDASH

	# Subtract the spindash rev
	self.spindashrev -= self.spindashrev / 32
	self.spindashpitch -= self.spindashpitch / 28

	# Rev up!
	if self.press_action():
		# Play spindash sound
		self.spindash__part_object.animation_tracker = AnimationTracker()
		play_sound(self.SFX_SpinCharge)

		# Reset the spindash frame
		self.animation_tracker.frame = 0 

		# Update spindash rev
		self.spindashpitch = min(self.spindashpitch + 1, 12)
		self.spindashrev = min(self.spindashrev + 2, 9)

		# Change the spindash sound pitch
		#if self.spindashpitch != 1: #audio_sound_pitch(sfx_spindash, 1 + self.spindashpitch / 13)

	# Release the spindash
	if not self.input_down:
		self.spindash__part_object.kill()
		# Stop the spindash sound
		self.SFX_SpinCharge.stop()

		# Play the release sound
		play_sound(self.SFX_SpinRelease)

		# Lag the camera
		self.CAM_lock_timer = 20

		# Set the self.ground speed and update the state
		if self.ground:
			self.ground_speed = (8 + (self.spindashrev // 2)) * self.facing
		else:
			self.speed[0] = (8 + (self.spindashrev // 2)) * self.facing
		
		self.state = ST_ROLL

def player_state_roll(self:PlayerBase):
	# ref : https://github.com/DarkD04/Harmony-Framework/blob/app/scripts/player_state_roll/player_state_roll.gml
	# List of states that allow for jumping
	can_roll_states = [ST_NORMAL, ST_JUMP, ST_LOOKDOWN, ST_SKID]

	roll_deceleration_speed     = self.constants["roll_deceleration_speed"]
	roll_friction_speed         = self.constants["roll_friction_speed"]
	slprollup                   = self.constants["slprollup"]
	slprolldown                 = self.constants["slprolldown"]
	
	self.can_roll = self.state in can_roll_states
	
	
	# Trigger rolling
	if(self.can_roll and self.input_down and abs(self.ground_speed) > 1 and self.ground):
	
		self.anim = ANIM_ROLL
		
		# Update the state
		if not self.landed:
			self.state = ST_ROLL
			
			# Play the sound
			play_sound(self.SFX_Roll) #play_sound(sfx_roll);
	
	# Stop executing if not rolling
	if(self.state != ST_ROLL):  return None

	self.jump_anim_speed = max(1.0, abs(self.ground_speed/4))
	
	# Change animation and speed
	self.anim = ANIM_ROLL
	
	# Change flags
	self.attacking = True

	# Change on ground flag
	if(self.ground): self.movement_allow = False
	
	
	# Rolling physics
	if(math.copysign(1, self.ground_speed) == math.copysign(1, math.sin(math.radians(self.ground_angle )))): 
		self.ground_speed -= slprollup * math.sin(math.radians(self.ground_angle ))
	else: 
		self.ground_speed -= slprolldown * math.sin(math.radians(self.ground_angle ))
	
	# Rolling driction
	self.ground_speed = approach(self.ground_speed, 0, 0.046875*1.01)
				
	# Stop rolling
	if(abs(self.ground_speed) < 0.5 and not self.force_roll and self.ground) or (get_pressed(K_UP)): 
		self.state = ST_NORMAL
	
	# Reset state back to normal when landing
	if(self.landed): self.state = ST_NORMAL
	
	# Get input
	mov = self.input_right - self.input_left
	
	# Turning to different direction
	if(mov == -math.copysign(1, self.ground_speed) and not self.force_roll): 
		self.ground_speed -= roll_deceleration_speed * -mov;	
	
	
	# Force roll push
	if(abs(self.ground_speed) < 0.5 and self.force_roll):
		if(self.ground_angle  < 20 or self.ground_angle  > 360 - 20): 
			self.ground_speed = 2 * self.facing
	
	# Rolling speed cap
	self.ground_speed = clamp(self.ground_speed, -32, 32)

def player_state_lookdown(self:PlayerBase):
	# ref : https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_state_lookdown/player_state_lookdown.gml
	frc = self.constants["frc"]
	# Trigger look down:
	if(self.state == ST_NORMAL or self.state == ST_KNUXFALL):
		if(self.ground and abs(self.ground_speed) < 1 and self.MODE == 0 and self.input_down):
			self.state = ST_LOOKDOWN
	
	# Stop executing
	if(self.state != ST_LOOKDOWN): return None
	
	# Change flags
	self.movement_allow = False
	self.direction_allow = False
	
	# Change animation
	self.anim = ANIM_LOOKDOWN # animation_play(animator, )
	
	# Slow crouch
	self.ground_speed = approach(self.ground_speed, 0, frc)
	
	# Slope influence
	if 320 >= self.ground_angle  >= 40 : self.ground_speed -= 0.125 * math.sin(math.radians(self.ground_angle ))
	
	# Stop crouching when releasing the down key
	if(not self.input_down): self.state = ST_NORMAL

def player_state_lookup(self:PlayerBase):
	# ref : https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_state_lookup/player_state_lookup.gml
	frc = self.constants["frc"]
	# Trigger look down:
	if(self.state == ST_NORMAL and self.ground and abs(self.ground_speed) < 0.5 and self.MODE == 0 and self.input_up):
		self.state = ST_LOOKUP
	
	# Stop executing
	if(self.state != ST_LOOKUP): return None
	
	# Change flags
	self.movement_allow = False
	self.direction_allow = False
	
	# Change animation
	self.anim = ANIM_LOOKUP
	
	# Slow crouch
	self.ground_speed = approach(self.ground_speed, 0, frc)
	
	# Release
	if(not self.input_up): self.state = ST_NORMAL

def player_state_spring(self:PlayerBase):
	# ref : https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_state_spring/player_state_spring.gml
	# If its not in spring state exit
	if(not self.state in [ST_SPRING_H, ST_SPRING_D]): return None
	
	# Change animation

	if self.state == ST_SPRING_H: self.anim = ANIM_SPRING_H
	if self.state == ST_SPRING_D: self.anim = ANIM_SPRING_D
	
	# Change state when falling
	if(self.speed[1] >= 0): self.state = ST_NORMAL
	
def player_state_skid(self:PlayerBase):
	# ref : https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_state_skid/player_state_skid.gml
	frc = self.constants["frc"]
	# Get input presses
	mov = self.input_right - self.input_left
	
	# Trigger the state
	if(
			self.state == ST_NORMAL 
		and mov == -math.copysign(1,self.ground_speed) 
		and self.ground 
		and abs(self.ground_speed) > 4 
		and math.copysign(1,self.ground_speed) == self.facing 
		and self.MODE == 0 
		and self.control_lock  == 0
		):
	
		# Play animation
		self.anim = ANIM_SKID
		
		# Play the skid sound
		play_sound(self.SFX_Skid) #play_sound(sfx_skid);
		
		# Reset the skid timer and update the state
		self.SKID_timer = 0
		self.state = ST_SKID
	

	# If not skidding stop
	if(self.state != ST_SKID): return None
	
	"""if(self.app.frame%4) == 0:
		OBJ:ObjectsManager = self.parent.object_manager
		OBJ.place(
			"Particle", 
			position= vec2(self.position) + (vec2(0, 15).rotate(-self.ground_angle)), 
			type="Dust",
			layer=LAYER_FOREGROUND
			)"""
		
	# Change flags
	self.direction_allow = False
	self.movement_allow = False
	
	# Add timer
	if(mov == self.facing or mov == 0 or self.MODE != 0) :
		self.SKID_timer += 1
	# Return to normal state in some cases
	
	if(self.SKID_timer > 16 or not self.ground or 180 > self.ground_angle  > 80 or 360-80 > self.ground_angle  > 180):
		self.state = ST_NORMAL
	
	# Decelerate
	
	if(mov == -self.facing): 
		self.ground_speed = approach(self.ground_speed, self.facing, 0.5)
	else :
		self.ground_speed = approach(self.ground_speed, self.facing, frc)

	# Change the animation to skid turn
	if(self.anim != ANIM_SKIDTURN):
		if(
			(-0.5 > self.ground_speed >= -1 and self.anim == ANIM_SKID and -self.facing == 1) or 
			(1 >= self.ground_speed >= 0.5 and self.anim == ANIM_SKID and -self.facing == -1)
			):
			self.anim = ANIM_SKIDTURN

	# Done
	if(self.anim == ANIM_SKIDTURN) and self.animation_has_finished:
		self.anim = ANIM_WALK
		self.state = ST_NORMAL
		self.facing *= -1
		self.ground_speed = 1 * self.facing

def player_state_knockout(self:PlayerBase):
	# Stop executing if not in knockout state
	if self.state != ST_KNOCKOUT:
		return
	
	# Change flags
	self.direction_allow = False
	self.movement_allow = False
	
	# Different knockout states
	if self.knockout_type == K_HURT:
		# Change animation
		self.anim = ANIM_HURT
		
		# Exit when ground
		if self.ground:
			self.state = ST_NORMAL
			self.speed[0] = 0  # ground_speed
			self.knockout_type = 0
		else:
			self.deconnect_withOBJ()
	
	elif self.knockout_type in [K_DIE, K_DROWN]:
		# Change player depth
		#self.depth = "Utilities"
		
		# Remove is_underwater physics if dying
		if self.knockout_type == K_DIE:
			self.is_underwater = False
		
		# Change animation
		self.anim = ANIM_DIE if self.knockout_type == K_DIE else ANIM_DROWN
		
		# Disable collision
		self.collision_allow = False
		
		# Add death timer
		self.death_timer += 1
		
		# Remove effects
		self.shield = S_NONE
		self.invincible_timer = 0
		#self.speed_shoes = 0
		self.invincible = False
		#self.speed_shoes_flag = False
		self.hitbox_allow = False
		
		# Fade out
		"""if self.death_timer == 80:
			if hud.lives != 0 or not self.is_time_over:
				hud.lives -= 1
				if hud.lives != 0 and not self.is_time_over:
					LVL.fade_out = True"""
		
		# Restart game
		"""if self.death_timer == 140 and hud.lives != 0 and not self.is_time_over:
			LVL.restart()"""
		
		# Create game over
		#if self.death_timer == 80:
		#	if self.global_life == 0 or self.is_time_over:
		#		self.music_set_fade("FADE_OUT", 2)
		#		if not self.instance_exists("obj_game_over"):
		#			obj = self.instance_create_layer(0, 0, "Utilities", "obj_game_over")
		#			obj.type = 0 if self.global_life == 0 else 1
		
		# Create bubbles for drowning event
		#if self.global_object_timer % 4 == 0 and self.knockout_type == "K_DROWN":
		#	bubble = self.instance_create_depth(self.position[0], self.position[1] - 12, self.depth - 1, "obj_bubble")
		#	bubble.type = 0
		#	bubble.angle = random.randint(0, 360)
		#

from .state_knux import *
from .state_tails import *

"""
Current
"""
def player_states(self:PlayerBase):
	# ref : https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_states/player_states.gml

	# Default flags:

	
	

	self.direction_allow = True
	self.movement_allow = True
	self.collision_allow = True
	self.gravity_allow = True
	self.hitbox_allow = True

	self.can_jump = False
	self.can_roll = False
	
	
	
	# Sonic states:
	player_state_peelout(self)
	player_state_dropdash(self)
	
	# Tails states:
	player_state_tailsfly(self)
	
	# Knuckles states:
	player_state_glide(self)
	player_state_wallclimb(self)
	player_state_ledgeclimb(self)
	player_state_knuxfall(self)
	player_state_knuxslide(self)
	
	# Common states:
	player_state_normal(self)
	player_state_jump(self)
	player_state_spindash(self)
	player_state_roll(self)
	player_state_lookdown(self)
	player_state_lookup(self)
	player_state_spring(self)
	player_state_skid(self)
	player_state_knockout(self)

	
	# Tails object
	player_handle_tails(self)

	if self.player_id != CHAR_TAILS:
		if self.anim == ANIM_ROLL:
			self.animation_tracker.timer *= int(self.jump_anim_speed*10000)/100000
	self.PUSH = False
	self.landed = False

