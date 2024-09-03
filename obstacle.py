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
fall_speed = 10

# Pipe settings
PIPE_WIDTH = 70
PIPE_HEIGHT = 400
pipe_velocity = 5
pipe_gap = 200

# Font
font = pygame.font.SysFont(None, 36)

def draw_bird(x, y):
    pygame.draw.rect(SCREEN, BLACK, (x, y, BIRD_WIDTH, BIRD_HEIGHT))

def draw_pipe(x, y, width, height):
    pygame.draw.rect(SCREEN, RED, (x, y, width, height))

def display_message(text, color, x, y):
    screen_text = font.render(text, True, color)
    SCREEN.blit(screen_text, [x, y])

def game_loop():
    global bird_y, bird_velocity

    # Pipe settings
    pipe_x = WIDTH
    pipe_y = random.randint(-150, 150)  # Random pipe position

    clock = pygame.time.Clock()
    score = 0

    running = True
    while running:
        SCREEN.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird_velocity = fly_height
                if event.key == pygame.K_DOWN:
                    bird_velocity = fall_speed

        # Bird mechanics
        bird_velocity += gravity
        bird_y += bird_velocity
        
        draw_bird(bird_x, bird_y)

        # Pipe mechanics
        pipe_x -= pipe_velocity

        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_y = random.randint(-150, 150)
            score += 1

        draw_pipe(pipe_x, HEIGHT // 2 + pipe_gap // 2 + pipe_y, PIPE_WIDTH, PIPE_HEIGHT)
        draw_pipe(pipe_x, HEIGHT // 2 - pipe_gap // 2 - PIPE_HEIGHT + pipe_y, PIPE_WIDTH, PIPE_HEIGHT)

        # Check for collision
        if bird_y > HEIGHT or bird_y < 0:
            display_message('Game Over', BLACK, WIDTH // 3, HEIGHT // 2)
            pygame.display.update()
            pygame.time.delay(2000)
            game_loop()

        if bird_x + BIRD_WIDTH > pipe_x and bird_x < pipe_x + PIPE_WIDTH:
            if bird_y < HEIGHT // 2 - pipe_gap // 2 + pipe_y or bird_y + BIRD_HEIGHT > HEIGHT // 2 + pipe_gap // 2 + pipe_y:
                display_message('Game Over', BLACK, WIDTH // 3, HEIGHT // 2)
                pygame.display.update()
                pygame.time.delay(2000)
                game_loop()

        display_message(f'Score: {score}', BLACK, 10, 10)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    game_loop()
