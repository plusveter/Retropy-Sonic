from scripts.base import *
from scripts.objects.player.macros import *

class WaterEffect(TiledObjectEntity):
    def __init__(self, objectid = -1):
        super().__init__(objectid)

        self.animation_tracker = AnimationTracker()
        self.static = vec2(0)
        self.time_to_live = 0
        self.value = 0 
        self.animation = ""
        self.speed = vec2(0)
        
        self.target_player = 0 
        self.is_already_collide = False
        self.static = vec2(self.position)

        self.had_setup = False

    def setup(self):
        self.static = self.position.copy()

        if self.animation[0:9] == "Countdown":
            self.speed.y = -10/(2*1.5)
            self.speed.x = 10/(2*1.5)
            self.time_to_live = 150

        def cancel():...
        self.setup = cancel
        

    def update(self):
        # [IMPORTANT] this feature is required for the system
        super().update()
        self.setup()

        animation_name = self.animation
        waterPoxY = general.water_height

        if self.animation == "Splash":
            self.position.y = waterPoxY
            if self.animation_tracker.has_looped:
                self.kill()
                
                
        elif self.animation in ["Small Bubble", "Large Bubble"]:
            
            self.position.y -= self.speed.y
            self.speed.y = min(self.speed.y+0.05, 0.5)
            self.position.x = self.static.x + (math.sin(math.radians((self.position.y-self.static.y+waterPoxY+self.value)*2))*5)

            if self.animation == "Large Bubble":
                
                if self.value == 1:
                    self.speed.y = 0
                    self.time_to_live -= 1
                    if self.time_to_live <= 0:
                        self.kill()
                else:
                    self.hitbox = rect([-12, -12, 24, 24])

                    for player in check_object_by_classname('Player'):
                        collide = self.Check_Object_Collision_Box(self.hitbox, player, player.hitbox, 0)
                        if collide and abs(self.position.y - self.static.y) > player.bound.height+15:
                            self.value = 1
                            player.air = 0
                            player.speed = vec2(0, 0)
                            player.ground = False
                            player.state = ST_NORMAL
                            player.anim = ANIM_BREATHE
                            play_sound(player.SFX_BubbleGet)
                            self.time_to_live = 20
                
                if self.position.y < waterPoxY-2 and not self.is_already_collide or not general.water_visible:
                    self.is_already_collide = True
                    self.animation_tracker = AnimationTracker()
                
            else:
                if self.position.y < waterPoxY-2 or not general.water_visible:
                    self.kill()
            

        elif self.animation[0:9] == "Countdown":
            player = self.target_player
            self.speed.y += -(self.speed.y)/(4*1.5)
            self.speed.x += -(self.speed.x)/(3*1.5)
            if not self.value:
                self.position.x += self.speed.x
                self.position.y += self.speed.y

                animation_name = "Countdown Appear"
                if self.animation_tracker.has_looped:
                    self.value = True
                    self.static.x = self.position.x - player.position.x
                    self.static.y = self.position.y - player.position.y
                    

            else:
                self.static.x += self.speed.x
                self.static.y += self.speed.y
                self.position.x = self.static.x + player.position.x
                self.position.y = self.static.y + player.position.y

            self.time_to_live += -1
            if self.time_to_live < 0:
                self.kill()

        if self.is_already_collide and self.animation == "Large Bubble":
            animation_name = "Burst"
            self.speed.y = 0

        self.animation_tracker.handle_animation_by_name(general.water_sprites, animation_name)
        if animation_name == "Burst":
            if self.animation_tracker.has_looped:
                self.kill()
                return

        
        
        prerender_name_sprite(general.water_sprites, animation_name, self.animation_tracker, special_flags=pygame.BLEND_ADD)

        if self.animation[0:9] == "Countdown" and self.value:
            array_width, array_height = graphic.surfarray.shape
            jelly_value = math.cos(math.radians(self.time_to_live*15))*3
            apply_scale_on_prerender(array_width-jelly_value, array_height+jelly_value)

            if self.time_to_live < 20:
                apply_scale_by_on_prerender(self.time_to_live/20)

        elif self.animation == "Large Bubble":
            if self.value == 1:
                apply_scale_by_on_prerender(self.time_to_live/20)


        self.draw()

        



    