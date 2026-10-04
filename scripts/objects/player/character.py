from scripts.base import *
from .base import PlayerBase
from .macros import *

class Character:
	def Spritesload(link_NormalForm, link_SuperForm = None):
		normalform = load_RSDKv5Animations(link_NormalForm)

		sprites_cache = [normalform, normalform]
		return sprites_cache

	# Animation Functions
	def rendering(self:PlayerBase):
		self.animation_tracker.handle_animation_by_name(self.sprites, self.anim)
		self.animation_has_finished = self.animation_tracker.has_looped

		if self.player_id == CHAR_TAILS:
			if self.tails_appears:
				self.tails_animation_tracker.handle_animation_by_name(self.sprites, self.tails_anim)
				prerender_name_sprite(self.sprites, self.tails_anim, self.tails_animation_tracker)
				apply_flip_on_prerender(flipX=min(0, self.tails_facing))
				apply_rotation_on_prerender(self.tails_visual_angle)
				
				self.draw(vec2(0))
		
		set_palette_at(2, kernel.palette.get_array(P_PLAYERS)[(0x10 + 3*self.player_id)], P_PLAYERS)
		set_palette_at(3, kernel.palette.get_array(P_PLAYERS)[(0x11 + 3*self.player_id)], P_PLAYERS)
		set_palette_at(4, kernel.palette.get_array(P_PLAYERS)[(0x12 + 3*self.player_id)], P_PLAYERS)
		
		prerender_name_sprite(self.sprites, self.anim, self.animation_tracker)

		apply_flip_on_prerender(flipX=min(0, self.facing))
		apply_rotation_on_prerender(self.rotation)
		
		self.draw(vec2(0))

	def draw_old(self:PlayerBase):
		cam_coord = vec2(0)
		self.sensor_UPDATE()

		offset_pal = (self.player_id)*3

		self.set_palette_between([2, 5], self.get_palette()[(16+offset_pal):(19+offset_pal)])

		if self.player_id == CHAR_TAILS:
			if self.tails_appears:
				self.render_FrameData(self.sprites.framedata(self.tails_anim, self.tails_animation_tracker))

				self.apply_flip(flipX=min(0, self.tails_facing))
				self.apply_rotation(self.tails_visual_angle)
				self.draw_image([self.position[0]-cam_coord[0], self.position[1]-cam_coord[1]])
		#self.rotation = self.ground_angle 
		self.render_FrameData(self.sprites.framedata(self.anim, self.animation_tracker))

		facing = min(0, self.facing)

		if self.flailing == 1:
			facing = 1

		elif self.flailing == 3:
			facing = 0

		self.apply_flip(flipX=facing)
		self.apply_rotation(self.rotation)
		self.draw_image([self.position[0]-cam_coord[0], self.position[1]-cam_coord[1]])

	def update_constant(self:PlayerBase, constants, SuperForm=False, Underwater=False):
		self.constants = constants

		if Underwater:
			self.constants["top"] 		*= 0.6
			self.constants["acc"] 		*= 0.6
			self.constants["frc"] 		*= 0.6
			self.constants["air_acc"] 	*= 0.6
			self.constants["dec"] 		*= 0.6
			self.constants["roll_friction_speed"] 		*= 0.6
			self.constants["roll_deceleration_speed"] 	*= 1
			self.constants["grv"] = 0.125

		if SuperForm:
			self.constants["top"]					*= 2.0
			self.constants["acc"]					*= 2.0
			self.constants["frc"]					*= 2.0
			self.constants["air_acc"] 				*= 4.0
			#self.constants["dec"] 					*= 0.5
			self.constants["roll_friction_speed"] 	*= 0.5
			self.constants["jmp"] 		*= 2.0
