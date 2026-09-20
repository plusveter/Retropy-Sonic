from scripts.base import *
from scripts import objects

# FR: Meilleur outil quand j'ai envis de faire quelque chose de beaux dans le code
global game_control, debug_mouse

from ._water import *

def run():
    # initilisation of settings
    kernel.size = kernel.window.size = vec2(360, 200)
    kernel.window.flags = pygame.RESIZABLE
    kernel.mixerscale = 10
    kernel.soundfx.volume = 5
    kernel.music.volume = 0
    kernel.opengl.setup( OPENGL_WINDOW_BUFFERARRAY, datapack.load_text(SHADERFOLDER+"default.vert"), datapack.load_text(SHADERFOLDER+"default.frag"))
    kernel.setup()

    # initilisation of keyboard button
    kernel.controller.add_button(pygame.K_UP        , K_UP      )
    kernel.controller.add_button(pygame.K_DOWN      , K_DOWN    )
    kernel.controller.add_button(pygame.K_RIGHT     , K_RIGHT   )
    kernel.controller.add_button(pygame.K_LEFT      , K_LEFT    )
    kernel.controller.add_button(pygame.K_a         , K_A       )
    kernel.controller.add_button(pygame.K_b         , K_B       )
    kernel.controller.add_button(pygame.K_ESCAPE    , K_ESCAPE  )
    kernel.controller.add_button(pygame.K_s         , K_S       )

    # initialisation of palettes
    palette_array = make_palette_viewer(2)
    kernel.palette.new(P_PLAYERS        )
    kernel.palette.new(P_OBJECTS        )
    kernel.palette.new(P_TILES          )
    kernel.palette.new(P_BACKGROUND     )


    # initilisation of shaders params
    filter_text1 = kernel.opengl.surf_to_texture(datapack.load_imagefile(SHADERFOLDER+"textures/crt.jpg"))
    kernel.opengl.use_texture(texture=filter_text1, name="uFilter")

    screen_text1 = kernel.opengl.prepare_texture(size=kernel.size)
    kernel.opengl.use_texture(texture=screen_text1, name="uScreen")
    kernel.bg_color = kernel.palette.surface.get_palette_at(200)

    # setup
    camera.view_size = kernel.size
    general.load_map("STZ1")
    general.musics = load_musics_from_jsonfile("Data\Game\musics.json")
    tiledmap.load_visible_tilelayers_2Darray(26, 16)
    play_music(general.musics.get(tiledmap.data.properties.get("music_name", ""), -1))
    
    

    # the start of the game loop
    while kernel.running:
        general.mask_array[general.mask_array > -1] = 0

        set_underwater_palette_offset()

        # shaders
        kernel.opengl.update_texture(screen_text1, kernel.screen)
        kernel.opengl.program['uWin'] = [kernel.window.size.x, kernel.window.size.y]
        kernel.opengl.program['uRes'] = [kernel.size.x, kernel.size.y]
        kernel.opengl.program['frames'] = (kernel.frames)%(math.pi * (2**10))

        kernel.refresh()
        general.update()
        kernel.bg_color = tiledmap.data.backgroundcolor

        game_control()
        camera.pre_update()
        tiledmap.pool.updates()
        tiledmap.set_view(camera.x, camera.y, kernel.size.x, kernel.size.y)
        background.camera_position = camera.position
        tiledmap.load_objects()
        tiledmap.refresh_all_tiles()

        # render background
        graphic.palette = P_BACKGROUND
        background.render()
        
        # render each layers
        for layerid in tiledmap.layers:
            layer = tiledmap.layers[layerid]
            if layer.type == "tilelayer":
                
                if tiledmap.prerender_tilelayer(layerid, special_flags=layer.mode):
                    constrain_prerender()
                    
                    graphic.palette = P_TILES
                    draw_prerender()

            elif layer.type == "objectgroup":
                tiledmap.pool.render(layerid)

        render_water()

        surfarray_blit(palette_array, vec2((32*0)+0, 2), pal_id=P_PLAYERS)
        surfarray_blit(palette_array, vec2((32*1)+1, 2), pal_id=P_OBJECTS)
        surfarray_blit(palette_array, vec2((32*2)+2, 2), pal_id=P_TILES)
        surfarray_blit(palette_array, vec2((32*3)+3, 2), pal_id=P_BACKGROUND)
        
        debug_mouse()
    kernel.destroy()


def game_control():
    # FR: C'est une fonction qui n'est pas nécessaire dans la version finale
    mouseposition = camera.get_scale_position(-vec2(pygame.mouse.get_rel()))
    if pygame.mouse.get_pressed()[0]: camera.position += mouseposition

    if pygame.mouse.get_pressed()[2]: 
        i = (kernel.frames*(math.pi)*2)+(kernel.frames)

        effect = objects.WaterEffect()
        effect.layerid = 3
        effect.animation = "Large Bubble"
        effect.position = (
            camera.position + 
            camera.get_scale_position(vec2(pygame.mouse.get_pos())) + 
            vec2(math.cos(i)*60, math.sin(i)*60)
            )

    kernel.framerate = 62
    if not kernel.window.focus:
        kernel.framerate = 20
        old_pos = camera.position.copy()
        tiledmap.reset(object_is_refreshed=0)
        general.reload_map()
        tiledmap.load_visible_tilelayers_2Darray(26, 16)
        camera.position = old_pos

    if get_pressed(K_ESCAPE):
        print("restarted")
        tiledmap.reset()
        general.reload_map()
        tiledmap.load_visible_tilelayers_2Darray(26, 16)

    if get_pressed(K_S):
        save_into_palfile("pal.pal", kernel.palette.array)

def debug_mouse():
    # FR: C'est la même chose que game_control
    if not general.debug_mouse: return

    mousex, mousey = pygame.mouse.get_pos()
    mouse_position = vec2(int(mousex), int(mousey))

    pygame.draw.rect(get_active_surface(), "blue", [mouse_position.x, mouse_position.y, 1, 1], )
    layerposition = tiledmap.offeset_views[1]

    angle, angle_postion = tiledmap.get_collision_angle(layerposition.x+mouse_position.x, layerposition.y+ mouse_position.y, 1)
    
    pygame.draw.rect(get_active_surface(), "green", [angle_postion.x - layerposition.x-1, angle_postion.y -  layerposition.y-1, tiledmap.data.tilewidth+2, tiledmap.data.tileheight+2], 1)
    draw_text(get_sprite_text(f"X:{int(camera.x+mouse_position.x)}\nY:{int(camera.y+mouse_position.y)} \nangle:{angle}", general.dev_font, spacey=2), mouse_position+vec2(16))
        