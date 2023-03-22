import pygame
import math

WHITE = (255, 255, 255)
ARROWHEAD_LENGTH = 10

def add_tuples(t1, t2):
    return tuple(map(sum, zip(t1, t2)))

class Arrow:
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int, arrow_color):
        self.start_coord = (start_x, start_y)
        self.end_coord = (end_x, end_y)
        self.color = arrow_color

    def draw(self, window):
        if(self.has_length()):
            angle = math.atan2(self.end_coord[1] - self.start_coord[1], self.end_coord[0] - self.start_coord[0])

            arrow_side_1 = (-ARROWHEAD_LENGTH * math.sin(angle - math.pi), -ARROWHEAD_LENGTH * math.cos(angle))
            arrow_side_2 = (ARROWHEAD_LENGTH * math.sin(angle - math.pi), ARROWHEAD_LENGTH * math.cos(angle))
            arrow_front = (ARROWHEAD_LENGTH * math.cos(angle), ARROWHEAD_LENGTH * math.sin(angle))

            arrow_head_coords = [add_tuples(self.end_coord, arrow_side_1), 
                                  add_tuples(self.end_coord, arrow_side_2), 
                                  add_tuples(self.end_coord, arrow_front)]

            pygame.draw.line(window, self.color, self.start_coord, self.end_coord, width = 3)
            pygame.draw.polygon(window, self.color, arrow_head_coords)
    
    def has_length(self):
        return not (self.start_coord[0] == self.end_coord[0] and self.start_coord[1] == self.end_coord[1])
    
    def get_start_coord(self):
        return self.start_coord
    
    def get_end_coord(self):
        return self.end_coord
        


        