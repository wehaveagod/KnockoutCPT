import pymunk
import pygame
import math
import arrow

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

class Disk:
    def __init__(self, center_x: int, center_y: int, radius: int, disk_color, vector = arrow.Arrow(0, 0, 0, 0, BLUE)):
        self.body = pymunk.Body()
        self.body.position = center_x, center_y
        self.radius = radius
        self.shape = pymunk.Circle(self.body, self.radius)
        self.disk_color = disk_color

        self.shape.elasticity = 1
        self.shape.density = 1
        self.vector = vector
    
    def draw(self, window):
        pygame.draw.circle(window, self.disk_color, self.body.position, self.radius)
        self.vector.draw(window)

    def is_over_mouse(self, pos: tuple[int, int]):
        return math.hypot(pos[0] - self.body.position[0], pos[1] - self.body.position[1]) < self.radius
    
    def set_vector(self, window, new_vector: arrow.Arrow):
        window.fill(BLACK)
        self.vector = new_vector
        self.draw(window)
    
    def clear_vector(self, window):
        self.vector = arrow.Arrow(0, 0, 0, 0)
        self.draw(window)

    def get_center_x(self):
        return self.body.position[0]
    
    def get_center_y(self):
        return self.body.position[1]
    