import pymunk
import pygame
import math
import arrow

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
MAX_SPEED = 100

WIDTH = 600
HEIGHT = 600


class Slider:
    def __init__(self, center_x: int, center_y: int, radius: int, disk_color, space: pymunk.Space, velocity_vector = arrow.Arrow(0, 0, 0, 0, BLUE)):
        self.body = pymunk.Body()
        self.body.position = (center_x, center_y)
        self.body.velocity = 0, 0

        self.radius = radius
        self.shape = pymunk.Circle(self.body, self.radius)
        self.disk_color = disk_color

        self.shape.elasticity = 1
        self.shape.density = 1
        self.velocity_vector = velocity_vector

        self.space = space
        self.space.add(self.body, self.shape)

    def draw(self, window):
        pygame.draw.circle(window, self.disk_color, self.body.position, self.radius)
        self.velocity_vector.draw(window)

    def is_over_mouse(self, pos: tuple[int, int]):
        return math.hypot(pos[0] - self.body.position[0], pos[1] - self.body.position[1]) < self.radius
    
    def set_vector(self, new_vector: arrow.Arrow):
        self.velocity_vector = new_vector

    def set_velocity(self):
        self.body.velocity = (MAX_SPEED * (self.velocity_vector.get_end_coord()[0] - self.velocity_vector.get_start_coord()[0]) / WIDTH, 
                              MAX_SPEED * (self.velocity_vector.get_end_coord()[1] - self.velocity_vector.get_start_coord()[1]) / HEIGHT)
        
    def get_center_x(self):
        return self.body.position[0]
    
    def get_center_y(self):
        return self.body.position[1]