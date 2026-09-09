from scripts.base import *


from .char_Sonic import Sonic
from .char_Tails import Tails
from .char_Knuckles import Knuckles
from .base import PlayerBase





from .states import player_states
from .water import player_water
from .movement import player_movement
from .collision import player_collision
#from .collision_objects import player_collision_objects
from .misc import player_misc
from .direction import player_direction
from .visual_angle import player_visual_angle
from .handle_hurt import player_handle_hurt
from .handle_camera import player_handle_camera
from .macros import *




MAX = 20
TIME_TRANSFORMATION = 20

class Player(PlayerBase):
	def __init__(self, objectid=-1):
		super().__init__(objectid)
		self.font = None
		self.sound_channel = "Player"
		new_sound_channel(self.sound_channel)
		
	

	def setupCharacters(self):
		# // Player
		self.player_id = 0
		self.player_list:list[Sonic] = [
			Sonic, Tails, Knuckles
		]
		
		for player in self.player_list:
			player.load(self)


		self.player_list[self.player_id].load_Forms(self)
		self.animation = "Run"
		self.frame = AnimationTracker()
		self.rotation = 0

		self.step_0 = 0
		self.step_1 = 0

	def kill(self): ...

	def update(self):
		super().update()
		select_sound_channel(self.sound_channel)
		graphic.palette = P_PLAYERS

		pressed = pygame.key.get_just_pressed()
		if pressed[pygame.K_KP_0]:
			if self.state in [ST_JUMP, ST_NORMAL, ST_LOOKDOWN, ST_LOOKUP]:
				self.player_id = (self.player_id+1)%3
				self.player_list[self.player_id].load_Forms(self)
			

		self.input_left = get_pressed(K_LEFT)
		self.input_right = get_pressed(K_RIGHT)
		self.input_up = get_pressed(K_UP)
		self.input_down = get_pressed(K_DOWN)
		self.input_a = get_pressed(K_A)
		self.input_b = get_pressed(K_B)


		# check if sonic is is_underwater
		player_water(self)

		player_states(self)
		player_direction(self)

		self.steps = 1 + abs(math.floor(abs(self.speed.x)/13)) + abs(math.floor(abs(self.speed.y)/13))
		# print(f"""{str(self.steps):<5} [{str(abs(self.speed[0])):<30} | {str(abs(self.speed[1])):<30}] {str(self.ground_speed):<5}""")
		
		self.chunk_mask = tiledmap.get_chunk_datamask(self.position[0], self.position[1], radius=3+self.steps, tilelayer_id=self.ground_layer)

		for i in range(self.steps):
			player_movement(self)
			if self.collision_allow: # ...
				player_collision(self)
				#player_collision_objects(self)
			self.get_ANGLE()

		self.ground_object = False
		self.flailing = 0
		self.sensor_UPDATE()
		
		player_handle_hurt(self)
		
		player_visual_angle(self)
		player_misc(self)

		# Reset Final
		self.player_list[self.player_id].rendering(self)
		player_handle_camera(self)

		debug = 1
		tile_angles = 0
		sensors_collision = 1
		hitbox_collision = 0

		self.get_ANGLE()
		if debug:
			if tile_angles:
				prerender_rect(self.left_rot	, 1, special_flags=pygame.BLEND_ADD)	;self.draw(-self.position)
				prerender_rect(self.right_rot	, 1, special_flags=pygame.BLEND_ADD)	;self.draw(-self.position)

			if sensors_collision:

				prerender_rect(self.sensor_Down_SHIFT.rect, 		1)		;self.draw(-self.position)
				prerender_rect(self.sensor_Down.rect, 				1)		;self.draw(-self.position)
				prerender_rect(self.sensor_STOP_right.rect, 		1)		;self.draw(-self.position)
				prerender_rect(self.sensor_STOP_left.rect, 			1)		;self.draw(-self.position)
				prerender_rect(self.sensor_Up.rect, 				1)		;self.draw(-self.position)

				prerender_rect(self.sensor_center_Down.rect, 		2)		;self.draw(-self.position)
				prerender_rect(self.sensor_ROTATION_left.rect, 		2)			;self.draw(-self.position)
				prerender_rect(self.sensor_ROTATION_right.rect, 	2)			;self.draw(-self.position)

				prerender_rect(self.sensor_climb.rect, 				1)		;self.draw(-self.position)
				prerender_rect(self.sensor_climb_up.rect, 			1)		;self.draw(-self.position)

			if hitbox_collision:
				prerender_rect(self.hitbox, 						1)		;self.draw()

			
			

