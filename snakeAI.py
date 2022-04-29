
from main import *


class GameAI(Game):
    width = 720
    height = 420
    difficulty = 25

    def __init__(self):
        super().__init__()
        self.game_screen()

    def reset(self):
        self.snake = Snake(self)
        self.score = 0
        self.food = Food(self)

    def game_screen(self):
        self.gui.mw.destroy()
        self.setUp()
        pygame.display.set_caption('Snake')
        environ['SDL_VIDEO_WINDOW_POS'] = f"{self.x},{self.y}"
        self.game_window = pygame.display.set_mode((self.width, self.height))

    def game_loop(self):  # The main game loop that runs continuously
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

    def over(self):  # Game Over
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


if __name__ == '__main__':
    game = GameAI()
    while True:  # The main game loop, not infinite, it stops when you lose
        game.game_loop()
