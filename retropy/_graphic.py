import pygame, numpy
from pygame import Vector2 as vec2

class Graphic:
    def __init__(self):
        self.image = pygame.Surface(vec2(2))
        self.surfarray:numpy.ndarray = None
        self.rotation_id    = 1
        self.pivot          = vec2(0)
        self.offset = vec2(0)
        self.special_flags  = -1
        self.palette = 0
    
    def get_renderpacket(self, position):
        return (self.image, (position + self.pivot), self.special_flags)

    def get_prerenderpacket(self, position):
        return (self.surfarray, (position + self.pivot), self.special_flags, self.palette)

    def set_prerenderpacker(self, data):
        self.surfarray, self.pivot, self.special_flags, self.palette = data

    def apply_scale(self, new_width:int, new_height:int):

        old_size = vec2(self.image.get_size())   # (h, w)
        new_size = vec2(new_width, new_height)                # (w, h)

        # Match original axis behavior exactly
        scale = vec2(
            new_size.y/old_size.y,  # x uses height
            new_size.x/old_size.x   # y uses width
        )

        self.pivot.x *= scale.x
        self.pivot.y *= scale.y
        self.image = pygame.transform.scale(self.image, new_size)

    def apply_scale_by(self, scale):

        new_size = vec2(self.image.get_size())*scale
        self.pivot *= scale
        self.image = pygame.transform.scale(self.image, new_size)

    def apply_rotation(self, angle):

        angle %= 360

        # No rotation allowed
        if self.rotation_id == 0 or angle == 0: return 

        # Snap rotation
        if self.rotation_id == 2:
            angle = ((angle + 22.5) // 45) * 45
        elif self.rotation_id == 3:
            angle = ((angle + 45) // 90) * 90
        elif self.rotation_id == 4:
            angle = ((angle + 90) // 180) * 180

        # Rotate surface
        rotated_image = pygame.transform.rotate(self.image, angle)

        # Original and new centers
        old_center = vec2(self.image.get_size()) / 2
        new_center = vec2(rotated_image.get_size()) / 2

        # Rotate pivot around center
        direction = old_center + self.pivot
        direction = direction.rotate(-angle)

        self.pivot = -new_center + direction
        self.image = rotated_image
    
    def apply_flip(self, flipX:int|bool=0, flipY:int|bool=0):
        if flipX or flipY:
            self.image = pygame.transform.flip(self.image, flipX, flipY)
            if flipX: self.pivot.x = -(self.pivot.x + self.image.width)
            if flipY: self.pivot.y = -(self.pivot.y + self.image.height)