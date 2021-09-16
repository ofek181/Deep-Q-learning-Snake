import pygame
import sys
import time
from consts import PIXEL, WINDOW_WIDTH, WINDOW_HEIGHT, FPS_CONTROLLER, Color, Direction
from game_logic import Logic


class Snake(Logic):
    def __init__(self, fps: int = 10):
        pygame.init()
        pygame.display.set_caption('Snake')
        self.fps = fps
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.action = Direction.KEEP.value
        super().__init__()

    def _game_over(self):
        font = pygame.font.SysFont('times new roman', 100)
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
                        self._config_parameters()
                        self.run_game()

    def _config_parameters(self):
        self.action = Direction.KEEP.value
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        super().__init__()

    def _play_again(self):
        k_font = pygame.font.SysFont('times new roman', 60)
        k_surface = k_font.render('Press any key to continue', True, Color.WHITE.value)
        k_rect = k_surface.get_rect()
        k_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3)
        self.window.fill(Color.BLACK.value)
        self.window.blit(k_surface, k_rect)
        font = pygame.font.SysFont('times new roman', 40)
        surface = font.render('Or press escape to exit', True, Color.RED.value)
        rect = surface.get_rect()
        rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.8)
        self.window.blit(surface, rect)
        pygame.display.flip()
        time.sleep(1)
        self._wait_for_action()

    def _show_score(self):
        score_font = pygame.font.SysFont('times new roman', 50)
        surface = score_font.render('SCORE: ' + str(self.score), True, Color.WHITE.value)
        rect = surface.get_rect()
        rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.8)
        self.window.blit(surface, rect)

    def run_game(self):
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


def main():
    snake = Snake(fps=15)
    snake.run_game()


if __name__ == '__main__':
    main()
