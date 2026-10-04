from scripts.base import *

class Particle(TiledObjectEntity):
    def __init__(self, objectid: int = -1):
        self.animation_tracker = AnimationTracker()
        self.specification = 0
        self.speed = vec2(0)
        self.can_die = True
        self.flipX = 0
        self.palette = P_OBJECTS

        self.surfarray:numpy.ndarray = None
        self.animation_name = ""
        super().__init__(objectid)

    def update(self):
        super().update()
        graphic.palette = self.palette

        if self.specification == 0:
            self.position.x += self.speed.x
            self.position.y += self.speed.y

            dynamic_sprites = general.dynamic_sprites
            self.animation_tracker.handle_animation_by_name( dynamic_sprites, self.animation_name )

            if self.animation_tracker.has_looped and self.can_die:
                self.kill()
                return

            prerender_name_sprite( dynamic_sprites, self.animation_name, self.animation_tracker )

            self.draw()

        elif self.specification == 1:
            prerender(self.surfarray)
            self.speed.y += 0.2
            self.position.x += self.speed.x
            self.position.y += self.speed.y
            apply_flip_on_prerender(self.flipX)
            self.draw()