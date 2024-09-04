import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load and resize images
def load_and_resize_image(path, width, height):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (width, height))

# Define image dimensions
PIPE_WIDTH, PIPE_HEIGHT = 70, 400

# Load pipe images
PIPE_IMAGE = load_and_resize_image('Sub(flappybird)/pipe.png', PIPE_WIDTH, PIPE_HEIGHT)
PIPE_IMAGE_FLIPPED = pygame.transform.flip(PIPE_IMAGE, False, True)

# Pipe drawing function
def draw_pipe(x, y, flipped=False):
    if flipped:
        SCREEN.blit(PIPE_IMAGE_FLIPPED, (x, y))
    else:
        SCREEN.blit(PIPE_IMAGE, (x, y))

# Main game loop
def game_loop():
    pipe_x = WIDTH  # Start pipes off-screen to the right
    pipe_y = random.randint(-150, 150)
    pipe_gap = 200  # Gap between upper and lower pipes
    pipe_velocity = 5
    clock = pygame.time.Clock()
    running = True

    while running:
        SCREEN.fill((255, 255, 255))  # Clear screen with white background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move pipes
        pipe_x -= pipe_velocity

        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_y = random.randint(-150, 150)

        # Draw the lower pipe (regular)
        draw_pipe(pipe_x, HEIGHT // 2 + pipe_gap // 2 + pipe_y)

        # Draw the upper pipe (flipped)
        draw_pipe(pipe_x, HEIGHT // 2 - pipe_gap // 2 - PIPE_HEIGHT + pipe_y, flipped=True)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
