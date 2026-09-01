from scripts.base import *
from .base import PlayerBase
from .macros import *

def player_state_tailsfly(self:PlayerBase):
    # https://github.com/UltraRing/Harmony-Framework/blob/50b24129d079e40f1a05dc1ac1bbf359fa8ff558/scripts/player_state_tailsfly/player_state_tailsfly.gml
    # Trigger fly
    
    if(self.state == ST_JUMP and self.press_action() and self.player_id == CHAR_TAILS):
        self.tails_timer = 480
        y_accel = 0.03125
        self.state = ST_TAILSFLY
    
    # Stop if not specific state
    if(self.state != ST_TAILSFLY):
        self.y_accel = self.constants["grv"]
        #audio_stop_sound(sfx_tailsfly);
        #audio_stop_sound(sfx_tailstired);
        return
     
    #Speed cap
    self.speed[1] = max(self.speed[1] , -4)
    
    #Changing gravity depending on the action
    if(self.press_action() and self.tails_timer != 0): self.y_accel = -0.125
    if(self.speed[1] <= -1 or self.touching_ceiling or self.tails_timer == 0): self.y_accel = 0.03125
    
    #Subtract timer
    self.tails_timer  = max(self.tails_timer-1, 0)
    
    #Reset the state when player is grounded
    if(self.ground):
        self.state = ST_NORMAL
        return 
    
    if (get_pressed(K_DOWN)):
        self.state = ST_ROLL
        return
    
    #Tired tails
    if self.is_underwater:
        if(self.tails_timer == 0):      self.anim = ANIM_TAILSSWIMTIRED
        else:                           self.anim = ANIM_TAILSSWIM
    else:
        if(self.tails_timer == 0):      self.anim = ANIM_TAILSTIRED
        else:                           self.anim = ANIM_TAILSFLY
    
    if(not self.is_underwater):
        if (kernel.frames % 10) == 0:
            if self.tails_timer != 0:
                play_sound(self.SFX_Flying)
            else:
                play_sound(self.SFX_FlyingFall)
    
    #Weird gravity fix
    if (self.tails_timer == 480-1): self.y_accel = 0.03125
    

def player_handle_tails(self:PlayerBase):
        visual_angle = self.ground_angle

        # Change tails' tail animation depending on players animation
        if self.anim in [ANIM_STAND, ANIM_WAIT, ANIM_LOOKUP, ANIM_LOOKDOWN, ANIM_PUSH]:
            visual_angle = 0
            self.tails_appears = True
            self.tails_facing = self.facing
            self.tails_anim = TAIL_1 #animation_play(animator, TAIL_1);
        
        elif self.anim in [ANIM_SPINDASH, ANIM_SKID, ANIM_SKIDTURN]:
            visual_angle = 0
            self.tails_appears = True
            self.tails_facing = self.facing
            self.tails_anim = TAIL_3 #animation_play(animator, TAIL_3);
        
        elif self.anim ==  ANIM_ROLL:
            self.tails_appears = True
            self.tails_anim = TAIL_2 #animation_play(animator, TAIL_2);

            # Rotating by speed
            if(self.state == ST_JUMP or self.state == ST_ROLL and not self.ground):
                if(sign(self.speed[0]) != 0): self.tails_facing = sign(self.speed[0])
                if(self.tails_facing == 1): visual_angle = math.degrees(math.atan2(self.speed[1], -self.speed[0]))-180
                if(self.tails_facing == -1): visual_angle = math.degrees(math.atan2(-self.speed[1], self.speed[0]))-180
            
            # Ground angle
            if (self.state == ST_ROLL and self.ground):
                if(sign(self.ground_speed) != 0): self.tails_facing = sign(self.ground_speed)
    
        else: 
            self.tails_anim = TAIL_1 #animation_play(animator, TAIL_1);
            self.tails_appears = False

        if self.player_id != CHAR_TAILS:
            self.tails_appears = False
    
        self.tails_visual_angle = visual_angle
