import pygame
import sys
import random
import json

# Initialize pygame and the mixer
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load and resize images
def load_and_resize_image(path, width, height):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (width, height))

# Define image dimensions
BIRD_WIDTH, BIRD_HEIGHT = 40, 40
PIPE_WIDTH, PIPE_HEIGHT = 70, 400
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 600, 600  

# Load images
BIRD_IMAGES = [
    load_and_resize_image('Sub(flappybird)/bird1.png', BIRD_WIDTH, BIRD_HEIGHT),
    load_and_resize_image('Sub(flappybird)/bird2.png', BIRD_WIDTH, BIRD_HEIGHT)
]
PIPE_IMAGE = load_and_resize_image('Sub(flappybird)/pipe.png', PIPE_WIDTH, PIPE_HEIGHT)
PIPE_IMAGE_FLIPPED = pygame.transform.flip(PIPE_IMAGE, False, True)
BACKGROUND_IMAGE = load_and_resize_image('Sub(flappybird)/background.jpg', BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
START_SCREEN_BACKGROUND_IMAGE = load_and_resize_image('Sub(flappybird)/background.jpg', WIDTH, HEIGHT)

# Load sound
hit_sound = pygame.mixer.Sound('dead_sound.wav')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bird settings
bird_x, bird_y = WIDTH // 4, HEIGHT // 2
bird_velocity = 0
gravity = 1
fly_height = -10

# Pipe settings
pipe_velocity = 10
pipe_gap = 200

# Font
font = pygame.font.SysFont(None, 36)

def draw_background():
    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))

def draw_bird(x, y, frame):
    SCREEN.blit(BIRD_IMAGES[frame], (x, y))

def draw_pipe(x, y, flipped=False):
    if flipped:
        SCREEN.blit(PIPE_IMAGE_FLIPPED, (x, y))
    else:
        SCREEN.blit(PIPE_IMAGE, (x, y))

def display_message(text, color, x, y):
    screen_text = font.render(text, True, color)
    SCREEN.blit(screen_text, [x, y])

def initialize_game():
    global bird_y, bird_velocity
    bird_y = HEIGHT // 2
    bird_velocity = 0
    return WIDTH, random.randint(-150, 150), 0

# File to store the high score
HIGH_SCORE_FILE = 'high_score.json'

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('high_score', 0)
    except FileNotFoundError:
        return 0

def save_high_score(high_score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump({'high_score': high_score}, f)

def show_start_screen():
    SCREEN.blit(START_SCREEN_BACKGROUND_IMAGE, (0, 0))
    display_message("Press ANY key to start", BLACK, WIDTH // 4, HEIGHT // 2)
    pygame.display.update()

def game_loop():
    global bird_y, bird_velocity

    # Load the high score from file
    high_score = load_high_score()

    # Show the start screen
    show_start_screen()
    
    # Wait for the player to press a key to start the game
    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                start_game = True

    # Initialize game variables
    pipe_x, pipe_y, score = initialize_game()

    clock = pygame.time.Clock()
    frame_count = 0
    bird_frame = 0
    running = True
    game_over = False

    while running:
        draw_background()  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird_velocity = fly_height
                if event.key == pygame.K_SPACE and game_over:
                    pipe_x, pipe_y, score = initialize_game()
                    game_over = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # Bird mechanics
            bird_velocity += gravity
            bird_y += bird_velocity
            draw_bird(bird_x, bird_y, bird_frame)

            # Pipe mechanics
            pipe_x -= pipe_velocity

            if pipe_x < -PIPE_WIDTH:
                pipe_x = WIDTH
                pipe_y = random.randint(-150, 150)
                score += 1

            # Draw the lower pipe (regular)
            draw_pipe(pipe_x, HEIGHT // 2 + pipe_gap // 2 + pipe_y)

            # Draw the upper pipe (flipped)
            draw_pipe(pipe_x, HEIGHT // 2 - pipe_gap // 2 - PIPE_HEIGHT + pipe_y, flipped=True)

            # Check for border collision
            if bird_y > HEIGHT - BIRD_HEIGHT or bird_y < 0:
                game_over = True
                if hit_sound:
                    hit_sound.play()
                    
            # Check for collision with pipes
            if bird_x + BIRD_WIDTH > pipe_x and bird_x < pipe_x + PIPE_WIDTH:
                if bird_y < HEIGHT // 2 - pipe_gap // 2 + pipe_y or bird_y + BIRD_HEIGHT > HEIGHT // 2 + pipe_gap // 2 + pipe_y:
                    game_over = True
                    if hit_sound:
                        hit_sound.play()

            # Update bird frame for animation
            frame_count += 1
            if frame_count % 10 == 0:  # Change frame every 10 ticks
                bird_frame = (bird_frame + 1) % len(BIRD_IMAGES)

        if game_over:
            if score > high_score:
                high_score = score
                save_high_score(high_score)

            display_message(f'Game Over! Final Score: {score}', BLACK, WIDTH // 6, HEIGHT // 2)
            display_message(f'High Score: {high_score}', BLACK, WIDTH // 6, HEIGHT // 2 + 50)
            display_message('Press SPACE to Restart', BLACK, WIDTH // 4, HEIGHT // 2 + 100)
        else:
            display_message(f'Score: {score}', BLACK, 10, 10)
            display_message(f'High Score: {high_score}', BLACK, 10, 50)

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    game_loop()
