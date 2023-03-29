import pygame
import pymunk
import slider
import arrow
import button
import dropdown
import random as rand
import numpy as np
import math
import sys
import time

#Color definitions
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#Game window definitions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

#Initializing Pygame window
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_caption("Knockout CPT")
CLOCK = pygame.time.Clock()
SPACE = pymunk.Space()
FPS = 50

#Function to convert time integer to string representation
def draw_text(font_size: int, text: str, center_position: tuple[int, int], text_color: tuple[int, int, int] = WHITE, background_color: tuple[int, int, int] = BLACK):
    font = pygame.font.SysFont(None, font_size)
    text_render = font.render(text, True, text_color, background_color)
    text_rect = text_render.get_rect()
    text_rect.center = center_position
    SCREEN.blit(text_render, text_rect)

#Function for menu screen
def menu():
    SCREEN.fill(BLACK)

    start_game = False

    draw_text(80, "KNOCKOUT CPT", (SCREEN_WIDTH / 2, 50), WHITE, BLACK)

    START_BUTTON = button.Button(GREEN, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 200, 200, 100, 50, "Start")
    START_BUTTON.draw(SCREEN)

    NUM_TOKENS_DROPDOWN = dropdown.DropDown(button.Button(WHITE, 50, 275, 200, 80, text = "Choose Token Number", font_size = 30), options = np.array(["3", "5", "7", "9"]))
    NUM_TOKENS_DROPDOWN.draw(SCREEN)

    SPEED_DROPDOWN = dropdown.DropDown(button.Button(WHITE, 300, 275, 200, 80, text = "Choose Token Speed", font_size = 30), options = np.array(["Slow", "Normal", "Medium", "Fast"]))
    SPEED_DROPDOWN.draw(SCREEN)

    ARENA_SIZE_DROPDOWN = dropdown.DropDown(button.Button(WHITE, 550, 275, 200, 80, text = "Choose Arena Size", font_size = 30), options = np.array(["Small", "Normal", "Medium", "Large"]))
    ARENA_SIZE_DROPDOWN.draw(SCREEN)

    while not start_game:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
            
            if(event.type == pygame.MOUSEBUTTONUP):
                mouse_pos = pygame.mouse.get_pos()

                if(START_BUTTON.is_over_mouse(mouse_pos) and not SPEED_DROPDOWN.get_show_full_menu() and not NUM_TOKENS_DROPDOWN.get_show_full_menu() and not ARENA_SIZE_DROPDOWN.get_show_full_menu()):
                    start_game = True
                elif(NUM_TOKENS_DROPDOWN.is_over_mouse(mouse_pos)):
                    NUM_TOKENS_DROPDOWN.update(SCREEN)
                elif(SPEED_DROPDOWN.is_over_mouse(mouse_pos)):
                    SPEED_DROPDOWN.update(SCREEN)
                elif(ARENA_SIZE_DROPDOWN.is_over_mouse(mouse_pos)):
                    ARENA_SIZE_DROPDOWN.update(SCREEN)

        pygame.display.update()
    
    return int(NUM_TOKENS_DROPDOWN.get_current_option()), SPEED_DROPDOWN.get_current_option(), ARENA_SIZE_DROPDOWN.get_current_option()

#Function for running the game
def run_game(num_tokens: int, speed: str, arena_size: str) -> bool:
    SPEED_TO_NUM = {"Slow": 100, "Normal": 300, "Medium": 500, "Fast": 700}
    ARENA_SIZE_TO_NUM = {"Small": 300, "Normal": 400, "Medium": 500, "Large": 600}

    SLIDERS_RECTTOP_LEFT_X = SCREEN_WIDTH / 2 - ARENA_SIZE_TO_NUM[arena_size] / 2
    SLIDERS_RECT_TOP_LEFT_Y = SCREEN_HEIGHT / 2 - ARENA_SIZE_TO_NUM[arena_size] / 2
    SLIDERS_RECT_WIDTH = ARENA_SIZE_TO_NUM[arena_size]
    SLIDERS_RECT_HEIGHT = ARENA_SIZE_TO_NUM[arena_size]
    SLIDER_RADIUS = 10
    SLIDERS_RECT = pygame.Rect(SLIDERS_RECTTOP_LEFT_X, SLIDERS_RECT_TOP_LEFT_Y, SLIDERS_RECT_WIDTH, SLIDERS_RECT_HEIGHT)
    ARROWHEAD_LENGTH = 10
    MAX_FORCE = 30

    num_player_one_disks = num_tokens
    num_player_two_disks = num_tokens
    all_disks = np.array([])
    disk_idx = -1
    for i in range(num_tokens):
        disk1 = slider.Slider(center_x = rand.randint(SLIDERS_RECTTOP_LEFT_X + SLIDER_RADIUS, SLIDERS_RECTTOP_LEFT_X + SLIDERS_RECT_WIDTH - SLIDER_RADIUS), center_y = rand.randint(SLIDERS_RECT_TOP_LEFT_Y + SLIDER_RADIUS, SLIDERS_RECT_TOP_LEFT_Y + SLIDERS_RECT_HEIGHT - SLIDER_RADIUS), radius = SLIDER_RADIUS, space = SPACE, collision_type = 1, player = 0, max_speed = SPEED_TO_NUM[speed])
        disk2 = slider.Slider(center_x = rand.randint(SLIDERS_RECTTOP_LEFT_X + SLIDER_RADIUS, SLIDERS_RECTTOP_LEFT_X + SLIDERS_RECT_WIDTH - SLIDER_RADIUS), center_y = rand.randint(SLIDERS_RECT_TOP_LEFT_Y + SLIDER_RADIUS, SLIDERS_RECT_TOP_LEFT_Y + SLIDERS_RECT_HEIGHT - SLIDER_RADIUS), radius = SLIDER_RADIUS, space = SPACE, collision_type = 1, player = 1, max_speed = SPEED_TO_NUM[speed])
        all_disks = np.append(all_disks, [disk1, disk2])

    running = True
    apply_physics = False
    state = 0
    game_over = False

    SEND_BUTTON = button.Button(color = WHITE, left_corner_x = SCREEN_WIDTH/2 - 40, left_corner_y = SCREEN_HEIGHT - 80, width = 150, height = 40, font_size = 40, text = "Send")
    MENU_BUTTON = button.Button(color = WHITE, left_corner_x = 400, left_corner_y = 20, width = 150, height = 60, font_size = 30, text = "Menu")
    PLAY_AGAIN_BUTTON = button.Button(color = WHITE, left_corner_x = 600, left_corner_y = 20, width = 150, height = 60, font_size = 30, text = "Play Again")
        
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
                game_over = True
                draw_text(50, "Game is a Tie", (200, 20), WHITE, BLACK)
                MENU_BUTTON.draw(SCREEN)
                PLAY_AGAIN_BUTTON.draw(SCREEN)
            elif(num_player_one_disks == 0):
                game_over = True
                draw_text(50, "Player Two Wins", (200, 20), WHITE, BLACK)
                MENU_BUTTON.draw(SCREEN)
                PLAY_AGAIN_BUTTON.draw(SCREEN)
            elif(num_player_two_disks == 0):
                game_over = True
                draw_text(50, "Player One Wins", (200, 20), WHITE, BLACK)
                MENU_BUTTON.draw(SCREEN)
                PLAY_AGAIN_BUTTON.draw(SCREEN)
            elif(state == 0):
                draw_text(50, "Player One's Turn", (SCREEN_WIDTH / 2, 20), WHITE, BLACK)
            elif(state == 1):
                draw_text(50, "Player Two's Turn", (SCREEN_WIDTH / 2, 20), WHITE, BLACK)
        else:
            draw_text(50, "Launch Targets", (SCREEN_WIDTH / 2, 20), WHITE, BLACK)
            
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
            i -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if(SLIDERS_RECT.collidepoint(mouse_pos)):
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
                    
                elif(PLAY_AGAIN_BUTTON.is_over_mouse(mouse_pos) and game_over):
                    num_player_one_disks = num_tokens
                    num_player_two_disks = num_tokens
                    all_disks = np.array([])
                    disk_idx = -1

                    MENU_BUTTON.remove(SCREEN)
                    PLAY_AGAIN_BUTTON.remove(SCREEN)

                    for i in range(num_tokens):
                        disk1 = slider.Slider(center_x = rand.randint(SLIDERS_RECTTOP_LEFT_X + SLIDER_RADIUS, SLIDERS_RECTTOP_LEFT_X + SLIDERS_RECT_WIDTH - SLIDER_RADIUS), center_y = rand.randint(SLIDERS_RECT_TOP_LEFT_Y + SLIDER_RADIUS, SLIDERS_RECT_TOP_LEFT_Y + SLIDERS_RECT_HEIGHT - SLIDER_RADIUS), radius = SLIDER_RADIUS, space = SPACE, collision_type = 1, player = 0, max_speed = SPEED_TO_NUM[speed])
                        disk2 = slider.Slider(center_x = rand.randint(SLIDERS_RECTTOP_LEFT_X + SLIDER_RADIUS, SLIDERS_RECTTOP_LEFT_X + SLIDERS_RECT_WIDTH - SLIDER_RADIUS), center_y = rand.randint(SLIDERS_RECT_TOP_LEFT_Y + SLIDER_RADIUS, SLIDERS_RECT_TOP_LEFT_Y + SLIDERS_RECT_HEIGHT - SLIDER_RADIUS), radius = SLIDER_RADIUS, space = SPACE, collision_type = 1, player = 1, max_speed = SPEED_TO_NUM[speed])
                        all_disks = np.append(all_disks, [disk1, disk2])

                    apply_physics = False
                    state = 0
                    game_over = False
                
                elif(MENU_BUTTON.is_over_mouse(mouse_pos) and game_over):
                    return True

            elif event.type == pygame.MOUSEMOTION:
                if(disk_idx != -1 and not game_over):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

                    end_arrow_x += event.rel[0]
                    end_arrow_y += event.rel[1]
                    if(SCREEN_RECT.collidepoint(end_arrow_x, end_arrow_y + ARROWHEAD_LENGTH)):
                        disk_arrow = arrow.Arrow(start_arrow_x, start_arrow_y, end_arrow_x, end_arrow_y, RED if all_disks[disk_idx].get_player() == 0 else YELLOW)
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
    return False

def transition_screen():
	SCREEN.fill(BLACK)
	
	draw_text(font_size = 100, text = "3", center_position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), text_color = WHITE, background_color = BLACK)
	pygame.display.update()
	time.sleep(1)
	draw_text(font_size = 100, text = "3", center_position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), text_color = BLACK, background_color = BLACK)
	draw_text(font_size = 100, text = "2", center_position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), text_color = WHITE, background_color = BLACK)
	pygame.display.update()
	time.sleep(1)
	draw_text(font_size = 100, text = "2", center_position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), text_color = BLACK, background_color = BLACK)
	draw_text(font_size = 100, text = "1", center_position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), text_color = WHITE, background_color = BLACK)
	pygame.display.update()
	time.sleep(1)
	draw_text(font_size = 100, text = "1", center_position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), text_color = BLACK, background_color = BLACK)	


#Main loop to connect screens
while True:
    exit = False
    NUM_TOKENS, SPEED, ARENA_SIZE = menu()
    while not exit:
        transition_screen()
        exit = run_game(num_tokens = NUM_TOKENS, speed = SPEED, arena_size = ARENA_SIZE)