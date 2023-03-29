import pymunk
import pygame
import math
import arrow

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

MAX_SPEED = 300

WIDTH = 600
HEIGHT = 600


class Slider:
    def __init__(self, center_x: int, center_y: int, radius: int, space: pymunk.Space, collision_type: int, player: int, max_speed: int, velocity_vector = arrow.Arrow(0, 0, 0, 0, BLUE)):
        self.body = pymunk.Body()
        self.body.position = (center_x, center_y)
        self.body.velocity = 0, 0

        self.radius = radius
        self.shape = pymunk.Circle(self.body, self.radius)
        self.disk_color = RED if player == 0 else YELLOW

        self.shape.elasticity = 1
        self.shape.density = 1
        self.velocity_vector = velocity_vector
        self.shape.collision_type = collision_type

        self.space = space
        self.space.add(self.body, self.shape)

        self.player = player
        self.max_speed = max_speed

    def draw(self, window, draw_arrow: bool):
        pygame.draw.circle(window, self.disk_color, self.body.position, self.radius)
        if(draw_arrow):
            self.velocity_vector.draw(window)

    def is_over_mouse(self, pos: tuple[int, int]):
        return math.hypot(pos[0] - self.body.position[0], pos[1] - self.body.position[1]) < self.radius
    
    def set_vector(self, new_vector: arrow.Arrow):
        self.velocity_vector = new_vector

    def set_velocity(self):
        self.body.velocity = (self.max_speed * (self.velocity_vector.get_end_coord()[0] - self.velocity_vector.get_start_coord()[0]) / WIDTH, 
                              self.max_speed* (self.velocity_vector.get_end_coord()[1] - self.velocity_vector.get_start_coord()[1]) / HEIGHT)
        
    def get_center_coord(self):
        return self.body.position
    
    def get_body(self):
        return self.body
    
    def get_player(self):
        return self.player