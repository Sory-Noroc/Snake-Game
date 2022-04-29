from snake import Direction
from enum import Enum
from main import *


class Action(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2


class SnakeAI(Snake):
    def __init__(self, context):
        super().__init__(context)

    def move_by_action(self, action):
        """
        :param action: [Straight, Right or Left]
        :return: None
        """
        rotation = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        index = rotation.index(self.direction)

        if action == Action.LEFT:
            # if we go up, change to last index, else go to left direction
            new_index = index - 1 if index > 0 else 3
            self.direction = rotation[new_index]
        elif action == Action.RIGHT:
            self.direction = rotation[(index+1) % 4]
        # If we go straight no need to change anything

        super().move()

    def check_pos(self, point=None, check_body=True):  # In case it hits itself or the window
        if point is None:
            point = self.pos

        if point[0] < 0 or point[0] > self.game.width - 10:
            # self.game.over()
            return True
        if point[1] < 0 or point[1] > self.game.height - 10:
            # self.game.over()
            return True
        if check_body:
            for block in self.body[1:]:  # Touching the snake body
                if self.pos[0] == block[0] and self.pos[1] == block[1]:
                    # self.game.over()
                    return True
        return False

    def grow(self, food):  # Adds to body length
        self.body.insert(0, list(self.pos))
        if self.pos[0] == food.pos[0] and self.pos[1] == food.pos[1]:  # If the snake touches food
            self.game.score += 1
            food.spawn = False
            reward = 10
            return reward
        else:
            self.body.pop()
            return 0


class GameAI(Game):
    width = 720
    height = 420
    difficulty = 25

    def __init__(self):
        super().__init__()
        self.reset()
        self.game_screen()

    def reset(self):
        self.snake = SnakeAI(self)
        self.score = 0
        self.food = Food(self)
        self.frame_count = 0

    def game_screen(self):
        self.gui.mw.destroy()
        self.setUp()
        pygame.display.set_caption('Snake')
        environ['SDL_VIDEO_WINDOW_POS'] = f"{self.x},{self.y}"
        self.game_window = pygame.display.set_mode((self.width, self.height))

    def game_loop(self, action=None):  # The main game loop that runs continuously
        self.frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.snake.move()

        reward = self.snake.grow(self.food)  # If snake eats, gets 10 reward, else 0
        game_over = self.snake.check_pos() or self.frame_count > 100 * len(self.snake.body)

        if game_over:
            reward = -10
            return reward, self.score
        self.food.spawn_food()
        self.snake.draw()
        self.food.draw()

        try:  # The error appears when the game ends and will be ignored
            self.show_score(1, (255, 255, 255), 'consolas', 20)
            pygame.display.flip()
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
    game.game_screen()
    while True:  # The main game loop, not infinite, it stops when you lose
        reward, score = game.game_loop()
