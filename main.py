import pygame
import pymunk
import disk
import arrow
import numpy as np

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()
SCREEN = pygame.display.set_mode((600, 600))
CLOCK = pygame.time.Clock()
SPACE = pymunk.Space()
FPS = 50

all_disks = np.array([])
disk_idx = -1
run = True

while run:
    for event in pygame.event.get():

        slider = disk.Disk(center_x = 100, center_y = 100, radius = 10, disk_color = WHITE)
        slider.draw(SCREEN)
        all_disks = np.append(all_disks, slider)
        
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            for i in range(len(all_disks)):
                if(all_disks[i].is_over_mouse(mouse_pos)):
                    disk_idx = i
                    break

            if(disk_idx != -1):
                start_arrow_x = all_disks[disk_idx].get_center_x()
                start_arrow_y = all_disks[disk_idx].get_center_y()

                end_arrow_x = start_arrow_x
                end_arrow_y = start_arrow_y

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

        elif event.type == pygame.MOUSEMOTION:
            if(disk_idx != -1):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

                end_arrow_x += event.rel[0]
                end_arrow_y += event.rel[1]

                disk_arrow = arrow.Arrow(start_arrow_x, start_arrow_y, end_arrow_x, end_arrow_y, BLUE)
                all_disks[disk_idx].set_vector(SCREEN, disk_arrow)

                pygame.display.update()

        elif event.type == pygame.MOUSEBUTTONUP:
            disk_idx = -1
            pygame.display.update()
        
    pygame.display.update()
    CLOCK.tick(FPS)
    SPACE.step(1 / FPS)