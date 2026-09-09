
from scripts.base import *
from .player import Player

class HUD(TiledObjectEntity): # Head Up Display
    def __init__(self, objectid = -1):
        super().__init__(objectid)
        self.delete() # stop the spam of the tilemap object loader

        # this one thing just cancel a new HUD to appear
        if len(check_object(HUD)) > 1: self.kill(); return
        self.position = vec2(0)

        self.score = 0
        self.time = [0, 0, 0]

        self.Axis_X = -2000
        self.ExtraLivePoint = 0
        self.checkpoint = [0, 0, [0, 0, 0]]
    
    def update(self):
        self.check_layer()
        if self.Axis_X < 0: self.Axis_X = min(self.Axis_X +20 ,0)

        # Time
        self.time[2] +=1
        
        if self.time[2] > 60:
            self.time[2] = 0
            self.time[1] += 1
        
        if self.time[1] >= 60:
            self.time[1] = 0
            self.time[0] += 1

        # render
        self.rendering()

    def check_layer(self):
        if tiledmap.layers.get(self.layerid): 
            if tiledmap.layers[self.layerid].name == "HUD": 
                return # skip if these params are true

        layer = check_layer_by_name("HUD")
        if (layer == -1):
            layer = tiledmap.new_layer()
            layer.name = "HUD"
            layer.parallaxx = 0
            layer.parallaxy = 0
            layer.type = LAYERTYPE_OBJECTGROUP
            tiledmap.add_layer(layer)

        self.layerid = layer.id

    def rendering(self):
        graphic.palette = P_OBJECTS
        # score
        Y = 15
        X = 60
        
        X += min(self.Axis_X, -75)+75

        #self.draw_sprite("HUD Elements", 6, ((X-60)+1, Y) )
        self.prerender_number(self.score, ((X+13), Y), space=7)
        self.prerender_sprites("HUD Elements", 2, ((X-60)+4, Y-1))

        # time
        Y += 15 
        X = 60 + min(self.Axis_X, -50)+50

        #self.draw_sprite("HUD Elements", 6, ((X-60)+1, Y) )
        self.prerender_number(self.time[0], (-1+X+((20+4)*0)-8, Y),space=3)
        self.prerender_number(self.time[1], (-1+X+((20+4)*1), Y),  space=2, spacechar="0")
        self.prerender_number(self.time[2], (-1+X+((20+4)*2), Y),  space=2, spacechar="0")
        self.prerender_sprites("HUD Elements", 3, (X+8, Y))

        self.prerender_sprites("HUD Elements", 0, ((X-60)+4, Y-1))

        # rings
        Y += 15
        X = 60 + min(self.Axis_X, -25)+25

        #self.draw_sprite("HUD Elements", 7, ((X-60)+1, Y) )
        self.prerender_number(general.rings, (X+((20+4)*0), Y), space=5)
        self.prerender_sprites("HUD Elements", 1 + (4 if ((self.time[2]//10)%2) == 0 and general.rings == 0 else 0), ((X-60)+4, Y-1))


        Y = (camera.size.y) - 20 +4
        X = 60 + (self.Axis_X)

        self.prerender_sprites("HUD Elements", 6, ((X-60)+20, Y))
        self.prerender_sprites("Life Icons", 0, ((X-60)+10, Y), )

        self.prerender_number(general.lives, ((X-56)+24, Y+4), font=general.dev_font, space=3, spacechar="0")

        self.render_bands()

    def prerender_sprites(self, animation, frame:int, position:vec2, special_flags:int=0):
        prerender_name_sprite(general.hud_sprites, animation, AnimationTracker(frame=frame), special_flags)
        self.draw(position - (camera.size//2))

    def prerender_number(self, number:int, position:vec2, max_value=999, space=0, font=general.hud_numbers_font, spacechar=" "):
        text = str(min(number, max_value))
        text = (spacechar*max(space - len(text), 0)) + text

        for charframe, position_text in get_sprite_text(text, font, spacey=2):
            prerender_frame(charframe)
            self.draw(position_text +vec2(position) - (camera.size//2))

    def render_bands(self):
        # 240 - 254
        if self.Axis_X > -1: return

        SPACE = 50
        SPEED = 1/600
        OFFSETY = 100
        bands = 8
        
        """
        if self.Axis_X < -1900:
            for value in range(bands): 
                set_palette_at(240+value, [255, value*(256/bands), 0])
                set_palette_at(240+value+bands, [0, value*(256/bands), 255])

        elif self.Axis_X > -50:
            for value in range(bands*2): set_palette_at(240+value, [0, 0, 0])
        """
        
        for value in range(bands):
            V = min(((abs((self.Axis_X+1800-(value*SPACE))**2))*SPEED)+OFFSETY, 1000)
            surfarray = numpy.zeros((48*192)).reshape((48, 192))
            surfarray[surfarray == 0] = 240+value

            prerender(surfarray)
            self.draw(vec2((value*surfarray.shape[0]), V) - (camera.size//2))

            
            V = -min(((abs((self.Axis_X+1200-(value*SPACE))**2))*SPEED)+OFFSETY, 1000)
            surfarray = numpy.zeros((48*192)).reshape((48, 192))
            surfarray[surfarray == 0] = 240+value+bands

            prerender(surfarray)
            self.draw(vec2((value*surfarray.shape[0]), V) - (camera.size//2))

    