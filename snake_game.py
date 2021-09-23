import pygame
import numpy as np
import sys
import time
from consts import PIXEL, WINDOW_WIDTH, WINDOW_HEIGHT, FPS_CONTROLLER, Color, Direction
from game_logic import Logic


class Snake(Logic):
    def __init__(self, fps: int = 10):
        super().__init__()
        pygame.init()
        pygame.display.set_caption('Snake')
        self.fps = fps
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.action = Direction.KEEP.value

    def _game_over(self):
        font = pygame.font.SysFont('times new roman', WINDOW_WIDTH*WINDOW_HEIGHT//1500)
        surface = font.render('GAME OVER', True, Color.RED.value)
        rect = surface.get_rect()
        rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3.2)
        self.window.fill(Color.BLACK.value)
        self.window.blit(surface, rect)
        self._show_score()
        pygame.display.flip()
        time.sleep(3)
        self._play_again()

    def _wait_for_action(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    else:
                        self.config_parameters()
                        self.play_game()

    def config_parameters(self):
        super().__init__()
        self.action = Direction.KEEP.value
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def _play_again(self):
        k_font = pygame.font.SysFont('times new roman', WINDOW_WIDTH*WINDOW_HEIGHT//2500)
        k_surface = k_font.render('Press any key to continue', True, Color.WHITE.value)
        k_rect = k_surface.get_rect()
        k_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3)
        self.window.fill(Color.BLACK.value)
        self.window.blit(k_surface, k_rect)
        font = pygame.font.SysFont('times new roman',  WINDOW_WIDTH*WINDOW_HEIGHT//2500)
        surface = font.render('Or press escape to exit', True, Color.RED.value)
        rect = surface.get_rect()
        rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.8)
        self.window.blit(surface, rect)
        pygame.display.flip()
        time.sleep(1)
        self._wait_for_action()

    def _show_score(self):
        score_font = pygame.font.SysFont('times new roman', WINDOW_WIDTH*WINDOW_HEIGHT//1800)
        surface = score_font.render('SCORE: ' + str(self.score), True, Color.WHITE.value)
        rect = surface.get_rect()
        rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.8)
        self.window.blit(surface, rect)

    def human_play(self):
        self.move(self.action)
        self.grow()
        self.spawn_food()
        self.window.fill(Color.BLACK.value)
        for position in self.snake_body:
            pygame.draw.rect(self.window, Color.GREEN.value, pygame.Rect(position[0], position[1],
                                                                         PIXEL, PIXEL))
        pygame.draw.rect(self.window, Color.WHITE.value, pygame.Rect(self.food_position[0],
                                                                     self.food_position[1], PIXEL, PIXEL))
        if self.is_game_over():
            self._game_over()

        pygame.display.update()
        FPS_CONTROLLER.tick(self.fps)

    def ai_play(self, action):
        self.move(action)
        self.grow()
        self.spawn_food()
        self.window.fill(Color.BLACK.value)
        for position in self.snake_body:
            pygame.draw.rect(self.window, Color.GREEN.value, pygame.Rect(position[0], position[1],
                                                                         PIXEL, PIXEL))
        pygame.draw.rect(self.window, Color.WHITE.value, pygame.Rect(self.food_position[0],
                                                                     self.food_position[1], PIXEL, PIXEL))
        pygame.display.update()
        FPS_CONTROLLER.tick(self.fps)

    def get_state_in_numpy_array(self) -> np.array:
        state = np.zeros((WINDOW_WIDTH // PIXEL, WINDOW_HEIGHT // PIXEL))

        for block in self.snake_body:
            state[block[0] // PIXEL, block[1] // PIXEL] = 1  # body

        state[self.snake_position[0] // PIXEL, self.snake_position[1] // PIXEL] = 2  # head
        state[self.food_position[0] // PIXEL, self.food_position[1] // PIXEL] = 3  # food
        return state

    def play_game(self):
        while True:
            self.action = Direction.KEEP.value
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.action = Logic.take_action(event)
                    if self.action == Direction.ESCAPE.value:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
            self.human_play()
            state = self.get_state_in_numpy_array()
            print(state)


def main():
    snake = Snake(fps=10)
    snake.play_game()


if __name__ == '__main__':
    main()
