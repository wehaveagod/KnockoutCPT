import pygame
import pymunk
import slider
import arrow
import button
import random as rand
import numpy as np
import math

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_caption("Knockout CPT")

CLOCK = pygame.time.Clock()
SPACE = pymunk.Space()
FPS = 50

def draw_text(font_size: int, text: str, center_position: tuple[int, int], text_color: tuple[int, int, int] = WHITE, background_color: tuple[int, int, int] = BLACK):
    font = pygame.font.SysFont(None, font_size)
    text_render = font.render(text, True, text_color, background_color)
    text_rect = text_render.get_rect()
    text_rect.center = center_position
    SCREEN.blit(text_render, text_rect)

def run_game():
    SLIDERS_RECTTOP_LEFT_X = 50
    SLIDERS_RECT_TOP_LEFT_Y = 50
    SLIDERS_RECT_WIDTH = SCREEN_WIDTH - 100
    SLIDERS_RECT_HEIGHT = SCREEN_HEIGHT - 100
    SLIDER_RADIUS = 10
    SLIDERS_RECT = pygame.Rect(SLIDERS_RECTTOP_LEFT_X, SLIDERS_RECT_TOP_LEFT_Y, SLIDERS_RECT_WIDTH, SLIDERS_RECT_HEIGHT)
    ARROWHEAD_LENGTH = 10
    MAX_FORCE = 30

    num_player_one_disks = 3
    num_player_two_disks = 3
    all_disks = np.array([])
    disk_idx = -1
    for i in range(num_player_one_disks):
        disk1 = slider.Slider(center_x = rand.randint(SLIDERS_RECTTOP_LEFT_X + SLIDER_RADIUS, SLIDERS_RECTTOP_LEFT_X + SLIDERS_RECT_WIDTH - SLIDER_RADIUS), center_y = rand.randint(SLIDERS_RECT_TOP_LEFT_Y + SLIDER_RADIUS, SLIDERS_RECT_TOP_LEFT_Y + SLIDERS_RECT_HEIGHT - SLIDER_RADIUS), radius = SLIDER_RADIUS, space = SPACE, collision_type = 1, player = 0)
        disk2 = slider.Slider(center_x = rand.randint(SLIDERS_RECTTOP_LEFT_X + SLIDER_RADIUS, SLIDERS_RECTTOP_LEFT_X + SLIDERS_RECT_WIDTH - SLIDER_RADIUS), center_y = rand.randint(SLIDERS_RECT_TOP_LEFT_Y + SLIDER_RADIUS, SLIDERS_RECT_TOP_LEFT_Y + SLIDERS_RECT_HEIGHT - SLIDER_RADIUS), radius = SLIDER_RADIUS, space = SPACE, collision_type = 1, player = 1)
        all_disks = np.append(all_disks, [disk1, disk2])

    running = True
    apply_physics = False
    state = 0
    game_over = False

    SEND_BUTTON = button.Button(WHITE, SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT - 50, 100, 40, pygame.font.SysFont(None, 30), "Send")
        
    while running:
        SCREEN.fill(BLACK)

        pygame.draw.rect(SCREEN, BLUE, SLIDERS_RECT, 3)

        all_velocities_zero = True
        for i in range(len(all_disks)):
            disk_velocity_magnitude = math.hypot(all_disks[i].body.velocity[0], all_disks[i].body.velocity[1])
            if(disk_velocity_magnitude >= 0.2):
                all_velocities_zero = False
                break

        if(all_velocities_zero):
            if(num_player_one_disks == 0 and num_player_two_disks == 0):
                game_over = False
                draw_text(50, "Game is a Tie", (SCREEN_WIDTH / 2, 25), WHITE, BLACK)
            elif(num_player_one_disks == 0):
                game_over = False
                draw_text(50, "Player One Wins", (SCREEN_WIDTH / 2, 25), WHITE, BLACK)
            elif(num_player_two_disks == 0):
                game_over = False
                draw_text(50, "Player Two Wins", (SCREEN_WIDTH / 2, 25), WHITE, BLACK)
            elif(state == 0):
                draw_text(50, "Player One's Turn", (SCREEN_WIDTH / 2, 25), WHITE, BLACK)
            elif(state == 1):
                draw_text(50, "Player Two's Turn", (SCREEN_WIDTH / 2, 25), WHITE, BLACK)
        else:
            draw_text(50, "Launch Targets", (SCREEN_WIDTH / 2, 25), WHITE, BLACK)
            
        apply_physics = not all_velocities_zero
        if((state == 1 and apply_physics) or (state == 2 and not apply_physics)):
            state += 1
            state %= 3

        if(not apply_physics and not game_over):
            SEND_BUTTON.draw(SCREEN)
        else:
            SEND_BUTTON.remove(SCREEN)

        i = all_disks.shape[0] - 1
        while(i >= 0):
            all_disks[i].draw(SCREEN, all_disks[i].player == state)

            if(apply_physics):
                velocity_magnitude = math.hypot(all_disks[i].body.velocity[0], all_disks[i].body.velocity[1])
                friction_vector = (MAX_FORCE * -all_disks[i].body.velocity[0] / velocity_magnitude,
                                   MAX_FORCE * -all_disks[i].body.velocity[1] / velocity_magnitude) if velocity_magnitude != 0 else (0, 0)
                all_disks[i].set_vector(arrow.Arrow(0, 0, 0, 0, BLACK))
                all_disks[i].body.apply_impulse_at_local_point(friction_vector, (0, 0))

                if(not SLIDERS_RECT.collidepoint(all_disks[i].get_center_coord())):
                    if(all_disks[i].player == 0):
                        num_player_one_disks -= 1
                    else:
                        num_player_two_disks -= 1
                    all_disks = np.delete(all_disks, [i])
                    i += 1
            i -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                for i in range(len(all_disks)):
                    if(all_disks[i].is_over_mouse(mouse_pos) and all_disks[i].get_player() == state):
                        disk_idx = i
                        break

                if(disk_idx != -1 and not game_over):
                    start_arrow_x = all_disks[disk_idx].get_center_coord()[0]
                    start_arrow_y = all_disks[disk_idx].get_center_coord()[1]

                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

                    end_arrow_x = start_arrow_x
                    end_arrow_y = start_arrow_y

            elif event.type == pygame.MOUSEMOTION:
                if(disk_idx != -1 and not game_over):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

                    end_arrow_x += event.rel[0]
                    end_arrow_y += event.rel[1]
                    if(SCREEN_RECT.collidepoint(end_arrow_x, end_arrow_y + ARROWHEAD_LENGTH)):
                        disk_arrow = arrow.Arrow(start_arrow_x, start_arrow_y, end_arrow_x, end_arrow_y, BLUE)
                        all_disks[disk_idx].set_vector(disk_arrow)

                for i in range(len(all_disks)):
                    all_disks[i].draw(SCREEN, all_disks[i].player == state)

            elif event.type == pygame.MOUSEBUTTONUP:
                if(disk_idx != -1 and not game_over):
                    disk_idx = -1
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                elif(SEND_BUTTON.is_over_mouse(mouse_pos) and not apply_physics and not game_over):     
                    if(state == 1):
                        apply_physics = True
                        for i in range(len(all_disks)):
                            all_disks[i].set_velocity()
                    else:
                        state += 1
                        state %= 3

        SPACE.step(1 / FPS)
        CLOCK.tick(FPS)
        pygame.display.update()

run_game()