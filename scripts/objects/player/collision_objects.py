from scripts.base import *
from .base import PlayerBase
from .macros import *

def player_object_collision(self:PlayerBase):
    xprevious = yprevious = hitbox_h = wall_w = 0

    def check_object(**agrs): return False
    def variable_instance_exists(**agrs): return False

    object = check_object(wall_w, hitbox_h, wall_w, hitbox_h)
     
    if(object and yprevious + hitbox_h >= object.bbox_top):
        # This is for rare cases, for example if there's a full moving solid object and you want player to be pushed out
        wall_collision_bottom = False
        
        if(variable_instance_exists(object, "wall_bottom")):
            wall_collision_bottom = object.wall_bottom
        
        # Check flag for if player is below a solid
        on_the_bottom = yprevious + hitbox_h >= object.bbox_bottom and self.ground and wall_collision_bottom
        
        # Difference between current and previous x position of the player
        previous_diff_x = xprevious - x
        
        # Wall collision check cases
        can_left = x + wall_w + previous_diff_x <= object.bbox_left or on_the_bottom
        can_right = x - wall_w + previous_diff_x >= object.bbox_right or on_the_bottom
        
        # Left Wall
        while(check_object(0, hitbox_h, wall_w, hitbox_h) and can_left):
            x -= 1
        
        # Right Wall
        while(check_object(wall_w, hitbox_h, 0, hitbox_h) and can_right):
            x += 1
        

        # Ceiling collision
        while(check_object(wall_w, hitbox_h, wall_w, 0) and y_speed <= 0):
            y+=1
            if(not self.ground): y_speed = 0
            
        
    
    # Landing
    if (check_object(wall_w, 0, wall_w, hitbox_h, True) and not on_object and y_speed >= 0 and self.MODE == 0):
        self.ground_speed = self.speed[0]
        self.ground = True
        self.landed = True
        on_object = True
    
    # FIX: Extending bottom
    bottom_ext = 8+max(y-yprevious, 0)

    # Switch on object flags fix
    if(check_object(wall_w, 0, wall_w, hitbox_h+2, True) and self.MODE == 0): on_object = True
    
    while(check_object(wall_w, 0, wall_w, hitbox_h, True) and self.MODE != 0 and self.MODE != 2): y -= 1;	
    
    if(on_object): self.ground_angle = 0
        
    # Full ground collision POST
    if(self.ground and self.MODE == 0):
        while(check_object(wall_w, 0, wall_w, hitbox_h+bottom_ext, True) and not check_object(wall_w, 0, wall_w, hitbox_h, True)):
            y += 1;	
        
        
        while(check_object(wall_w, 0, wall_w, hitbox_h, True)):
            y -= 1;	
        
        
        if(not check_object(wall_w, 0, wall_w, hitbox_h+bottom_ext, True)):
            on_object = False
        
    
    # Disable on object collision in the air
    if (not self.ground):
        on_object = False


def player_collision_objects(self:PlayerBase):
    self.sensor_UPDATE()

    speed0 = [
        clamp(self.speed[0], -MAX_SPEED, MAX_SPEED)/self.steps, 
        clamp(self.speed[1], -MAX_SPEED, MAX_SPEED)/self.steps
        ]
    
    OBJ:ObjectsManager = self.parent.object_manager

    #print(speed0[0], self.speed[0], self.ground_speed, self.steps)

    self.position, self.STAND_ON_OBJ, datacollision = OBJ.collision_manager(
        self.rectbox[0], 
        standobj=self.STAND_ON_OBJ, 
        GROUNDED=self.ground, 
        SPEED=speed0
        )
    
    STAND_IDOBJ = OBJ.get_STAND_IDOBJ(self.STAND_ON_OBJ)
    self.ground = datacollision["ground"]

    if not datacollision["standobj_rect"] is None:
        if not datacollision["edge_left"] is None: 
            self.edge_left = [datacollision["edge_left"], datacollision["standobj_rect"][1]]
        if not datacollision["edge_right"] is None: 
            self.edge_right = [datacollision["edge_right"], datacollision["standobj_rect"][1]]

    if (datacollision["pivot_left"] != 0 or datacollision["pivot_right"] != 0) and datacollision["pivot_bottom"] <= 1:    
        if datacollision["pivot_left"] != 0:

            offsetx = datacollision["pivot_left"]
            if self.pressed_key(K_LEFT):
                self.PUSH = True
                if self.ground: offsetx = min(0, datacollision["pivot_left"]+1)

            self.position[0] -= offsetx
            if not STAND_IDOBJ is None: self.STAND_ON_OBJ = OBJ.offset_STAND_VALUEOBJ(self.STAND_ON_OBJ, -offsetx)


            if self.ground: self.ground_speed = 0
            self.speed[0] = 0
        
        elif datacollision["pivot_right"] != 0:

            offsetx = datacollision["pivot_right"]
            if self.pressed_key(K_RIGHT):
                self.PUSH = True
                if self.ground: offsetx = max(0, datacollision["pivot_right"]-1)
            
            
            self.position[0] -= offsetx
            if not STAND_IDOBJ is None: self.STAND_ON_OBJ = OBJ.offset_STAND_VALUEOBJ(self.STAND_ON_OBJ, -offsetx)


            if self.ground: self.ground_speed = 0
            self.speed[0] = 0

    
            

    if datacollision["pivot_top"] != 0:
        self.position[1] -= datacollision["pivot_top"]
        if self.speed[1] < 0: self.speed[1] = 0

    if not STAND_IDOBJ is None: 
        self.ground_speed = self.speed[0]
        

    self.sensor_UPDATE()

def player_collision_objects(self:PlayerBase):
    objmanag:ObjectsManager = self.parent.object_manager

    rboxes = objmanag.get_overlapping_boxes(self.rectbox.outlined(1))

    speedx , speedy = self.speed[0], self.speed[1]

    for rbox in rboxes:
        offsetx, offsety = rbox.check_axis(self.rectbox.outlined(1))
        if abs(offsetx) < abs(offsety):
            
            if offsetx > 0: 
                if rbox.enable_left:
                    self.position[0] += offsetx-1
                    if self.ground:
                        if self.ground_speed < -0: 
                            self.ground_speed = 0
                            self.PUSH = True
                    else:
                        if self.speed[0] < 0: 
                            self.speed[0] = 0
                            self.PUSH = True

            
            if offsetx < 0: 
                if rbox.enable_right:
                    self.position[0] += offsetx+1
                    if self.ground: 
                        if self.ground_speed > 0: 
                            self.ground_speed = 0
                            self.PUSH = True
                    else:
                        if self.speed[0] > 0: 
                            self.speed[0] = 0
                            self.PUSH = True
        else:
            
            if offsety >= 0: 
                if speedy < 0:
                    if rbox.enable_bottom:
                        self.position[1] += offsety-1
                        self.position[1] += 1
                        self.speed[1] = 0

                
            else:
                if self.position_rel[1] >= 0:
                    if rbox.enable_up:
                        self.position[1] += offsety+1
                        self.Grounding()
                        if (self.on_object != rbox.objectid) and (self.on_object_height == self.on_object_height):
                            self.on_object_positionx = self.position[0] - (rbox.centerx-((self.rectbox.width/2) +((rbox.width/2))))-self.position_rel[0]
                            self.on_object = rbox.objectid
                            self.on_object_height = rbox.y
                        
                        self.speed[1] = 0
    
    rbox = objmanag.look_for_boxid(self.on_object)
    if rbox:
        self.rectbox = self.rectbox.offset_to_zero()

        combined_x_diameter = (self.rectbox.width + rbox.width)
        combined_y_diameter = (self.rectbox.height+ rbox.height)

        #stand_on_obj_rect = rbox.rect

        #STAND_HEIGHTOBJ = rbox.y
        
        self.on_object_positionx += self.position_rel[0]
        self.ground = True

        self.position[0] = ((rbox.centerx-(combined_x_diameter/2)) + self.on_object_positionx)
        self.position[1] = ((rbox.centery)-(combined_y_diameter/2))
        
        if self.on_object_positionx < 0: self.deconnect_withOBJ(); self.ground = False
        elif self.on_object_positionx > combined_x_diameter: self.deconnect_withOBJ(); self.ground = False
        

    self.sensor_UPDATE()



