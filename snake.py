from enum import Enum

import pygame  # version 1.9.6


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Snake:

    def __init__(self, game):  # The initial stats
        self.game = game
        self.pos = [100, 50]
        self.body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.direction = Direction.RIGHT
        self.change_to = self.direction

    def draw(self):  # Draws the Snake back
        self.game.game_window.fill((0, 0, 0))
        for pos in self.body:
            pygame.draw.rect(self.game.game_window, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))

    def grow(self, food):  # Adds to body length
        self.body.insert(0, list(self.pos))
        if self.pos[0] == food.pos[0] and self.pos[1] == food.pos[1]:  # If the snake touches food
            self.game.score += 1
            food.spawn = False
        else:
            self.body.pop()

    def check_pos(self):  # In case it hits itself or the window
        if self.pos[0] < 0 or self.pos[0] > self.game.width - 10:
            self.game.over()
        if self.pos[1] < 0 or self.pos[1] > self.game.height - 10:
            self.game.over()
        for block in self.body[1:]:  # Touching the snake body
            if self.pos[0] == block[0] and self.pos[1] == block[1]:
                self.game.over()

    def move(self):
        # Making sure the snake cannot move in the opposite direction instantaneously
        if self.change_to == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        if self.change_to == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        if self.change_to == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        if self.change_to == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        # Moving the snake
        if self.direction == Direction.UP:
            self.pos[1] -= 10
        if self.direction == Direction.DOWN:
            self.pos[1] += 10
        if self.direction == Direction.LEFT:
            self.pos[0] -= 10
        if self.direction == Direction.RIGHT:
            self.pos[0] += 10
