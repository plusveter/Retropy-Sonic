import sys

import pygame
import numpy as np

pygame.init()

SCREEN_W = 800
SCREEN_H = 600

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

lens_size = 70
lens_pos = [0, 0]
r = (lens_size / 2)# radius

surfarray3d_lens = np.zeros((lens_size, lens_size, 3)) # np -> numpy
blue_overlay = pygame.Surface((lens_size, lens_size))
blue_overlay.fill((40, 30, 200))

while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.draw.circle(screen, (100, 255, 40), (200, 200), 100)
    pygame.draw.circle(screen, (255, 100, 40), (200, 200), 90)

    m_pos = pygame.mouse.get_pos()
    
    lens_pos = [int(m_pos[0]), int(m_pos[1])] # custom function to get mouse position
    surfarray3d_original = pygame.surfarray.array3d(screen) # surf is just the surface that gets blitted on the display later
    
    for x in range(lens_size):
        for y in range(lens_size):
            rad_d = abs((x - r)**2 + (y - r)**2)**0.5 # basically just distance from the center
            surfarray3d_lens[x, y] = surfarray3d_original[int(lens_pos[0] + (x - r) * rad_d/40) % SCREEN_W, int(lens_pos[1] + (y - r) * rad_d/40) % SCREEN_H] # you can change the 40 to other numbers, it changes how much it is distorted

            #surfarray3d_lens[x, y, 0] = int((((int((x - r) * rad_d/40))/SCREEN_W)*256) +128 )%256
            #surfarray3d_lens[x, y, 1] = int((((int((y - r) * rad_d/40))/SCREEN_H)*256) +128 )%256
            #print((x, y), surfarray3d_lens[x, y])
    lens_surf = pygame.surfarray.make_surface(surfarray3d_lens)
    lens_surf.blit(blue_overlay, (0, 0), special_flags=pygame.BLEND_ADD)

    pygame.draw.circle(lens_surf, (255, 0, 255), (r, r), r+20, 20)
    lens_surf.set_colorkey((255, 0, 255))
    screen.blit(lens_surf, lens_surf.get_rect(center=(lens_pos)))
    
    pygame.display.update()
    clock.tick(60)


    