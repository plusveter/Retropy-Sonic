from scripts.base import *
from .base import PlayerBase
from .macros import *


def dev_control(self:PlayerBase):
	x, y = pygame.mouse.get_pos()
	win_size = self.app.windowsize
	mouse_pressed = pygame.mouse.get_pressed()

	if mouse_pressed[0]:
		self.speed[1] -= (((win_size[1]/2)-y)/200)*1.1
		self.speed[0] -= (((win_size[0]/2)-x)/200)*1.1
	else:
		self.speed[1] = 0
		self.speed[0] = 0

	if mouse_pressed[2]:
		self.state = ST_ROLL

	


def player_movement(self:PlayerBase):

	limit   = self.constants["limit"]

	if False:
		dev_control(self)
	else:
		if (not self.ground) and self.gravity_allow:
			self.MODE = 0
			self.ground_angle  = 0
			self.speed[1] += self.y_accel/self.steps
		self.ground_speed = clamp(self.ground_speed, -MAX_SPEED, MAX_SPEED)

		if self.ground:
			self.speed[0] = float(self.ground_speed * math.cos(math.radians(self.ground_angle )))
			self.speed[1] = float(self.ground_speed * -math.sin(math.radians(self.ground_angle )))

	self.position_rel[0] = clamp(self.speed[0], -MAX_SPEED, MAX_SPEED)/self.steps
	self.position_rel[1] = clamp(self.speed[1], -MAX_SPEED, MAX_SPEED)/self.steps

	self.position[0] = self.position[0]+self.position_rel[0]
	self.position[1] = self.position[1]+self.position_rel[1]
	
