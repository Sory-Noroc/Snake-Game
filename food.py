
from random import randrange
import pygame


class Food:
    def __init__(self, game):  # Spawns food randomly on the map
        self.game = game
        self.pos = [randrange(1, (game.width // 10)) * 10, randrange(1, (game.height // 10)) * 10]
        self.spawn = True

    def draw(self):
        pygame.draw.rect(self.game.game_window, (255, 255, 255), pygame.Rect(self.pos[0], self.pos[1], 10, 10))

    def spawn_food(self):
        if not self.spawn:
            self.pos = [randrange(1, (self.game.width // 10)) * 10, randrange(1, (self.game.height // 10)) * 10]
            self.spawn = True
