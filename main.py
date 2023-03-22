import pygame
import pymunk
import slider
import arrow
import button
import numpy as np

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

WIDTH = 600
HEIGHT = 600

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
SPACE = pymunk.Space()
FPS = 50

all_disks = np.array([])
disk_idx = -1

SLIDERS_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT - 50)
ARROWHEAD_LENGTH = 10

running = True

disk1 = slider.Slider(center_x = WIDTH/2, center_y = HEIGHT/2, radius = 10, disk_color = WHITE, space = SPACE)
all_disks = np.append(all_disks, disk1)

LAUNCH_BUTTON = button.Button(WHITE, WIDTH/2 - 50, HEIGHT - 50, 100, 40, pygame.font.SysFont(None, 30), "Launch")
LAUNCH_BUTTON.draw(SCREEN)
    
while running:
    SCREEN.fill(BLACK, SLIDERS_RECT)
    for i in range(len(all_disks)):
        all_disks[i].draw(SCREEN)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
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

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

                end_arrow_x = start_arrow_x
                end_arrow_y = start_arrow_y

        elif event.type == pygame.MOUSEMOTION:
            if(disk_idx != -1):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

                end_arrow_x += event.rel[0]
                end_arrow_y += event.rel[1]
                if(SLIDERS_RECT.collidepoint(end_arrow_x, end_arrow_y + ARROWHEAD_LENGTH)):
                    disk_arrow = arrow.Arrow(start_arrow_x, start_arrow_y, end_arrow_x, end_arrow_y, BLUE)
                    all_disks[disk_idx].set_vector(disk_arrow)

                    SCREEN.fill(BLACK, SLIDERS_RECT)
                    for i in range(len(all_disks)):
                        all_disks[i].draw(SCREEN)

                    pygame.display.update()

        elif event.type == pygame.MOUSEBUTTONUP:
            if(disk_idx != -1):
                disk_idx = -1
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.display.update()
            elif(LAUNCH_BUTTON.is_over_mouse(mouse_pos)):
                for i in range(len(all_disks)):
                    all_disks[i].set_velocity()

    pygame.display.update()
    SPACE.step(1 / FPS)
    CLOCK.tick(FPS)
    