from scripts.base import *
from .macros import *

class PlayerBase(TiledObjectEntity):
	def __init__(self, objectid):
		super().__init__(objectid)
		self.position_rel = [0, 0]

		self.on_object = -1
		self.on_object_positionx = 0
		self.on_object_height = 0

		self.ground = False
		self.ground_speed = 0
		self.ground_angle  = 0
		self.ground_layer = 0

		self.ground_angle_is_typeX = False
		self.floor_delay = 0
		self.speed = vec2(0)
		self.facing = 1
		self.y_accel = 0

		self.flailing = 0

		self.control_lock  = 0
		self.is_underwater = False

		self.form = "Normal"

		self.constants = {}
		self.sprites_cache = {}
		self.palettes = {}

		self.box_type = 0


		self.left_rot = pygame.Rect(0, 0, 0, 0)
		self.right_rot = pygame.Rect(0, 0, 0, 0)
		self.edge_left = [0, 0]
		self.edge_right =[0, 0]
		self.mouse_rot = pygame.Rect(0, 0, 0, 0)
		self.mouse_rot_angle = 0

		self.upward_rotation = False

		self.PUSH = False
		self.MODE = 0
		self.INVINCIBILITY_counter = 0
		self.CONTR_sensor = "N"
		
		self.invincible_angle = 0

		
		

		
		self.setAngle = None

		""" SENSOR: """
		self.sensor_center_Down = rect_to_dmask([-5, 10, 10, 1], self.position)
		self.sensor_Down = rect_to_dmask([-5, 10, 10, 1], self.position)
		self.sensor_Down_SHIFT = rect_to_dmask([-5, 10, 10, 1], self.position)
		self.sensor_Up = rect_to_dmask([-5, 10, 10, 1], self.position)

		self.sensor_ROTATION_right = rect_to_dmask([10, 13, 1, 9], self.position)
		self.sensor_ROTATION_left = rect_to_dmask([-10, 13, 1, 9], self.position)

		self.sensor_STOP_right = rect_to_dmask([6, 13, 1, 9], self.position)
		self.sensor_STOP_left = rect_to_dmask([6, 13, 1, 9], self.position)


		
		self.CAM_lock_timer = 0
		self.SKID_timer = 0

		# camera setup
		self.camera_active = 0
		self.camera_mouvement = [0, 0]
		self.camera_rect = pygame.Rect(0, 0, 10, 10)
		self.camera_coordset = [0, 0]
		self.camera_lagset = 0

		# OBJ
		self.object_timer = 1

		# Spindash
		self.spindashrev = 0
		self.spindashpitch = 0
		self.spindash__part_object = None
		
		#Peelout
		self.Peelout = False

		#Keyboard
		self.input_left 	= 0
		self.input_right 	= 0
		self.input_up 		= 0
		self.input_down 	= 0
		self.input_a 		= 0
		self.input_b 		= 0

		# SoundFX
		self.SFX_Hurt 						= load_soundfx(SOUNDSFOLDER +"Global/Hurt.wav")
		self.SFX_Jump 						= load_soundfx(SOUNDSFOLDER +"Global/Jump.wav")
		#self.SFX_Life 						= load_soundfx("Music/1up.ogg")# Music/1up.ogg
		self.SFX_Roll 						= load_soundfx(SOUNDSFOLDER +"Global/Roll.wav")
		self.SFX_Grab 						= load_soundfx(SOUNDSFOLDER +"Global/Grab.wav")
		self.SFX_Skid 						= load_soundfx(SOUNDSFOLDER +"Global/Skidding.wav")
		self.SFX_Death 						= load_soundfx(SOUNDSFOLDER +"Global/Hurt.wav")
		self.SFX_Drown 						= load_soundfx(SOUNDSFOLDER +"Stage/Drown.wav")
		self.SFX_Spike 						= load_soundfx(SOUNDSFOLDER +"Global/Spike.wav")
		self.SFX_Flying 					= load_soundfx(SOUNDSFOLDER +"Global/Flying.wav")
		self.SFX_FlyingFall 				= load_soundfx(SOUNDSFOLDER +"Global/Tired.wav")
		self.SFX_GlideGrab 					= load_soundfx(SOUNDSFOLDER +"Global/Grab.wav")
		self.SFX_GlideLand 					= load_soundfx(SOUNDSFOLDER +"Global/Land.wav")
		self.SFX_GlideSlide 				= load_soundfx(SOUNDSFOLDER +"Global/Slide.wav")
		self.SFX_Transform2 				= load_soundfx(SOUNDSFOLDER +"Stage/Transform2.wav")
		self.SFX_SpinCharge 				= load_soundfx(SOUNDSFOLDER +"Global/Charge.wav")
		self.SFX_SpinRelease 				= load_soundfx(SOUNDSFOLDER +"Global/Release.wav")
		self.SFX_PeelRelease 				= load_soundfx(SOUNDSFOLDER +"Global/PeelRelease.wav")

		self.SFX_ShieldAction_Fire 			= load_soundfx(SOUNDSFOLDER +"Global/FireDash.wav")
		self.SFX_ShieldAction_Electric 		= load_soundfx(SOUNDSFOLDER +"Global/LightningJump.wav")
		self.SFX_ShieldAction_Bubble 		= load_soundfx(SOUNDSFOLDER +"Global/BubbleBounce.wav")
		self.SFX_ShieldAction_Insta 		= load_soundfx(SOUNDSFOLDER +"Global/InstaShield.wav")
		self.SFX_ShieldObtain_Basic 		= load_soundfx(SOUNDSFOLDER +"Global/BlueShield.wav")
		self.SFX_ShieldObtain_Fire 			= load_soundfx(SOUNDSFOLDER +"Global/FireShield.wav")
		self.SFX_ShieldObtain_Electric 		= load_soundfx(SOUNDSFOLDER +"Global/LightningShield.wav")
		self.SFX_ShieldObtain_Bubble 		= load_soundfx(SOUNDSFOLDER +"Global/BubbleShield.wav")

		self.SFX_WaterWarning 				= load_soundfx(SOUNDSFOLDER +"Stage/Warning.wav")
		self.SFX_DrownAlert					= load_soundfx(SOUNDSFOLDER +"Stage/DrownAlert.wav")
		self.SFX_WaterSplash 				= load_soundfx(SOUNDSFOLDER +"Stage/Splash.wav")
		self.SFX_BubbleGet 					= load_soundfx(SOUNDSFOLDER +"Stage/Breathe.wav")
		self.SFX_Impact3 					= load_soundfx(SOUNDSFOLDER +"Stage/Impact3.wav")
		self.SFX_BadnikDestroy 				= load_soundfx(SOUNDSFOLDER +"Global/Destroy.wav")
		self.SFX_Destroy 					= load_soundfx(SOUNDSFOLDER +"Global/Destroy.wav")
		self.SFX_BossHit 					= load_soundfx(SOUNDSFOLDER +"Stage/BossHit.wav")
		self.SFX_Spring 					= load_soundfx(SOUNDSFOLDER +"Global/Spring.wav")
		self.SFX_Checkpoint 				= load_soundfx(SOUNDSFOLDER +"Global/StarPost.wav")
		self.SFX_SpecialRing 				= load_soundfx(SOUNDSFOLDER +"Global/SpecialRing.wav")
		self.SFX_SpecialWarp 				= load_soundfx(SOUNDSFOLDER +"Global/SpecialWarp.wav")
		self.SFX_DropDash 					= load_soundfx(SOUNDSFOLDER +"Global/DropDash.wav")

		self.SFX_RayDive 					= load_soundfx(SOUNDSFOLDER +"Global/RayDive.wav")
		self.SFX_RaySwoop 					= load_soundfx(SOUNDSFOLDER +"Global/RaySwoop.wav")

		self.SFX_MightyDeflect 				= load_soundfx(SOUNDSFOLDER +"Global/MightyDeflect.wav")
		self.SFX_MightyUnspin 				= load_soundfx(SOUNDSFOLDER +"Global/MightyUnspin.wav")
		self.SFX_MightyDrill 				= load_soundfx(SOUNDSFOLDER +"Global/MightyDrill.wav")
		self.SFX_MightyLand 				= load_soundfx(SOUNDSFOLDER +"Global/MightyLand.wav")
		
		self.SFX_PimPom 					= load_soundfx(SOUNDSFOLDER +"Stage/PimPom.wav")
		self.SFX_RingLeft 					= load_soundfx(SOUNDSFOLDER +"Global/Ring.wav")
		self.SFX_RingRight 					= load_soundfx(SOUNDSFOLDER +"Global/Ring.wav")
		self.SFX_RingSpill 					= load_soundfx(SOUNDSFOLDER +"Global/LoseRings.wav")
		self.SFX_HyperRing 					= load_soundfx(SOUNDSFOLDER +"Global/HyperRing.wav")

		# setupCharacters Variable
		self.player_id = 0
		self.player_list = []
		self.player_num = 0

		self.animation = "N"
		self.sprites:AnimationData
		self.animation_tracker = AnimationTracker()
		self.rotation = 0

		self.tails_anim = ""
		self.tails_animation_tracker = AnimationTracker()
		self.tails_visual_angle = 0
		self.tails_appears = False
		self.tails_timer = 0
		self.tails_facing = 1
		

		self.setupCharacters()

		self.has_died = False

		# Other
		self.anim = ""
		self.jump_flag = False
		self.ceiling_lock = 0
		self.death_timer = 0
		
		self.idle_timer = 0
		self.touching_ceiling = False
		self.animation_has_finished = False
		self.jump_anim_speed = 0
		self.landed = False
		self.steps = 1
		self.hurt_position = vec2(0)
		self.is_time_over = 0

		self.state = 0
		self.knockout_type = 0
		self.shield = S_NONE

		self.invincible_timer = 0
		self.speedup_timer = 0
		self.dropdash_timer = 0
		self.invincible = False

		# Default flags:
		self.collision_allow 	= True
		self.gravity_allow 		= True
		self.hitbox_allow 		= True

		self.force_roll = False
		self.attacking = False
		self.movement_allow = True
		self.direction_allow = True

		# State allowing flags:
		self.can_jump = False
		self.can_roll = True
		
		self.input_disable = False
		self.air = 0

		self.glide_speed = 0
		self.knuckles_angle = 0
		self.chunk_mask = None
		self.clamp_storex = self.position[0]
		self.clamp_storey = self.position[1]
		self.can_climb = False

	def point_check(self, x, y):
		return point_to_dmask([x, y], self.position).collide(self.chunk_mask)
	
	def press_action(self):
		return get_clicked(K_A) or get_clicked(K_B)

	def hold_action(self):
		return self.input_a or self.input_b

	def deconnect_withOBJ(self):
		self.platform_standing = -1
	
	def is_connected_withOBJ(self):
		return self.on_object == -1
	

	def setupCharacters(self):
		"""
		Empty Fonction:
		
		Code that is required after the succession (Example bellow):

		'''
			self.player_list:list[Sonic] = [
				Sonic,Knuckles
			]

			
			for player in self.player_list:
				player.load(self)
				
				
			self.player_list[self.player_id].load_Forms(self)

			self.animation = "Run"

			self.frame = SpriteAnimations.update(self.sprites, self.animation, 0) 

			self.rotation = 0

		'''
		"""
		pass

	def Check_Object_Collision_Box(self, self_hitbox, other_object, other_hitbox, set_values):
		# link : https://github.com/RSDKModding/Sonic-Mania-Decompilation/blob/9dc699428420d752af9767bdb13f585ee0881bc0/SonicMania/Objects/Global/Player.c#L2267
		side  = super().Check_Object_Collision_Box(self_hitbox, other_object, other_hitbox, set_values)


		if side == C_TOP:

			self.controlLock = 0
			self.collisionMode = G_MODE_FLOOR

			other_object.position = vec2(other_object.position)

			colPos = [
				other_object.position.x + other_hitbox.left, 
				 other_object.position.x + other_hitbox.right
			]

			sensorX1 = self.position.x + self.sensor_ROTATION_left.offsetx
			sensorX2 = self.position.x + (self.sensor_ROTATION_left.offsetx + self.sensor_center_Down.offsetx) /2
			sensorX3 = self.position.x + self.sensor_center_Down.offsetx
			sensorX4 = self.position.x + (self.sensor_ROTATION_right.offsetx + self.sensor_center_Down.offsetx) /2
			sensorX5 = self.position.x + self.sensor_ROTATION_right.offsetx

			if sensorX1 >= colPos[0] and sensorX1 <= colPos[1] and sensorX3 >= colPos[0] and sensorX3 <= colPos[1]:
				self.flailing = 0
			else:
				if sensorX1 >= colPos[0] and sensorX1 <= colPos[1]:
					self.flailing = 1

				if sensorX5 >= colPos[0] and sensorX5 <= colPos[1]:
					self.flailing = 5


				if sensorX4 >= colPos[0] and sensorX4 <= colPos[1]:
					self.flailing = 4

				if sensorX3 >= colPos[0] and sensorX3 <= colPos[1]:
					self.flailing = 3


				if sensorX2 >= colPos[0] and sensorX2 <= colPos[1]:
					self.flailing = 2

			return C_TOP

		elif side == C_LEFT:
			self.control_lock = 0
			if (self.input_right and self.ground):
				self.PUSH = True
				#self.ground_speed = -0x8000

			return C_LEFT
		
		elif side == C_RIGHT:
			self.control_lock = 0
			if (self.input_left and self.ground):
				self.PUSH = True
				#self.ground_speed = 0x8000
			return C_RIGHT
		
		elif side == C_BOTTOM:
			return C_BOTTOM
		
		else:
			return C_NONE
		

	def Check_Object_Collision_Platform(self, self_hitbox, other_object:ObjectEntity, other_hitbox, set_values):
		if super().Check_Object_Collision_Platform(self_hitbox, other_object, other_hitbox, set_values):
		
			self.controlLock = 0
			self.collisionMode = G_MODE_FLOOR

			other_object.position = vec2(other_object.position)

			colPos = [
				other_object.position.x + other_hitbox.left, 
				 other_object.position.x + other_hitbox.right
			]

			sensorX1 = self.position.x + self.sensor_ROTATION_left.offsetx
			sensorX2 = self.position.x + self.sensor_center_Down.offsetx
			sensorX3 = self.position.x + self.sensor_ROTATION_right.offsetx

			if sensorX1 >= colPos[0] and sensorX1 <= colPos[1] and sensorX3 >= colPos[0] and sensorX3 <= colPos[1]:
				self.flailing = 0
			else:
				if sensorX1 >= colPos[0] and sensorX1 <= colPos[1]:
					self.flailing = 1

				if sensorX3 >= colPos[0] and sensorX3 <= colPos[1]:
					self.flailing = 3

				if sensorX2 >= colPos[0] and sensorX2 <= colPos[1]:
					self.flailing = 2

			return True

		return False
	

	def get_ANGLE(self, detect=False):
		self.sensor_UPDATE()

		tilewidth, tileheight = tiledmap.data.tilesize
		rotation_left = "N"
		rotation_right = "N"

		if self.ground:
			final_rotation = str(self.MODE * 90)
		else:
			final_rotation = 0

		SIZE = 128
		self.left_rot = pygame.Rect(0, 0, 0, 0)
		self.right_rot = pygame.Rect(0, 0, 0, 0)
		self.mouse_rot = pygame.Rect(0, 0, 0, 0)
		
		s = int(self.steps/12)+2

		y_m = [-1, 1, 1]
		if self.MODE == 1: y_m = [1, -1, -1]


		left_x = self.sensor_ROTATION_left.x
		left_y = self.sensor_ROTATION_left.y

		right_x = self.sensor_ROTATION_right.x
		right_y = self.sensor_ROTATION_right.y
		
		for y in range(y_m[0]*s, y_m[1]*s, y_m[2]):
			for x in range(-s, s):
				rect = self.sensor_ROTATION_left.rect
				rot, position = tiledmap.get_collision_angle(left_x+(x*tilewidth), left_y+(y*tileheight), self.ground_layer)

				tilerect = pygame.Rect(position.x, position.y, tilewidth, tileheight)
				if tilerect.colliderect(rect):
					if rotation_left in ["N", "X"] and (not rot in ["N", "X"]): 
						self.left_rot = tilerect
						rotation_left = rot

				rect = self.sensor_ROTATION_right.rect
				rot, position = tiledmap.get_collision_angle(right_x+(x*tilewidth), right_y+(y*tileheight), self.ground_layer)

				tilerect = pygame.Rect(position.x, position.y, tilewidth, tileheight)
				if tilerect.colliderect(rect):
					if rotation_right in ["N", "X"] and (not rot in ["N", "X"]):
						self.right_rot = tilerect
						rotation_right = rot

		"""
		ROTATION WORK
		"""


		if not rotation_right  == "N": final_rotation = rotation_right
		if not rotation_left == "N": final_rotation = rotation_left

		if rotation_left == "X" and rotation_right == "X":
			final_rotation = rotation_right

		elif rotation_left not in ["N", "X"] and rotation_right not in ["N", "X"]:
			if self.sensor_ROTATION_right.collide(self.chunk_mask):
				final_rotation = rotation_right
			elif self.sensor_ROTATION_left.collide(self.chunk_mask):
				final_rotation = rotation_left

			if rotation_right  == "Y" and not rotation_left  == "Y":
				final_rotation = rotation_left
			
			elif not rotation_right  == "Y" and rotation_left  == "Y":
				final_rotation = rotation_right
		
		else:
			if rotation_right not in ["N", "X"]: final_rotation = rotation_right
			if rotation_left not in ["N", "X"]: final_rotation = rotation_left

		
		if not self.setAngle is None and self.ground:
			final_rotation = self.setAngle

		

		self.ground_angle_is_typeX = False
		if final_rotation == "X":
			final_rotation = self.MODE * 90
			if self.MODE == 0: self.ground_angle_is_typeX = True
		
		if final_rotation == "Y":
			final_rotation = self.ground_angle 

		
		self.ground_angle  = int(final_rotation)%360

		self.floor_delay = max(self.floor_delay-1, 0)

		angle = 44

		new_mode = self.MODE
		if self.ground_angle  >= (360-angle) or self.ground_angle  <= angle: new_mode = 0
		if (90-angle) <=  self.ground_angle  <= (90+angle): new_mode = 1
		if (180-angle) <= self.ground_angle  <= (180+angle): new_mode = 2
		if (270-angle) <= self.ground_angle  <= (270+angle): new_mode = 3

		# The Harmony framework from Ultra Ring Team is goated
		# This floor delay was the only thing missing for the puzzle
		# Thank you guys from the Ultra Team, I wish you to you guys the best.
		if self.floor_delay == 0 and new_mode != self.MODE:
			self.floor_delay = max(32 - math.floor(abs(self.ground_speed * 4)), 0)
			self.MODE = new_mode


	def landing(self):
		if self.speed[1] >= 0:
			if not self.ground:
				self.landed = True
				
				self.SKID_timer = 0
				
				self.Grounding()
				
			self.ground = True
		self.deconnect_withOBJ()
		

	def Grounding(self):
		self.get_ANGLE()
		self.sensor_UPDATE()

		xspeed = self.speed[0]
		yspeed = -self.speed[1]

		gspeed = xspeed

		absXSpeed = abs(xspeed)
		absYSpeed = abs(yspeed)
		absYSpeedHalf = absYSpeed * 0.5
		sign = -math.copysign(1, math.sin(math.radians(self.ground_angle )))

		if self.ground_angle  >= 180:
			# Full Steep
			if self.ground_angle  <= 315.0:
				if absXSpeed <= absYSpeed:
					gspeed = -yspeed

			# Half Steep
			elif self.ground_angle  <= 337.5:
				if absXSpeed <= absYSpeedHalf:
					gspeed = -yspeed * 0.5
			# Shallow
			else: gspeed = xspeed
		else:
			# Full Steep
			if self.ground_angle  >= 45.0:
				if absXSpeed <= absYSpeed:
					gspeed = yspeed

			# Half Steep
			elif self.ground_angle  >= 22.5:
				if absXSpeed <= absYSpeedHalf:
					gspeed = yspeed * 0.5
			# Shallow
			else: gspeed = xspeed

		gspeed = min(gspeed, 24)


		self.speed[1] =  0
		self.speed[0] = gspeed
		self.ground_speed = gspeed

		
	def sensor_UPDATE(self):
		old_bottom = self.hitbox.bottom
		if self.death_timer > 5:
			self.Cancel_Sensor()
		else:
			if self.state in [ST_JUMP, ST_ROLL, ST_KNUXSLIDE, ST_KNUXGLIDE, ST_KNUXFALL, ST_KNUXCLIMB]:
				self.Rolling_Sensor()
			else:
				self.Normal_Sensor()

		if self.ground_speed: self.y += old_bottom -self.hitbox.bottom
		wall_w = 20
		self.sensor_climb = rect_to_dmask([min((wall_w+1)* self.facing, 0)+(wall_w/2), 0, 1, 1], self.position)
		self.sensor_climb_up = rect_to_dmask([min((wall_w+1)* self.facing, 0)+(wall_w/2), -7-4, 1, 1], self.position)

		

	def Normal_Sensor(self):
		# CENTER_POINT
		# SENSOR

		bottom = 19
		top = -19
		left = -8
		right = 8
		
		if self.player_id == CHAR_TAILS: top += 4;bottom -= 4  

		stop_pivot_x = 2
		stop_pivot_y = 0
		if not self.ground: stop_pivot_x = (16-right)
		
		
		rotation_pivot_x = 1
		rotation_pivot_y = -2
		rotation_height = 8
		rotation_width = 1

		width = right-left+1
		height = bottom-top

		offset_width_ground = 0 
		offset_x_ground = 0

		if (self.ground_angle  < 35 or self.ground_angle  > 326) and self.floor_delay == 0: # Sonic
			if self.anim in [ANIM_RUN, ANIM_WALK]: 
				offset_width_ground = 5
			
		offset_x_ground = min(0, self.facing)

		self.hitbox = rect(left-2, top, width+3, height)

		self.sensor_Up = rect_to_dmask([left, top, width, 1], self.position)


		ground_x = (offset_width_ground*offset_x_ground)
		ground_x_neg = (offset_width_ground*(offset_x_ground+1))
		ground_with = width-offset_width_ground

		self.sensor_Down = rect_to_dmask([left-ground_x, bottom, ground_with , 1], self.position)
		
		self.sensor_Down_SHIFT = rect_to_dmask([left-ground_x, bottom, ground_with, 10 + abs(self.ground_speed)+abs(math.cos(math.radians(self.ground_angle ))*4)],
														self.position)
		self.sensor_center_Down = rect_to_dmask([0, 17, 1, 17], self.position)


		Rotationsensor = 0
		if self.speed[1] < 0 and not self.ground and self.upward_rotation:
			if self.CONTR_sensor == "0":
				self.sensor_Down = rect_to_dmask([-6, 8, 13, 0], self.position)
			Rotationsensor = -20

		self.sensor_ROTATION_right = rect_to_dmask(
			[right+rotation_pivot_x-ground_x_neg - int(rotation_width/2), bottom+rotation_pivot_y+Rotationsensor, rotation_width, rotation_height]
			, self.position)
		
		self.sensor_ROTATION_left = rect_to_dmask(
			[left-rotation_pivot_x-ground_x - int(rotation_width/2) , bottom+rotation_pivot_y+Rotationsensor, rotation_width, rotation_height]
			, self.position)

		self.sensor_STOP_right = rect_to_dmask([right+stop_pivot_x, -2, 1, 1], self.position)
		self.sensor_STOP_left = rect_to_dmask([left-stop_pivot_x, -2, 1, 1], self.position)

		if self.ground_angle_is_typeX:
			self.sensor_STOP_right = rect_to_dmask([right+stop_pivot_x, 0, 1, 1], self.position)
			self.sensor_STOP_left = rect_to_dmask([left-stop_pivot_x, 0, 1, 1], self.position)


		self.sensor_Down 			= self.sensor_Down.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_Down_SHIFT 		= self.sensor_Down_SHIFT.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_Up 				= self.sensor_Up.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_ROTATION_right 	= self.sensor_ROTATION_right.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_ROTATION_left 	= self.sensor_ROTATION_left.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_STOP_right 		= self.sensor_STOP_right.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_STOP_left 		= self.sensor_STOP_left.rotate_by_90degrees(self.MODE, self.position)

	def Rolling_Sensor(self):
		# CENTER_POINT
		bottom = 15
		top = -15

		lenght_x = 6
		left = -lenght_x
		right = lenght_x


		if self.player_id == CHAR_TAILS: top += 4;bottom -= 4  
		if self.state in [ST_KNUXGLIDE, ST_KNUXSLIDE]: bottom = 13

		stop_pivot_x = 2
		if not self.ground: stop_pivot_x = (bottom-right)+1
		rotation_pivot_x = 1
		rotation_pivot_y = -2
		rotation_height = 6
		rotation_width = 1

		if self.state in [ST_KNUXGLIDE, ST_KNUXSLIDE]:
			rotation_height = 10


		width = right-left+1
		height = bottom-top

		self.hitbox = rect(left-2, top, width+3, height)
		self.sensor_Up = rect_to_dmask([left, top, width, 1], self.position)
		self.sensor_Down = rect_to_dmask([left, bottom, width, 1], self.position)
		self.sensor_Down_SHIFT = rect_to_dmask([left, bottom-1, width, 16 +abs(math.cos(math.radians(self.ground_angle ))*4)], self.position)
		
		Rotationsensor = 0

		if self.speed[1] < 0 and not self.ground and self.upward_rotation:
			if self.CONTR_sensor == "0":
				self.sensor_Down = rect_to_dmask([-6, 8, 13, 0], self.position)
			Rotationsensor = -20

		

		self.sensor_ROTATION_right = rect_to_dmask([right+rotation_pivot_x-(rotation_width//2), bottom+rotation_pivot_y+Rotationsensor, rotation_width, rotation_height], self.position)
		self.sensor_ROTATION_left = rect_to_dmask([left-rotation_pivot_x+(rotation_width//2), bottom+rotation_pivot_y+Rotationsensor, rotation_width, rotation_height], self.position)

		self.sensor_STOP_right = rect_to_dmask([right+stop_pivot_x, 0, 1, 1], self.position)
		self.sensor_STOP_left = rect_to_dmask([left-stop_pivot_x, 0, 1, 1], self.position)

		if self.ground_angle_is_typeX:
			self.sensor_STOP_right = rect_to_dmask([right+stop_pivot_x, 0, 1, 1], self.position)
			self.sensor_STOP_left = rect_to_dmask([left-stop_pivot_x, 0, 1, 1], self.position)

		""" ROTATION: 0, 1, 2, 3 """
		self.sensor_Down 			= self.sensor_Down.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_Down_SHIFT 		= self.sensor_Down_SHIFT.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_Up 				= self.sensor_Up.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_ROTATION_right 	= self.sensor_ROTATION_right.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_ROTATION_left 	= self.sensor_ROTATION_left.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_STOP_right 		= self.sensor_STOP_right.rotate_by_90degrees(self.MODE, self.position)
		self.sensor_STOP_left 		= self.sensor_STOP_left.rotate_by_90degrees(self.MODE, self.position)
	

	def Cancel_Sensor(self):

		self.hitbox = rect(0, 0, 0, 0)
		self.sensor_center_Down = rect_to_dmask([0, 0, 0, 0], self.position)
		self.sensor_Down = rect_to_dmask([0, 0, 0, 0], self.position)
		self.sensor_Down_SHIFT = rect_to_dmask([0, 0, 0, 0], self.position)
		self.sensor_Up = rect_to_dmask([0, 0, 0, 0], self.position)

		self.sensor_ROTATION_right = rect_to_dmask([0, 0, 0, 0], self.position)
		self.sensor_ROTATION_left = rect_to_dmask([0, 0, 0, 0], self.position)

		self.sensor_STOP_right = rect_to_dmask([0, 0, 0, 0], self.position)
		self.sensor_STOP_left = rect_to_dmask([0, 0, 0, 0], self.position)