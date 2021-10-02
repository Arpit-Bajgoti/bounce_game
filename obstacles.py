import random
from collections import namedtuple
import pygame
from main import TurboGame

width = 1236
height = 664
OLIVE = (181, 179, 92)
Point = namedtuple("Point", "w, h")


class Obstacles:
    def __init__(self):

        self.w = width
        self.h = height
        self.brick = None
        self.width = 80
        self.height = 30
        self.bricks = []
        self.brick_conditions = []

    def brick(self):
        x = random.randint(int(0.1 * self.w), int(0.9 * self.w))
        y = random.randint(int(0.1 * self.h), int(0.9 * self.h))
        self.brick = Point(x, y)
        return self.brick

    def draw_brick(self):
        rectangle = pygame.draw.rect(self.display, OLIVE,
                                     pygame.Rect(self.brick.w, self.brick.h, self.width, self.height))
        self.bricks.append(rectangle)
        return rectangle

    def brick_conditions(self):
        if self.ball[0] - self.radius in range(self.brick.w, self.brick.w + self.width) and self.ball[1] - self.radius in range(self.brick.w, self.brick.w - self.height) :
            self.update[1] = -self.update[1]

