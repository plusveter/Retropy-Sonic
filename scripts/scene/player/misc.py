from scripts.base import *
from .base import PlayerBase
from .macros import *


def player_misc(self:PlayerBase):

    if(self.ground_angle  >= 35 and self.ground_angle  <= 360-35 and self.control_lock  == 0 and abs(self.ground_speed) < 2.5): self.control_lock  = 30
    if(self.ground_angle  >= 69 and self.ground_angle  <= 360-69 and abs(self.ground_speed) < 2.5 and not self.force_roll): self.ground = False
            
        
    # Subtract control lock timer
    self.control_lock  = max(self.control_lock  - 1, 0)

    # object
    if not self.is_connected_withOBJ() and self.object_timer == 0.1: self.object_timer = 10
    self.object_timer = max(self.object_timer - 1, 1)
    if self.is_connected_withOBJ(): self.object_timer = 0.1
    
    
    self.CONTR_sensor = "None"
    self.setAngle = None
    if (self.knockout_type == 0): self.invincible_timer = max(self.invincible_timer - 1, 0)


