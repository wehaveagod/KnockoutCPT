import pygame
from numpy import array

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
SCREEN = pygame.display.set_mode((640, 480))
FPS = pygame.time.Clock()

line_selection = False
all_lines = []

run = True
while run:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            line_selection = True
            start_line_x = pygame.mouse.get_pos()[0]
            start_line_y = pygame.mouse.get_pos()[1]

            end_line_x = start_line_x
            end_line_y = start_line_y

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

        elif event.type == pygame.MOUSEMOTION:
            if line_selection:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

                end_line_x += event.rel[0]
                end_line_y += event.rel[1]

                SCREEN.fill(BLACK)

                for i in range(len(all_lines)):
                    pygame.draw.line(SCREEN, WHITE, all_lines[i][0], all_lines[i][1], width = 3)

                pygame.draw.line(SCREEN, WHITE, (start_line_x, start_line_y), (end_line_x, end_line_y), width = 3)

        elif event.type == pygame.MOUSEBUTTONUP:
            line_selection = False
            pygame.draw.line(SCREEN, WHITE, (start_line_x, start_line_y), (end_line_x, end_line_y), width = 3)
            array(all_lines.append([(start_line_x, start_line_y), (end_line_x, end_line_y)]))
            pygame.display.update()
        
    pygame.display.update()
    FPS.tick(60)