# SNAKE Game by Sory

import sys
import pygame  # version 1.9.6
import tkinter  # version 8.6
from time import sleep
from random import randrange
from os import environ


class Snake:
    def __init__(self, game):  # The initial stats
        self.game = game
        self.pos = [100, 50]
        self.body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def draw(self):  # Draws the Snake back
        self.game.game_window.fill((0, 0, 0))
        for pos in self.body:
            pygame.draw.rect(self.game.game_window, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))

    def grow(self):  # Adds to body length
        self.body.insert(0, list(self.pos))
        if self.pos[0] == food.pos[0] and self.pos[1] == food.pos[1]:  # If the snake touches food
            game.score += 1
            food.spawn = False
        else:
            self.body.pop()

    def check_pos(self):  # In case it hits itself or the window
        if self.pos[0] < 0 or self.pos[0] > game.width - 10:
            game.over()
        if self.pos[1] < 0 or self.pos[1] > game.height - 10:
            game.over()
        for block in self.body[1:]:  # Touching the snake body
            if self.pos[0] == block[0] and self.pos[1] == block[1]:
                game.over()

    def move(self):
        # Making sure the snake cannot move in the opposite direction instantaneously
        if snake.change_to == 'UP' and snake.direction != 'DOWN':
            snake.direction = 'UP'
        if snake.change_to == 'DOWN' and snake.direction != 'UP':
            snake.direction = 'DOWN'
        if snake.change_to == 'LEFT' and snake.direction != 'RIGHT':
            snake.direction = 'LEFT'
        if snake.change_to == 'RIGHT' and snake.direction != 'LEFT':
            snake.direction = 'RIGHT'
        # Moving the snake
        if self.direction == 'UP':
            self.pos[1] -= 10
        if self.direction == 'DOWN':
            snake.pos[1] += 10
        if self.direction == 'LEFT':
            snake.pos[0] -= 10
        if self.direction == 'RIGHT':
            snake.pos[0] += 10
