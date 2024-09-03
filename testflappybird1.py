import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bird settings
BIRD_WIDTH, BIRD_HEIGHT = 40, 40
bird_x, bird_y = WIDTH // 4, HEIGHT // 2
bird_velocity = 0
gravity = 0.5
fly_height = -10

# Pipe settings
PIPE_WIDTH = 70
PIPE_HEIGHT = 400
pipe_velocity = 5
pipe_gap = 200

# Font
font = pygame.font.SysFont(None, 36)

def draw_bird(x, y):
    pygame.draw.rect(SCREEN, BLACK, (x, y, BIRD_WIDTH, BIRD_HEIGHT))

