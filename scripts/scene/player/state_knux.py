from scripts.base import *
from .base import PlayerBase
from .macros import *

hitbox_w = 9;						# Hitbox width variable
hitbox_h = 19;						# Hitbox height variable
wall_w = 20;						# Horizontal wall radius
wall_h = 0;							# Vertical wall radius

def player_state_glide(self:PlayerBase):
	# https://github.com/DarkD04/Harmony-Framework/blob/50b24129d079e40f1a05dc1ac1bbf359fa8ff558/scripts/player_state_glide/player_state_glide.gml
	# Trigger the glide
	if(self.state == ST_JUMP and self.player_id == CHAR_KNUX and self.press_action()):
		self.control_lock  = 4
		self.glide_speed = 4
		self.knuckles_angle = 90 * self.facing
		self.speed.y = max(self.speed.y, 0.5)
		self.state = ST_KNUXGLIDE
		self.facing = self.facing
		self.anim = ANIM_KNUXGLIDE
	
	#If not gliding then stop
	if(self.state != ST_KNUXGLIDE): return
	
	# Change flags
	self.movement_allow = False
	self.direction_allow = False
	self.gravity_allow = False
	self.attacking = True
	
	# Trigger the slide
	if self.ground: self.state = ST_KNUXSLIDE
	
	# Adjust y speed
	if(self.speed.y < 0.5) : self.speed.y += 0.125
	if(self.speed.y > 0.5) : self.speed.y -= 0.125
	
	# Force x speed to glide speed
	self.speed.x = self.glide_speed * math.sin(math.radians(self.knuckles_angle))
	
	# Accelerate
	if(self.knuckles_angle == 90 or self.knuckles_angle == -90):
		self.glide_speed += 0.015625
	
	# Limit the glide speed
	self.glide_speed = clamp(self.glide_speed, -24, 24)
	
	# Get input
	mov = get_pressed(K_RIGHT) - get_pressed(K_LEFT)
	
	# Glide turn animation
	if(mov == -1 and self.facing == 1 or mov == 1 and self.facing == -1):
		self.facing *= -1 
		self.animation_tracker = AnimationTracker()
		self.anim = ANIM_KNUXGLIDETURN
	
	# Turn glide
	if(mov != 0): self.facing = mov
	
	# Adjust angle
	self.knuckles_angle = approach(self.knuckles_angle, 90 * self.facing, 2.8125)
	
	if	(self.animation_tracker.has_looped and self.anim == ANIM_KNUXGLIDETURN):
		self.anim = ANIM_KNUXGLIDE
	
	# Attach to the wall
	self.get_ANGLE()
	line = rect_to_dmask([min((wall_w)* self.facing, 0), 0, abs((wall_w)* self.facing), 1], self.position)
	
	if line.collide(self.chunk_mask):
		self.can_climb = False

		if self.MODE != 0 or int(self.ground_angle ) != 0:
			self.state = ST_NORMAL
			self.control_lock  = 30
			self.ground = True
			self.ground_speed = self.facing * 4
		else:
			play_sound(self.SFX_GlideGrab)
			self.state = ST_KNUXCLIMB
	
	# Get ground
	if(self.ground and 315 > self.ground_angle  >= 45):
		self.state = ST_NORMAL
		self.control_lock  = 4
	
	# Trigger falling if player is not pressing action button
	if(not self.hold_action() and not self.ground):
		self.ceiling_lock = 4
		self.speed.x *= 0.25
		self.speed.y = 0
		self.state = ST_KNUXFALL

def player_state_knuxfall(self:PlayerBase):
	# If state is not falling stop
	if(self.state != ST_KNUXFALL): return
	
	# Change animations
	if(not self.ground):
		self.anim = ANIM_KNUXFALL
	
	# Play landing sound
	if(self.ground and self.anim == ANIM_KNUXFALL) :
		play_sound(self.SFX_GlideLand)
	
	# Landed
	if(self.ground):
		if self.MODE == 0 and not (315 > self.ground_angle  >= 45):
			self.anim = ANIM_KNUXLAND
			self.ground_speed = 0
		else:
			self.state = ST_NORMAL
	
	# The end of animation
	if(self.anim == ANIM_KNUXLAND and self.animation_tracker.has_looped and not self.landed):
		self.state = ST_NORMAL

def player_state_knuxslide(self:PlayerBase):
	# If not sliding stop executing
	if (self.state != ST_KNUXSLIDE): return
	
	
	# Change flags
	self.direction_allow = False
	self.movement_allow = False
	
	# Change animation
	if(self.ground_speed != 0):
		self.anim = ANIM_KNUXSLIDE
	
	# Get ground
	if (self.ground and self.ground_angle  > 45 and self.ground_angle  < 315):
		self.state = ST_NORMAL
		self.control_lock  = 4
	
	# Ground event
	if(self.ground):
		# Decelerate
		self.ground_speed = approach(self.ground_speed, 0, 0.125)
		
		# Create dust effect
		if((kernel.frames%8) == 0 and self.ground_speed != 0 and not self.landed):
			play_sound(self.SFX_GlideSlide)
			#create_effect(x+random_range(-8, 8), y + hitbox_h, spr_dust_effect, 0.4, depth-1, random_range(0.8, 1.2) * facing, -2, 0, 0.15);

			"""OBJ:ObjectsManager = self.parent.object_manager
			OBJ.place(
				"Particle", 
				position= vec2(self.position) + vec2(0, 10), 
				type="Dust",
				layer=LAYER_FOREGROUND
				)"""
	
	# Make knuckles fall if detached
	if(not self.ground):
		self.state = ST_KNUXFALL
	
	# Change animation
	if(self.ground_speed == 0):
		self.anim = ANIM_KNUXGETUP
	
	# Reset the state
	if(self.anim == ANIM_KNUXGETUP and self.animation_tracker.has_looped):
		self.state = ST_NORMAL


def player_state_wallclimb(self:PlayerBase):
	# If state is not wall climb don't execute
	if(self.state != ST_KNUXCLIMB) : 
		self.can_climb = False
		return
	
	# Change flags
	self.movement_allow = False
	self.direction_allow = False
	self.gravity_allow = False
	jump_strength  = self.constants["jmp"]
	
	# Change direction
	image_xscale = self.facing
	
	# Change animation
	if(self.speed.y != 0) :
		if sign(self.speed.y) == 1: self.anim = ANIM_KNUXCLIMBDOWN
		else: self.anim = ANIM_KNUXCLIMBUP
	else:
		self.anim = ANIM_KNUXCLIMBIDLE
	
	# Get input presses
	mov = get_pressed(K_DOWN) - get_pressed(K_UP)
	
	# Move up and down
	self.speed.y = 1 * mov
	self.speed.x = 0

	if not self.can_climb: return



	# check_object(wall_w + 2, hitbox_h, wall_w + 2, hitbox_h))
	if not self.point_check((wall_w -4) * self.facing, 6) or self.MODE != 0:
		self.state = ST_KNUXFALL
		self.ground = False
	
	# Jump off the wall
	if(self.press_action() and self.control_lock  == 0):
		self.facing *= -1
		self.speed.x = (4/1.25) * self.facing
		self.speed.y = -(4/1.25)
		self.state = ST_JUMP
		self.anim = ANIM_ROLL
		play_sound(self.SFX_Jump)
	
	# Has reached the ground
	if(self.ground):
		self.control_lock  = 4
		self.get_ANGLE()
		self.ground_speed = -2.5 * math.sin(math.radians(self.ground_angle ))
		self.state = ST_NORMAL


def player_state_ledgeclimb(self:PlayerBase):
	# Stop executing if its not specific state
	if(self.state != ST_KNUXLEDGE) : return
	animation_finished = self.animation_tracker.has_looped
	
	# Change flags
	self.movement_allow = False
	self.direction_allow = False
	self.gravity_allow = False
	self.collision_allow = False
	
	# Change animation
	self.anim = ANIM_KNUXLEDGE
	
	# Temp values
	
	# Values for ofsets during animation
	positionarrayx = [1, 	10, 	14+5, 	24, 	22	]
	positionarrayy = [0,	-11, 	-13, 	-15, 	-19	]

	#positionarrayx = [0, 0, 11, 22, 22];
	#positionarrayy = [0,-16, -25, -20, -19];
	
	# Get array length
	length = len(positionarrayx) - 1
	frame = self.animation_tracker.frame
	
	# set position
	if not animation_finished:
		self.position[0] = self.clamp_storex + (positionarrayx[min(frame, length)] * self.facing)
		self.position[1] = self.clamp_storey + (positionarrayy[min(frame, length)])
		self.speed.x = 0
		self.speed.x = 0
		self.sensor_UPDATE()
	
	# Set camera target
	#obj_camera.knux_offset_x = self.clamp_storex + (positionarrayx[length] * self.facing)
	#obj_camera.knux_offset_y = self.clamp_storey + positionarrayy[length]
	# Animation is over, return to normal state
	if(animation_finished and self.control_lock  <= 0):
		
		self.ground_speed = 0
		self.speed = vec2(0)
		self.ground = True
		self.anim = ANIM_STAND
		self.collision_allow = True
		self.state = ST_NORMAL
	
	self.sensor_UPDATE()