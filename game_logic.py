import pygame
import random
from consts import PIXEL, Direction


class Logic:
    def __init__(self, snake_position: list, snake_body: list, food_position: list,
                 score: int, food_spawn: bool, direction: str):
        self.snake_position = snake_position
        self.snake_body = snake_body
        self.food_position = food_position
        self.score = score
        self.food_spawn = food_spawn
        self.direction = direction

    def _move_position(self, action: str):
        problem = True
        if action == Direction.UP.value and self.direction != Direction.DOWN.value:
            self.direction = Direction.UP.value
            self.snake_position[1] -= PIXEL
            problem = False
        if action == Direction.DOWN.value and self.direction != Direction.UP.value:
            self.direction = Direction.DOWN.value
            self.snake_position[1] += PIXEL
            problem = False
        if action == Direction.LEFT.value and self.direction != Direction.RIGHT.value:
            self.direction = Direction.LEFT.value
            self.snake_position[0] -= PIXEL
            problem = False
        if action == Direction.RIGHT.value and self.direction != Direction.LEFT.value:
            self.direction = Direction.RIGHT.value
            self.snake_position[0] += PIXEL
            problem = False

        if problem:
            if self.direction == Direction.DOWN.value:
                self.snake_position[1] += PIXEL
            if self.direction == Direction.UP.value:
                self.snake_position[1] -= PIXEL
            if self.direction == Direction.LEFT.value:
                self.snake_position[0] -= PIXEL
            if self.direction == Direction.RIGHT.value:
                self.snake_position[0] += PIXEL

    def _grow_if_food_eaten(self):
        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position == self.food_position:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

    def _randomly_spawn_food(self, width: int, height: int):
        if not self.food_spawn:
            self.food_position = [random.randrange(1, (width // PIXEL)) * PIXEL,
                                  random.randrange(1, (height // PIXEL)) * PIXEL]
        self.food_spawn = True

    def move(self, action: str):
        self._move_position(action)

    def grow(self):
        self._grow_if_food_eaten()

    def spawn_food(self, width: int, height: int):
        self._randomly_spawn_food(width, height)

    def is_game_over(self, width: int, height: int) -> bool:
        game_over = False
        if self.snake_position[0] < 0 or self.snake_position[0] >= width:
            game_over = True
        if self.snake_position[1] < 0 or self.snake_position[1] >= height:
            game_over = True
        for block in self.snake_body[1:]:
            if self.snake_position == block:
                game_over = True
        return game_over

    @staticmethod
    def take_action(event: pygame.event) -> str:
        action = Direction.KEEP.value
        if event.key == pygame.K_UP or event.key == ord('w'):
            action = Direction.UP.value
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            action = Direction.DOWN.value
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            action = Direction.LEFT.value
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            action = Direction.RIGHT.value
        if event.key == pygame.K_ESCAPE:
            action = Direction.ESCAPE.value
        return action




