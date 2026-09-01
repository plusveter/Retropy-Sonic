from scripts.base import *

def set_underwater_palette_offset():
    if not general.water_visible: return
    general.mask_array[:, min(max(int(general.water_height - camera.y), 0), int(kernel.size.y)):] = 32

def render_water():
    if not general.water_visible: return

    water_animation_name = "Waves"
    general.waterwave_tracker.handle_animation_by_name(general.water_sprites, water_animation_name)
    

    prerender_name_sprite(general.water_sprites, water_animation_name, general.waterwave_tracker, special_flags=pygame.BLEND_ADD)

    lenght_surfarray = graphic.surfarray.shape[0]
    y = general.water_height-camera.y
    x = -(camera.x%lenght_surfarray)

    for x0 in range(0, int(kernel.size.x//lenght_surfarray)+2):
        draw_prerender([x0*lenght_surfarray+x, y])
