from scripts.base import *
from .base import PlayerBase
from .macros import *



def SHIFT_collision(self:PlayerBase):
    self.sensor_UPDATE()

    if self.ground_object: return

    if self.MODE == 0:
        if self.ground:
            self.position[1] += (self.sensor_Down.attract_floor(self.chunk_mask))

    if self.MODE == 1:
        if self.ground:
            self.position[0] += (self.sensor_Down.attract_rightside(self.chunk_mask))

    if self.MODE == 2:
        if self.ground:
            self.position[1] += (self.sensor_Down.attract_ceiling(self.chunk_mask))

    if self.MODE == 3:
        if self.ground:
            self.position[0] += (self.sensor_Down.attract_leftside(self.chunk_mask))

def collision_correction(self:PlayerBase):
    self.sensor_UPDATE()
    up_cond = self.CONTR_sensor == "0"

    isOBJgounded = self.is_connected_withOBJ()

    if self.MODE == 0:
        if self.sensor_Down_SHIFT.collide(self.chunk_mask):
            if self.sensor_Down.collide(self.chunk_mask):
                value = -self.sensor_Down.repel_floor(self.chunk_mask)
                
                if (not up_cond) or ((self.position_rel[1] >= 0 and value >= -(abs(self.position_rel[1])+1)*(2+self.object_timer) or (self.ground and not isOBJgounded))):
                    
                    self.position[1] += value
                    if not self.ground: self.ground_speed = self.speed[0]
                    self.landing()
        else:
            if not self.ground_object: self.ground = False

    elif self.MODE == 1:
        if self.sensor_Down_SHIFT.collide(self.chunk_mask):
            if self.sensor_Down.collide(self.chunk_mask):
                value = -(self.sensor_Down.repel_rightside(self.chunk_mask))

                self.landing()
                self.position[0] += value
        else:
            self.ground = False

    elif self.MODE == 2:
        if self.sensor_Down_SHIFT.collide(self.chunk_mask):
            if self.sensor_Down.collide(self.chunk_mask):
                value = -(self.sensor_Down.repel_ceiling(self.chunk_mask))
                self.position[1] += value
                self.ground = True
        else:
            self.ground = False

    elif self.MODE == 3:
        if self.sensor_Down_SHIFT.collide(self.chunk_mask):
            if self.sensor_Down.collide(self.chunk_mask):
                value = -(self.sensor_Down.repel_leftside(self.chunk_mask))
                self.landing()
                self.position[0] += value
        else:
            self.ground = False




def Collision_Stop(self:PlayerBase):
    self.sensor_UPDATE()
    if self.MODE == 0:
        if self.sensor_STOP_right.collide(self.chunk_mask):
            varx = -(self.sensor_STOP_right.repel_rightside(self.chunk_mask))
            self.position[0] += varx
            if self.speed[0] < 0: 
                self.speed[0] = 0
                self.position[0] += -1
                self.platform_position += -1
            self.platform_position += varx
        if self.sensor_STOP_left.collide(self.chunk_mask):
            varx = -(self.sensor_STOP_left.repel_leftside(self.chunk_mask))
            self.position[0] += varx
            if self.speed[0] > 0: 
                self.speed[0] = 0
                self.position[0] += 1
                self.platform_position += 1
            else:self.platform_position += varx

    if self.MODE == 1:
        if self.sensor_STOP_right.collide(self.chunk_mask):
            self.position[1] += -(self.sensor_STOP_right.repel_ceiling(self.chunk_mask))
        if self.sensor_STOP_left.collide(self.chunk_mask):
            self.position[1] += -(self.sensor_STOP_left.repel_floor(self.chunk_mask))

    if self.MODE == 2:
        if self.sensor_STOP_right.collide(self.chunk_mask):
            self.position[0] += -(self.sensor_STOP_right.repel_leftside(self.chunk_mask))
        if self.sensor_STOP_left.collide(self.chunk_mask):
            self.position[0] += -(self.sensor_STOP_left.repel_rightside(self.chunk_mask))

def Stop_correction(self:PlayerBase):
    self.sensor_UPDATE()
    if self.MODE == 0:
        if self.sensor_STOP_right.collide(self.chunk_mask):
            if self.ground_speed > 0: 
                if (self.state == ST_SKID): self.state = ST_NORMAL
                self.PUSH = True

            self.speed[0] = 0
            self.ground_speed = 0
            # self.position[0] += -(self.sensor_STOP_right.repel_rightside( self.chunk_mask))

        if self.sensor_STOP_left.collide(self.chunk_mask):
            if self.ground_speed < 0:
                if (self.state == ST_SKID): self.state = ST_NORMAL
                self.PUSH = True
                
            self.speed[0] = 0
            self.ground_speed = 0
            # self.position[0] += -(self.sensor_STOP_left.repel_leftside(self.chunk_mask))

    if self.MODE == 1:
        if self.sensor_STOP_right.collide(self.chunk_mask):
            self.ground_speed = 0

        if self.sensor_STOP_left.collide(self.chunk_mask):
            self.ground_speed = 0

    if self.MODE == 2:
        if self.sensor_STOP_right.collide(self.chunk_mask):
            self.PUSH = True
            self.speed[0] = 0
            self.ground_speed = 0
            self.position[0] += -(self.sensor_STOP_right.repel_leftside(self.chunk_mask))

        if self.sensor_STOP_left.collide(self.chunk_mask):
            self.PUSH = True
            self.speed[0] = 0
            self.ground_speed = 0
            self.position[0] += -(self.sensor_STOP_left.repel_rightside(self.chunk_mask))

    if self.MODE == 3:
        if self.sensor_STOP_right.collide(self.chunk_mask):
            self.ground_speed = 0

        if self.sensor_STOP_left.collide(self.chunk_mask):
            self.ground_speed = 0

def UP_collision(self:PlayerBase):
    self.touching_ceiling = False
    self.sensor_UPDATE()
    if self.MODE == 0:
        if self.sensor_Up.collide(self.chunk_mask):
            self.touching_ceiling =True
            self.position[1] += -(self.sensor_Up.repel_ceiling(self.chunk_mask))
            Grounding_Upward(self)
            self.position[1] += 1

def Grounding_Upward(self:PlayerBase):
    self.get_ANGLE()
    xspeed = self.speed[0]
    yspeed = -self.speed[1]

    absXSpeed = abs(xspeed)
    absYSpeed = abs(yspeed)
    gspeed = xspeed

    # Upward Slope (Right)
    if 270.0+20 > self.ground_angle  > 210-20:
        
        if yspeed > -absXSpeed :
            self.ground = True

            gspeed = -yspeed
            if self.ground_angle  <= 210:
                gspeed *= 0.5

            self.ground_speed = gspeed

    elif 136.40625+20 > self.ground_angle  > 90.0-20:
        
        if yspeed > -absXSpeed:
            self.ground = True

            gspeed = yspeed
            if self.ground_angle  >= 136.40625:
                gspeed *= 0.5

            self.ground_speed = gspeed

    if self.speed[1] < 0: self.speed[1] = 0

def player_climb(self:PlayerBase):
    if(self.state != ST_KNUXCLIMB) : return

    self.sensor_UPDATE()
    if self.facing == 1:
        self.position[0] -= self.sensor_climb.repel_rightside(self.chunk_mask)
    else:
        self.position[0] -= self.sensor_climb.repel_leftside(self.chunk_mask)

    self.sensor_UPDATE()
    if self.facing == 1:
        self.position[0] += self.sensor_climb.attract_rightside(self.chunk_mask)
    else:
        self.position[0] += self.sensor_climb.attract_leftside(self.chunk_mask)
    
    wall_w = 20
    self.sensor_UPDATE()
    if not self.can_climb:
        self.position[1] += self.sensor_climb_up.attract_floor(self.chunk_mask)

    else:
        if not self.point_check((wall_w + 1) * self.facing, -4-8) and int(self.ground_angle  == 0):

            # If using smooth scroll
            #if(global.knux_camera_smooth)
            #{
            #	obj_camera.mode = 2;
            #}
            
            self.animation_tracker = AnimationTracker()
            self.control_lock  = 5
            self.clamp_storex = self.position[0]
            self.clamp_storey = self.position[1]
            self.state = ST_KNUXLEDGE

    self.can_climb = True

def player_collision(self:PlayerBase):
    collision_stop_cond = not self.CONTR_sensor == "0" and not self.CONTR_sensor =="1"

    up_cond = not self.CONTR_sensor == "0"
    down_cond = not self.CONTR_sensor == "1"

    if collision_stop_cond:
        Collision_Stop(self)
        
    if up_cond: 
        if (down_cond or self.speed[1] < 0.5):
            UP_collision(self)
    
    if down_cond:
        collision_correction(self)

    if collision_stop_cond: 
        Stop_correction(self)

    if down_cond:
        SHIFT_collision(self)
    else: 
        self.ground = False
    
    player_climb(self)

    self.sensor_UPDATE()

    