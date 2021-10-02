import pygame
from enum import Enum
from collections import namedtuple
import keyboard
import time
import random

# 1536 x 864 is the current screen resolution of my pc
pygame.init()
radius = 10
width = 836
height = 664
block_size = 20

# rgb colors
DARK_GREEN = (0, 100, 0)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
font = pygame.font.SysFont('arial', 25)


class Direction(Enum):
    LEFT = 1
    RIGHT = 2


Point = namedtuple("Point", "w, h")
color_dict = {1: DARK_GREEN, 0: GREEN}


class TurboGame:
    def __init__(self, w=width, h=height):
        self.w = w
        self.h = h
        self.w_initial = int(0.25 * self.w)
        self.h_initial = int(0.9 * self.h)
        self.counter = 3
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Turbo")
        self.score = 0
        self.bat = None
        self.update_bat()
        self.direction = None
        self.ball = None
        self._place_ball()
        self.game_over = False
        self.update = [6, 6]
        self.radius = radius
        self.width = 120
        self.height = 30
        self.lst = []
        self.stone = []
        self.bat_length = 60
        self.counter = 5

    def update_bat(self):
        self.bat = [Point(self.w_initial, self.h_initial),
                    Point(int(self.w * 0.2), int(0.01 * self.h))]

    def play_step(self):
        # 1. collect user input
        if keyboard.is_pressed("left arrow"):
            self.direction = Direction.LEFT
        elif keyboard.is_pressed("right arrow"):
            self.direction = Direction.RIGHT

        self.update_bat()
        self.update_ball()
        # self.stone_conditions()
        self._move(self.direction)
        self.direction = None

        # 2. update ui
        self._update_ui()
        return self.game_over, self.score

    def _place_ball(self):
        x = random.randint(40, self.w)
        y = random.randint(100, int(0.5 * self.h_initial))
        self.ball = [x, y]

    def _update_ui(self):
        self.display.fill(BLACK)

        pygame.draw.rect(self.display, BLUE1,
                         pygame.Rect(self.bat[0].w, self.bat[0].h, self.bat[1].w, 30))

        pygame.draw.circle(self.display, RED, tuple(self.ball), self.radius)

        self.draw_brick()
        text = font.render("Score: " + str(self.score), True, MAGENTA)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        if direction == Direction.RIGHT and self.w_initial < (self.w - self.bat[1].w - 20):
            self.w_initial += block_size
        elif direction == Direction.LEFT and self.w_initial > 10:
            self.w_initial -= block_size

    def update_ball(self):
        # ball hitting bat
        if (self.ball[1] + self.radius) > self.h_initial - 10:
            if (self.ball[0] - self.radius > self.w_initial - 10) and self.ball[0] + self.radius < self.w_initial + \
                    self.bat[1].w + 10:
                self.update[1] = random.randint(6, 10)
                self.update[1] = -self.update[1]
                self.score += 10
            else:
                self.game_over = True
        # ball hitting boundaries
        elif self.ball[0] + self.radius > self.w:
            self.update[0] = -self.update[0]
            # self.update[0] = random.randint(5, 10)
        elif self.ball[1] + self.radius < 20:
            self.update[1] = -self.update[1]
            self.update[1] = random.randint(5, 10)
        elif self.ball[0] + self.radius < 20:
            self.update[0] = -self.update[0]
            self.update[0] = random.randint(5, 10)
        self.stone_conditions()
        # updating ball at each while loop
        self.ball[0] += self.update[0]
        self.ball[1] += self.update[1]

    # TODO this code for bricks

    def brick(self):
        for i in range(30, self.w - self.width - 10, self.width + 10):
            for j in range(10, self.h - (self.height * 5), self.height + 10):
                x = i
                y = j
                z = [x, y]
                self.stone.append(z)

    def draw_brick(self):
        for value in self.lst:
            pygame.draw.rect(self.display, color_dict[value[2]],
                             pygame.Rect(value[0], value[1], self.width, self.height))

    def stone_conditions(self):
        for value in self.lst:
            if value[0] < (self.ball[0] - self.radius) < (value[0] + self.width) and \
                    value[1] + 20 > (
                    self.ball[1] - self.radius) > (value[1] - self.height + 10):
                self.update[1] = -self.update[1]
                x = self.lst.index(value)
                if value[2]:
                    value[2] -= 1
                    self.score += 5
                else:
                    self.score += 10
                    self.lst.pop(x)
                    self.counter -= 1


if __name__ == '__main__':
    game = TurboGame()
    # game loop
    game.brick()
    game.lst = random.sample(game.stone, random.randint(5, 8))
    for val in game.lst:
        val.append(random.randint(0, 1))
    while True:
        if game.counter == 3:
            num = random.randint(2, 4)
            add = random.sample(game.stone, num)
            for val in add:
                val.append(random.randint(0, 1))
            game.lst.extend(add)
            game.counter = 3 + num
        game_over, score = game.play_step()
        if game_over:
            break
        time.sleep(0.03)
    print('Final Score', score)

    pygame.quit()
