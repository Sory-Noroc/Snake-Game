import numpy as np
import torch
import random
from snakeAI import GameAI, Direction
from collections import deque
from model import LinearQNet, QTrainer
from helper import plot

MAX_MEMORY = 50_000
BATCH_SIZE = 800
LR = 0.01


class Agent:
    def __init__(self):
        self.game_count = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.8  # rate of discount
        self.memory = deque(maxlen=MAX_MEMORY)  # automatically removes from left when full
        self.model = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake.body[0]
        point_l = [head.x - 20, head.y]
        point_r = [head.x + 20, head.y]
        point_u = [head.x, head.y - 20]
        point_d = [head.x, head.y + 20]

        dir_l = game.snake.direction == Direction.LEFT
        dir_r = game.snake.direction == Direction.RIGHT
        dir_u = game.snake.direction == Direction.UP
        dir_d = game.snake.direction == Direction.DOWN

        # change_pos method checks if our snake hits the border or itself, but we only need the border => False
        state = [
            # Danger straight
            (dir_r and game.snake.change_pos(point_r, False)) or
            (dir_l and game.snake.change_pos(point_l, False)) or
            (dir_u and game.snake.change_pos(point_u, False)) or
            (dir_d and game.snake.change_pos(point_d, False)),

            # Danger right
            (dir_u and game.snake.change_pos(point_r, False)) or
            (dir_d and game.snake.change_pos(point_l, False)) or
            (dir_l and game.snake.change_pos(point_u, False)) or
            (dir_r and game.snake.change_pos(point_d, False)),

            # Danger left
            (dir_d and game.snake.change_pos(point_r, False)) or
            (dir_u and game.snake.change_pos(point_l, False)) or
            (dir_r and game.snake.change_pos(point_u, False)) or
            (dir_l and game.snake.change_pos(point_d, False)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food.x < head.x,  # food left
            game.food.x > head.x,  # food right
            game.food.y < head.y,  # food up
            game.food.y > head.y  # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(self, states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(self, state, action, reward, next_state, done)

    def get_action(self, state):
        """ Random moves: Exploration combined with exploitation """
        self.epsilon = 80 - self.game_count
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = GameAI()
    while True:
        old_state = agent.get_state(game)
        final_move = agent.get_action(old_state)

        # perform move and get new state
        reward, score = game.game_loop(final_move)
        new_state = agent.get_state(game)

        # train short memory
        agent.train_short_memory(old_state, final_move, reward, new_state, True)

        # remember
        agent.remember(old_state, final_move, reward, new_state, True)

        # train long memory, plot results
        game.reset()
        agent.game_count += 1
        agent.train_long_memory()
        if (score > record):
            record = score
            # agent.model.save()

        print("Games:", agent.game_count, "Score:", score, "Record:", record)

        plot_scores.append(score)
        total_score += score
        mean_score = total_score / agent.game_count
        plot_mean_scores.append(mean_score)
        plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    train()