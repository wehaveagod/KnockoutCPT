import pygame

WHITE = (255, 255, 255)

class Arrow:
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int, arrow_color):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = arrow_color

    def draw(self, window):
        if(self.has_length()):
            pygame.draw.line(window, self.color, (self.start_x, self.start_y), (self.end_x, self.end_y), width = 3)
    
    def has_length(self):
        return not (self.start_x == self.end_x and self.start_y == self.end_y)

        