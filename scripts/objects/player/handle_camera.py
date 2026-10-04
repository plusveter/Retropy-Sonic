from scripts.base import *
from .macros import *

from .base import PlayerBase

def player_handle_camera(self:PlayerBase):
    if camera.mode == -1: return None

    if camera.tiled_objectid  == -1: camera.tiled_objectid = self.tiled_id 
    if camera.tiled_objectid  != self.tiled_id: return
    
    centered_windows = [(camera.view_size.x/2)+camera.x, (camera.view_size.y/2)-camera.look_shift+camera.y]

    freespace_size = [8//1.25 , 24//1.25]
    max_speed = vec2(18, 22)*2
    percentage = 1
    
    camera_x = camera.x
    camera_y = camera.y

    if self.CAM_lock_timer > 0:
        self.CAM_lock_timer -= 1  

    # Loop

    if self.CAM_lock_timer == 0:
        if self.ground and abs(self.speed[1]) < 14: camera_y -= ((centered_windows[1] - self.position[1])/5)

        camera_rect = pygame.Rect(
            centered_windows[0]-freespace_size[0]-self.camera_mouvement[0], 
            centered_windows[1]-freespace_size[1]-self.camera_mouvement[1],
            freespace_size[0]*2, freespace_size[1]*2
            )
        if not camera_rect.collidepoint(self.position):
            if (camera_rect.centerx - self.position[0]) < 0:
                VAR =  min((camera_rect.x+ camera_rect.width) - self.position[0], 0)
                camera_x -= max(VAR*percentage, -max_speed.x)

            elif (camera_rect.centerx - self.position[0]) > 0:
                VAR = max(camera_rect.x - (self.position[0]), 0)
                camera_x -= min(VAR*percentage, max_speed.x)

            if (camera_rect.centery - self.position[1]) < 0:
                VAR = min((camera_rect.y + camera_rect.height) - self.position[1], 0)
                camera_y -= max(VAR*percentage, -max_speed.y)

            elif (camera_rect.centery - self.position[1]) > 0:
                VAR = max(camera_rect.y - (self.position[1] ), 0)
                camera_y -= min(VAR*percentage, max_speed.y)

    camera.x = int(camera_x)
    camera.y = int(camera_y)

    # get_player_coord
    camera.target_x = self.position[0]
    camera.target_y = self.position[1]

    # Look up and down
    if(self.state == ST_LOOKUP): camera.look_timer -= 1
    if(self.state == ST_LOOKDOWN): camera.look_timer += 1
        
    # Restart looking timer
    if(self.state != ST_LOOKUP and camera.look_timer < 0 or self.state != ST_LOOKDOWN and camera.look_timer > 0):
        camera.look_timer = 0
        
    # Shifting time
    if(camera.look_timer <= -120): camera.look_shift = approach(camera.look_shift, -88, 2)
    if(camera.look_timer >= 120): camera.look_shift = approach(camera.look_shift, 88, 2)

    # Shift back
    if(camera.look_timer == 0): camera.look_shift = approach(camera.look_shift, 0, 2)