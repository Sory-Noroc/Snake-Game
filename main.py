
import sys
import pygame  # version 1.9.6
from time import sleep
from os import environ
from gui import StarterGui
from food import Food
from snake import Snake


class Game:
    width = 720
    height = 420
    difficulty = 25

    def __init__(self):
        self.gui = StarterGui(self)
        self.food = Food(self)
        self.snake = Snake(self)
        # self.setUp()
        # self.gui.launch()

    def setUp(self):
        self.x = self.gui.x
        self.y = self.gui.y
        pygame.init()
        self.fps_controller = pygame.time.Clock()
        self.score = 0
        self.game_window = None

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.width / 10, 15)
        else:
            score_rect.midtop = (self.width / 2, self.height / 1.25)
        self.game_window.blit(score_surface, score_rect)

    def game_loop(self):  # The main game loop that runs continuously
        self.gui.mw.destroy()
        self.setUp()
        pygame.display.set_caption('Snake')
        environ['SDL_VIDEO_WINDOW_POS'] = f"{self.x},{self.y}"
        self.game_window = pygame.display.set_mode((self.width, self.height))

        while True:  # The main game loop, not infinite, it stops when you lose
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Whenever a key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.snake.change_to = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.snake.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.snake.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.snake.change_to = 'RIGHT'
                    # Esc -> Create event to quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT, {}))

            self.snake.move()
            self.snake.grow(self.food)  # Snake body growing mechanism
            self.food.spawn_food()
            self.snake.draw()
            self.food.draw()
            self.snake.check_pos()  # Getting out of bounds

            try:  # The error appears when the game ends and will be ignored
                self.show_score(1, (255, 255, 255), 'consolas', 20)
                pygame.display.update()
            except pygame.error:  # This is raised by pygame not recognizing fonts
                sys.exit()
            self.fps_controller.tick(self.difficulty)  # Refresh rate

    def over(self):
        """
        Gets called when the snake runs into itself or the border
        :return: None
        """
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_label = my_font.render('YOU DIED', True, (255, 0, 0))
        game_over_rect = game_over_label.get_rect()
        game_over_rect.midtop = (self.width / 2, self.height / 4)
        self.game_window.fill((0, 0, 0))
        self.game_window.blit(game_over_label, game_over_rect)
        self.show_score(0, (255, 0, 0), 'times', 20)
        small_font = pygame.font.SysFont('times new roman', 20)
        wait_label = small_font.render('Wait a second...', True, (255, 255, 255))
        wait_rect = wait_label.get_rect()
        wait_rect.midtop = (self.width / 2, self.height / 1.1)
        self.game_window.blit(wait_label, wait_rect)
        pygame.display.flip()  # Clearing the screen for a new game
        sleep(1)
        pygame.quit()
        self.snake = Snake(self)  # For the next game
        self.food = Food(self)
        self.gui.__init__(self)
        self.gui.launch()


if __name__ == '__main__':
    game = Game()
    game.gui.launch()
