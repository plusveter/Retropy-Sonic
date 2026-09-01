from scripts.base import *
from .base import PlayerBase
from .macros import *


def player_direction(self:PlayerBase):
    # ref : https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_control/player_control.gml
    if(not self.movement_allow): return None
    mouvement =  self.input_right -self.input_left


    if mouvement < 0: self.facing = -1
    if mouvement > 0: self.facing = 1


    top = self.constants["top"]
    acc = self.constants["acc"]
    dec = self.constants["dec"]
    air = self.constants["air"]
    frc = self.constants["frc"]
    slp = self.constants["slp"]


    if self.ground:
        if abs(self.ground_speed) > slp or self.control_lock  > 0: 
            self.ground_speed -= slp*math.sin(math.radians(self.ground_angle ))

        # Move to the left:
        if mouvement == -1 and self.control_lock  == 0:
            if self.ground_speed > 0:
                self.ground_speed -= 0.5
                if self.ground_speed <= 0:
                    self.ground_speed = -0.5
                    
            elif self.ground_speed > -top:
                self.ground_speed -= acc

        # Move to the right:
        if mouvement == 1 and self.control_lock  == 0:
            if self.ground_speed < 0:
                self.ground_speed += 0.5
                if self.ground_speed >= 0:
                    self.ground_speed = 0.5
                
            elif self.ground_speed < top:
                self.ground_speed += acc

        # Control lock quirk
        if self.control_lock  != 0:
            if 0 < self.ground_speed <= 2.5 and 45 <= self.ground_angle  <= 90 and mouvement == -1:
                self.ground_speed = -0.5
                self.facing = -1

            if 0 > self.ground_speed >= 2.5 and 315 >= self.ground_angle  >= 270 and mouvement == 1:
                self.ground_speed = 0.5
                self.facing = 1
        
        # Decelerate when not holding anything:
        if mouvement == 0 and self.control_lock  == 0:
                self.ground_speed -= min(abs(self.ground_speed), frc) * math.copysign(1, self.ground_speed)
    
    if not self.ground:

        # Handle air drag:
        if (0> self.speed[1] > -4):
            self.speed[0] -= self.speed[0]/32
        
        # Move to the left:
        if(self.speed[0] >= -top  and mouvement == -1):
            self.speed[0] -= acc *2
            
        # Move to the right:
        if(self.speed[0] <= top  and mouvement == 1):
            self.speed[0] += acc *2