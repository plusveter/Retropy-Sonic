from scripts.base import *

# load Particles
from scripts.objects._global.particle import Particle
from scripts.objects.player.macros  import *

class BreakableTileRegion(TiledObjectEntity):
    namedatas = {
        "falling_tiles": "FallingTiles",
        "ground_break":  "GroundBreak",
    }

    data_dict = {}

    def __init__(self, objectid: int = -1):
        self.has_collide_with_player = False

        self.tile_datas = []


        super().__init__(objectid)

        self.layer_collision = self.tiled_properties.get("collision", 0)
        self.grouplayer_surface = self.tiled_properties.get("surface", 0)
        self.fall_side = self.tiled_properties.get("fall_Side", 0)
        self.destruction_speed = self.tiled_properties.get("destruction speed", 4)

        self.destruction_timer = self.tiled_width + self.tiled_height
        self.collect_tiles()

        if len(self.tile_datas) == 0: 
            self.tile_datas = self.data_dict.get(self.tiled_id, [])

    def kill(self):
        self.data_dict[self.tiled_id] = self.tile_datas
        return super().kill()

    def update(self):
        super().update()

        if self.tiled_name == "falling_tiles":
            self.update_falling_tiles()

        elif self.tiled_name == "ground_break":
            self.update_ground_break()

    def collect_tiles(self):
        if len(self.tile_datas) != 0:
            return

        tilewidth, tileheight = tiledmap.data.tilewidth, tiledmap.data.tileheight
        space_width = int(self.tiled_width / tilewidth)
        space_height = int(self.tiled_height / tileheight)

        for j in range(space_height):
            for i in range(space_width):
                x = i + int(self.position.x / tilewidth)
                y = j + int(self.position.y / tileheight)

                tile_id = tiledmap.get_tile( x, y, self.grouplayer_surface)
                tiledmap.set_tile(0, x, y, self.grouplayer_surface)

                if tile_id != 0:
                    self.tile_datas.append([
                        tiledmap.tiles[tile_id],
                        vec2(i * tilewidth, j * tileheight)
                    ])

    def update_falling_tiles(self):
        self.hitbox = rect(
            self.tiled_offset.x,
            self.tiled_offset.y,
            self.tiled_width,
            self.tiled_height
        )

        if self.has_collide_with_player:
            self.destruction_timer = max( self.destruction_timer - self.destruction_speed, 0 )
        else:
            for player in check_object_by_classname("Player"):
                if player.Check_Object_Collision_Box(player.hitbox, self, self.hitbox, 0):
                    self.has_collide_with_player = True
                    play_sound(general.SFX_LedgeBreak)
                    break

        if self.destruction_timer <= 0:
            return

        save_datas = []

        for tile_array, pos in self.tile_datas:
            prerender(tile_array)

            diagonal_pos = (self.tiled_width - pos.x) + pos.y

            if self.fall_side == 1:
                diagonal_pos = pos.x + pos.y



            particle_position = vec2((self.position.x + pos.x), (self.position.y + pos.y))
            x = int(particle_position.x / tiledmap.data.tilewidth)
            y = int(particle_position.y / tiledmap.data.tileheight)
            

            if self.destruction_timer >= diagonal_pos:
                graphic.palette = P_TILES
                self.draw(vec2(pos.x, pos.y))
                

            if self.destruction_timer > diagonal_pos:
                save_datas.append([tile_array, pos])
            else:
                tiledmap.set_tile(0, x, y, self.layer_collision)

                particle = Particle()
                
                particle.position = vec2(particle_position)
                particle.specification = 1
                particle.surfarray = tile_array
                particle.tiled_layerid = self.tiled_layerid
                particle.palette = P_TILES

        self.tile_datas = save_datas

    def update_ground_break(self):
        if len(self.tile_datas) == 0:
            return

        self.hitbox = rect(
            self.tiled_offset.x,
            self.tiled_offset.y,
            self.tiled_width,
            self.tiled_height
        )
        resist_dropdash = False
        resist_jump = False
        resist_roll = False
        resist_spindash = False
        destroyed = False

        for player in check_object_by_classname("Player"):
            resist_dropdash = resist_dropdash or (
                not self.tiled_properties.get("Resist DropDash", False)
                and player.state == ST_DROPDASH
            )
            resist_jump = resist_jump or (
                not self.tiled_properties.get("Resist Jump", False)
                and player.state == ST_JUMP
            )
            resist_roll = resist_roll or (
                not self.tiled_properties.get("Resist Roll", False)
                and player.state == ST_ROLL
            )
            resist_spindash = resist_spindash or (
                not self.tiled_properties.get("Resist SpinDash", False)
                and player.state == ST_SPINDASH
            )

        
            hitbox = pygame.Rect(self.hitbox)
            hitbox.x += 16 
            collision_side = self.Check_Object_Collision_Box(hitbox, player, player.hitbox, 0)

            if collision_side == C_BOTTOM and player.ground:
                if resist_dropdash or resist_jump or resist_roll or resist_spindash:
                    player.speed.y = -4
                    player.ground = False
                    player.ground_object = 0
                    player.platform_standing = -1
                    if player.state == ST_SPINDASH: 
                        if player.spindash__part_object:
                            player.spindash__part_object.kill()
                        player.state = ST_ROLL
                    destroyed = True
                    play_sound(general.SFX_LedgeBreak3)
                    break


        for tile_array, pos in self.tile_datas:
            prerender(tile_array)

            if destroyed:
                particle_position = vec2((self.position.x + pos.x), (self.position.y + pos.y))
                x = int(particle_position.x / tiledmap.data.tilewidth)
                y = int(particle_position.y / tiledmap.data.tileheight)
                tiledmap.set_tile(0, x, y, self.layer_collision)

                particle = Particle()
                particle.position = vec2(particle_position)
                particle.specification = 1
                particle.surfarray = tile_array
                particle.speed.y = -(5 + (1 - abs(pos.y / self.tiled_height)))
                particle.speed.x = -(((self.tiled_width / 2) - pos.x) / (self.tiled_width / 2))
                particle.tiled_layerid = self.tiled_layerid
                particle.palette = P_TILES

            else:
                # if self.debug: prerender_rect(rect(0, 0, self.tiled_width, self.tiled_height), 1)
                graphic.palette = P_TILES
                self.draw(vec2(pos.x, pos.y))

        if destroyed:
            self.tile_datas = []