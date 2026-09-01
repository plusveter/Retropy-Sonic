import pygame as pg

class ObjectEntity:
    position        :pg.Vector2
    speed           :pg.Vector2
    angle           :int
    hitbox          :pg.Rect
    
    ground          :bool
    ground_speed    :int
    ground_angle    :int

    collision_offset :int

    def __init__(self):
        self.position        = pg.Vector2(0)
        self.speed           = pg.Vector2(0)
        self.hitbox          = pg.Rect([0]*4)

        self.ground          = False
        self.ground_speed    = 0
        self.ground_angle    = 0

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


C_NONE      = 0
C_RIGHT     = 1
C_TOP       = 2
C_LEFT      = 3
C_BOTTOM    = 4


def check_object_collision_platform( this_object:ObjectEntity, this_hitbox:pg.Rect, other_object:ObjectEntity, other_hitbox:pg.Rect, set_values:bool):
    # source: https://github.com/RSDKModding/RSDKv5-Decompilation/blob/43d426f8427c5553dab72afc02354e275f9ace48/RSDKv5/RSDK/Scene/Collision.cpp#L489

    # Get integer positions
    this_ix = int(this_object.position.x)
    this_iy = int(this_object.position.y)

    other_ix = int(other_object.position.x)
    other_iy = int(other_object.position.y)

    other_move_y = int(other_object.position.y - other_object.speed.y)

    if (
        (   other_iy + other_hitbox.bottom >= this_iy + this_hitbox.top and
            other_move_y + other_hitbox.bottom <= this_iy + this_hitbox.bottom and
            this_ix + this_hitbox.left < other_ix + other_hitbox.right and
            this_ix + this_hitbox.right > other_ix + other_hitbox.left) and 

        other_object.speed.y >= 0
    ):
        other_object.position.y = (this_object.position.y + int(this_hitbox.top - other_hitbox.bottom))

        if set_values:
            other_object.speed.y = 0

            if not other_object.ground:
                other_object.ground_speed = other_object.speed.x
                other_object.ground_angle = 0x00
                other_object.ground = True

        return True
    return False

def check_object_collision_box( this_object:ObjectEntity, this_hitbox:pg.Rect, other_object:ObjectEntity, other_hitbox:pg.Rect, set_values:bool):
    # source : https://github.com/RSDKModding/RSDKv5-Decompilation/blob/43d426f8427c5553dab72afc02354e275f9ace48/RSDKv5/RSDK/Scene/Collision.cpp#L276

    collision_side_h = C_NONE
    collision_side_v = C_NONE

    collide_x = other_object.position.x
    collide_y = other_object.position.y

    # Fixed-point positions converted to integers
    this_rect = pg.Rect(
        int(this_object.position.x) + this_hitbox.left,
        int(this_object.position.y) + this_hitbox.top,
        this_hitbox.right - this_hitbox.left,
        this_hitbox.bottom - this_hitbox.top,
    )

    other_rect = pg.Rect(
        int(other_object.position.x) + other_hitbox.left,
        int(other_object.position.y) + other_hitbox.top,
        other_hitbox.right - other_hitbox.left,
        other_hitbox.bottom - other_hitbox.top,
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
            collide_x = ( int(this_object.position.x) + int( this_hitbox.left - other_hitbox.right ) )
    else:
        if this_rect.colliderect(other_rect):
            collision_side_h = C_RIGHT
            collide_x = ( int(this_object.position.x) + int( this_hitbox.right - other_hitbox.left ) )+1

    # Restore temporary vertical hitbox changes
    other_hitbox.left       += 1
    other_hitbox.top        -= 1
    other_hitbox.right      -= 1
    other_hitbox.bottom     += 1

    #--------------------------------------------
    # Vertical collision
    #--------------------------------------------

    if other_rect.centery <= this_rect.centery:
        if this_rect.colliderect(other_rect):
            collision_side_v = C_TOP
            collide_y = ( this_object.position.y + int( this_hitbox.top - other_hitbox.bottom ) )

    else:
        if this_rect.colliderect(other_rect):
            collision_side_v = C_BOTTOM
            collide_y = ( this_object.position.y + int( this_hitbox.bottom - other_hitbox.top ) )

    # Restore temporary horizontal hitbox changes
    other_rect.right        += 1
    other_rect.left         -= 1

    #--------------------------------------------
    # Determine final collision side
    #--------------------------------------------
    side = C_NONE

    cx = int(collide_x - other_object.position.x)
    cy = int(collide_y - other_object.position.y)

    side = collision_side_h 
    if ( ( (cx**2) >= (cy**2) and (collision_side_v or not collision_side_h) ) or ( not collision_side_h and collision_side_v ) ): 
        side = collision_side_v
    
        
    if not set_values: return side
    #--------------------------------------------
    # Apply collision values
    #--------------------------------------------

    if side == C_NONE:
        pass

    elif side == C_TOP:
        other_object.position.y = collide_y
        if other_object.speed.y > 0: other_object.speed.y = 0
        
        if ( not other_object.ground and other_object.speed.y >= 0 ):
            other_object.ground_speed = ( other_object.speed.x )
            other_object.ground_angle = 0x00
            other_object.ground = True

    elif side == C_LEFT:
        other_object.position.x = collide_x
        vel_x = other_object.speed.x

        if other_object.ground: vel_x = other_object.ground_speed

        if vel_x > 0:
            other_object.speed.x = 0
            other_object.ground_speed = 0

    elif side == C_RIGHT:
        other_object.position.x = collide_x
        vel_x = other_object.speed.x

        if other_object.ground: vel_x = other_object.ground_speed

        if vel_x < 0:
            other_object.speed.x = 0
            other_object.ground_speed = 0

    elif side == C_BOTTOM:
        other_object.position.y = collide_y
        if other_object.speed.y < 0: other_object.speed.y = 0
    
        if (not other_object.ground and other_object.speed.y <= 0 ):
            other_object.ground_angle = 0x80
            other_object.ground_speed = ( -other_object.speed.x)
            other_object.ground = True

    return side


