from typing import TypeVar
import pygame as pg

TObjectEntity = TypeVar("TObjectEntity", bound="ObjectEntity")
entity_lastid = 0

C_NONE      = 0
C_RIGHT     = 1
C_TOP       = 2
C_LEFT      = 3
C_BOTTOM    = 4

class ObjectEntity:
	position        :pg.Vector2
	speed           :pg.Vector2
	angle           :int
	hitbox          :pg.Rect
	
	ground          :bool
	ground_speed    :int
	ground_angle    :int

	collision_offset :pg.Vector2

	def __init__(self):
		global entity_lastid

		self.entity_id		= entity_lastid = (entity_lastid+1)
		self.position       = pg.Vector2(0)
		self.speed          = pg.Vector2(0)
		self.hitbox         = pg.Rect([0]*4)

		self.ground         = False
		self.ground_speed   = 0
		self.ground_angle   = 0
		self.ground_object  = False

		self.platform_position = 0 
		self.platform_standing = -1 

		self.collision_offset = pg.Vector2(0) # still in prototype

	# [Position]
	@property
	def x(self): return self.position.x

	@x.setter
	def x(self, new_x): self.position.x = new_x

	@property
	def y(self): return self.position.y

	@y.setter
	def y(self, new_y): self.position.y = new_y

	def Stand_on_Platform(self, self_hitbox:pg.Rect, other_object:TObjectEntity, other_hitbox:pg.Rect):
		self_rect = pg.Rect(
			int(self.position.x + self_hitbox.left) ,
			int(self.position.y + self_hitbox.top),
			self_hitbox.right - self_hitbox.left,
			self_hitbox.bottom - self_hitbox.top,
		)

		other_rect = pg.Rect(
			int(other_object.position.x + other_hitbox.left) ,
			int(other_object.position.y + other_hitbox.top) ,
			other_hitbox.right - other_hitbox.left,
			other_hitbox.bottom - other_hitbox.top,
		)
		
		if self.platform_standing == -1:
			self.ground_speed = self.speed.x
			self.platform_position = self.x - (other_rect.centerx-((self_hitbox.width +(other_rect.width)) /2 ))-self.speed.x
			self.platform_standing = other_object.entity_id
		else:
			if self.platform_standing != other_object.entity_id:
				return 0


		self.ground = True
		self.ground_object = True

		self.platform_position += self.speed.x
		
		self.x -= int(self_rect.right - other_rect.left) - int(self.platform_position)
		self.y -= int(self_rect.bottom - other_rect.top + 0.5) 

		if self.platform_position < 1: 
			self.platform_standing = -1
			
		elif self.platform_position > (self_rect.width + other_rect.width): 
			self.platform_standing = -1
		return 1


	def Check_Object_Collision_Box(self, self_hitbox:pg.Rect, other_object:TObjectEntity, other_hitbox:pg.Rect, set_values:bool):
		# source : https://github.com/RSDKModding/RSDKv5-Decompilation/blob/43d426f8427c5553dab72afc02354e275f9ace48/RSDKv5/RSDK/Scene/Collision.cpp#L276

		collision_side_h = C_NONE
		collision_side_v = C_NONE

		collide_x = self.position.x
		collide_y = self.position.y

		# Fixed-point positions converted to integers
		this_rect = pg.Rect(
			int(other_object.position.x) + other_hitbox.left,
			int(other_object.position.y+0.5) + other_hitbox.top,
			other_hitbox.right - other_hitbox.left,
			other_hitbox.bottom - other_hitbox.top,
		)

		other_rect = pg.Rect(
			int(self.position.x) + self_hitbox.left,
			int(self.position.y+1) + self_hitbox.top,
			self_hitbox.right - self_hitbox.left,
			self_hitbox.bottom - self_hitbox.top,
		)

		#--------------------------------------------
		# Horizontal collision
		#--------------------------------------------

		# Temporarily modify hitbox
		other_rect.top          += 1
		other_rect.bottom       -= 1


		if other_rect.centerx <= this_rect.centerx:
			if this_rect.colliderect(other_rect):
				collision_side_h = C_LEFT
				collide_x = ( other_object.position.x +1 + int( other_hitbox.left - self_hitbox.right) )
		else:
			if this_rect.colliderect(other_rect):
				collision_side_h = C_RIGHT
				collide_x = ( other_object.position.x +0.5 + int( other_hitbox.right - self_hitbox.left) )

		# Restore temporary vertical hitbox changes
		self_hitbox.left       += 1
		self_hitbox.top        -= 1
		self_hitbox.right      -= 1
		self_hitbox.bottom     += 1


		#--------------------------------------------
		# Vertical collision
		#--------------------------------------------

		if other_rect.centery <= this_rect.centery:
			if this_rect.colliderect(other_rect):
				collision_side_v = C_TOP
				collide_y = ( other_object.position.y+0.5 + int( other_hitbox.top - self_hitbox.bottom ) )

		else:
			if this_rect.colliderect(other_rect):
				collision_side_v = C_BOTTOM
				collide_y = ( other_object.position.y+0.5 + int( other_hitbox.bottom - self_hitbox.top ) )

		# Restore temporary horizontal hitbox changes
		other_rect.right        += 1
		other_rect.left         -= 1

		#--------------------------------------------
		# Determine final collision side
		#--------------------------------------------
		side = C_NONE

		cx = int(collide_x - self.position.x)
		cy = int(collide_y - self.position.y)

		side = collision_side_h 
		if ( ( (cx**2) >= (cy**2) and (collision_side_v or not collision_side_h) ) or ( not collision_side_h and collision_side_v ) ): 
			side = collision_side_v
		
		if not set_values : return side
		#--------------------------------------------
		# Apply collision values
		#--------------------------------------------
		if side == C_NONE:
			pass

		elif side == C_TOP:
			
			self.position.y = collide_y
			if self.speed.y > 0: self.speed.y = 0
			
			if ( not self.ground and self.speed.y >= 0 ):
				self.ground_speed = ( self.speed.x )
				self.ground_angle = 0x00
				self.ground = True
				self.ground_object = True

		elif side == C_LEFT:

			vel_x = self.speed.x
			if self.ground: vel_x = self.ground_speed
			self.position.x = collide_x #+ int(vel_x != 0)


			if vel_x > 0:
				self.speed.x = 0
				self.ground_speed = 0

		elif side == C_RIGHT:

			vel_x = self.speed.x
			if self.ground: vel_x = self.ground_speed
			self.position.x = collide_x #- int(vel_x != 0)

			if vel_x < 0:
				self.speed.x = 0
				self.ground_speed = 0

		elif side == C_BOTTOM:
			self.position.y = collide_y
			if self.speed.y < 0: self.speed.y = 0
		
			if (not self.ground and self.speed.y <= 0 ) and False:
				self.ground_angle = 0x80
				self.ground_speed = -self.speed.x
				self.ground = True
				self.ground_object = True

		return side


	def Check_Object_Collision_Platform(self, self_hitbox:pg.Rect, other_object:TObjectEntity, other_hitbox:pg.Rect, set_values:bool):
		# source: https://github.com/RSDKModding/RSDKv5-Decompilation/blob/43d426f8427c5553dab72afc02354e275f9ace48/RSDKv5/RSDK/Scene/Collision.cpp#L489

		# Get integer positions
		this_ix = int(other_object.position.x)
		this_iy = int(other_object.position.y+0.5)

		other_ix = int(self.position.x)-1
		other_iy = int(self.position.y+1)

		other_move_y = int(self.position.y - self.speed.y)



		if (
			(   other_iy + self_hitbox.bottom > this_iy + other_hitbox.top and
				other_move_y + self_hitbox.bottom < this_iy + other_hitbox.bottom and
				this_ix + other_hitbox.left < other_ix + self_hitbox.right and
				this_ix + other_hitbox.right-1 > other_ix + self_hitbox.left) and 

			self.speed.y >= 0
		):
			self.position.y = (other_object.position.y+0.5 + int(other_hitbox.top - self_hitbox.bottom))

			if set_values:
				self.speed.y = 0

				if not self.ground:
					self.ground_speed = self.speed.x
					self.ground_angle = 0x00
					self.ground = True

			return True
		return False

