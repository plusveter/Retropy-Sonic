from scripts.base import *
from .base import PlayerBase
from .macros import *

def player_visual_angle(self:PlayerBase):
	# Visual angle
	Math_PI_DOUBLE = math.pi*2

	self.rotation = self.rotation%360
	angle = self.ground_angle 
	if not self.ground: angle = 0

	angle_limit = 45
	angle_limit0 = 5.625

	TOP_MOUV = 12




	if angle <= angle_limit0 or angle >= 360-angle_limit0:
		if angle > angle_limit and angle < 360-angle_limit:
			self.rotation = angle
		else:
			if self.ground:
				self.rotation = 0.0
			else:
				self.rotation += 20 * -math.sin(math.radians(self.rotation))
	else:
		rot = (angle*math.pi)/180.0

		rad_rotation = (self.rotation*math.pi)/180.0

		v = 30
		if (angle <= v or angle >= 360-v):
			rot = 0.0

		if abs(self.ground_speed) <= self.constants["top"]-1:
			rad_rotation += (((rot - rad_rotation + Math_PI_DOUBLE*1.5) % Math_PI_DOUBLE) - math.pi) /  (TOP_MOUV)
		else:
			rad_rotation += (((rot - rad_rotation + Math_PI_DOUBLE*1.5) % Math_PI_DOUBLE) - math.pi) / (TOP_MOUV/2)

		self.rotation = (rad_rotation*180.0)/math.pi