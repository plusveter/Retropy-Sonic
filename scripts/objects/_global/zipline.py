from scripts.base import *
from ..player import macros as player_macros


class ZipLine(TiledObjectEntity):
    handle_offsety = 10
    handle_width = 16
    handle_height = 24

    rope_height = 1
    rope_color = 4
    rope_shadow_color = 5

    minimum_speed = 2

    move_speed = 128.0
    jump_release_speed = -8.0

    def __init__(self, objectid=-1):
        super().__init__(objectid)

        self.angle = float(self.tiled_properties.get("angle", 0)) % 360
        self.lenght = float(self.tiled_properties.get("lenght", 10))

        self.grip_tracker = AnimationTracker()

        self.start_pos = vec2(self.position)
        self.end_pos = vec2(0)
        self.handle_pos = vec2(self.start_pos)

        self.direction = vec2(0)
        self.velocity = vec2(0)

        self.active_player = None
        self.grab_delay = {}

        self.state = "idle"

        self.ground_speed = 0
        self.max_speed = 10.0
        self.gravity_accel = 0.25

        self.setup_line()

    def setup_line(self):
        rad = numpy.radians(self.angle)

        self.direction = vec2(
            numpy.cos(rad),
            numpy.sin(rad)
        )

        self.end_pos = self.start_pos + self.direction * self.lenght
        self.handle_pos = vec2(self.start_pos)
        # self.velocity = self.direction * self.move_speed

    def set_momentum_from_player(self, player):
        if player.ground:
            self.ground_speed = player.ground_speed

            if 90 <= self.angle <= 270:
                self.ground_speed = -self.ground_speed
        else:
            self.ground_speed = player.speed.dot(self.direction)

        self.ground_speed = clamp(
            self.ground_speed,
            -self.max_speed,
            self.max_speed
        )

        self.velocity = self.direction * self.ground_speed

    def update(self):
        super().update()
        graphic.palette = P_OBJECTS

        if not self.active_player is None:
            tiledmap.pool.add_preceding_obj(self.active_player, self.tiled_id)

        self.update_grab_delays()

        if self.state == "moving":
            self.state_moving()
        elif self.state == "free_moving":
            self.state_free_moving()
        else:
            self.state_idle()

        self.draw_zipline()

    def update_grab_delays(self):
        for player_id in list(self.grab_delay.keys()):
            self.grab_delay[player_id] -= 1
            if self.grab_delay[player_id] <= 0:
                del self.grab_delay[player_id]

    def get_player_key(self, player):
        return getattr(player, "player_id", getattr(player, "entity_id", id(player)))

    def get_handle_hitbox(self):
        offset = self.handle_pos - self.position

        return rect(
            offset.x - self.handle_width / 2,
            offset.y + self.handle_offsety,
            self.handle_width,
            self.handle_height
        )

    def state_idle(self):
        self.try_grab_players()

    def state_moving(self):
        player = self.active_player

        if player is None:
            self.state = "idle"
            return

        player_key = self.get_player_key(player)

        self.advance_handle()
        edge = self.reached_any_end()
        if edge:
            if edge == "start":
                ...
            else:
                self.handle_pos = vec2(self.end_pos)

            
            if self.ground_speed > self.minimum_speed: self.release_player(player, jump=False)

            self.stop_handle_at_edge(edge)
            return

        self.attach_player_to_handle(player)

        if player_key not in self.grab_delay and player.press_action():
            
            self.release_player(player, jump=True)

    def advance_handle(self):
        self.ground_speed += self.direction.y * self.gravity_accel

        self.ground_speed = clamp(
            self.ground_speed,
            -self.max_speed,
            self.max_speed
        )

        self.velocity = self.direction * self.ground_speed
        self.handle_pos += self.velocity

    def grab_player(self, player):
        self.active_player = player
        self.state = "moving"

        player_key = self.get_player_key(player)
        

        self.set_momentum_from_player(player)

        player.state = player_macros.ST_HANG
        player.ground = False
        player.ground_speed = 0
        player.speed = vec2(0)
        player.jump_flag = False
        player.platform_standing = -1

        self.attach_player_to_handle(player)

        self.grab_delay[player_key] = 15
        play_sound(player.SFX_Grab)

    def attach_player_to_handle(self, player):
        player.position = vec2(
            self.handle_pos.x,
            self.handle_pos.y + self.handle_height + self.handle_offsety
        )

        player.speed = vec2(0)
        player.ground_speed = 0
        player.ground = False
        player.state = player_macros.ST_HANG

    def release_player(self, player, jump=False):
        player_key = self.get_player_key(player)

        player.state = player_macros.S_NORMAL
        player.ground = False
        player.platform_standing = -1
        player.jump_flag = False

        if jump:
            player.speed = vec2(self.velocity.x, self.jump_release_speed)
            play_sound(player.SFX_Jump)
        else:
            player.speed = vec2(self.velocity)

        self.grab_delay[player_key] = 60

        self.active_player = None
        
        if jump :
            self.state = "free_moving"
        else:
            self.state = "idle"

    def draw_zipline(self):
        center = (self.end_pos + self.start_pos)/2

        rope_rect = rect(
            0,
            0,
            self.lenght,
            self.rope_height
        )

        array = numpy.zeros((rope_rect.width*rope_rect.height), dtype=numpy.uint8).reshape((rope_rect.width, rope_rect.height))
        array[:, 1:] = self.rope_color
        array[:, :1] = self.rope_shadow_color
        prerender(array, vec2(0))
        graphic.rotation_id = 1
        
        apply_rotation_on_prerender(-self.angle)
        self.draw(0)

        prerender_name_sprite(general.dynamic_sprites, "Grip", self.grip_tracker)
        self.draw(vec2(self.handle_pos)-self.position)

    def reached_any_end(self):
        to_end = self.end_pos - self.start_pos
        to_handle = self.handle_pos - self.start_pos

        line_len_sq = to_end.dot(to_end)
        if line_len_sq <= 0:
            return "start"

        t = to_handle.dot(to_end) / line_len_sq

        if self.ground_speed < 0 and t <= 0:
            return "start"

        if self.ground_speed > 0 and t >= 1:
            return "end"

        return None

    def stop_handle_at_edge(self, edge):
        if edge == "start":...
        elif edge == "end":
            self.handle_pos = vec2(self.end_pos)

        self.ground_speed = 0
        self.velocity = vec2(0)
        self.state = "idle"

    def state_free_moving(self):
        self.advance_handle()

        if self.try_grab_players():
            return

        edge = self.reached_any_end()
        if edge:
            self.stop_handle_at_edge(edge)

    def try_grab_players(self):
        handle_hitbox = self.get_handle_hitbox()

        for player in check_object_by_classname("Player"):
            tiledmap.pool.add_preceding_obj(player, self.tiled_id)

            player_key = self.get_player_key(player)

            if player_key in self.grab_delay:
                continue

            if player.input_down:
                continue

            player_hitbox = player.hitbox

            grab_hitbox = rect(
                player_hitbox.left,
                player_hitbox.top - 4,
                player_hitbox.width,
                8
            )

            if player.Check_Object_Collision_Box(grab_hitbox, self, handle_hitbox, 0):
                self.grab_player(player)
                return True

        return False