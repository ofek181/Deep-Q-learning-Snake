import pygame
from enum import Enum

PIXEL = 10

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 480
FPS_CONTROLLER = pygame.time.Clock()


class Color(Enum):
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)


class Direction(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    KEEP = 'KEEP'
    ESCAPE = 'ESCAPE'
