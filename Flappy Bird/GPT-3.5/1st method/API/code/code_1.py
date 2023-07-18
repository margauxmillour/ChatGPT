import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set the dimensions of the game window
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Load assets
ASSETS_PATH = 'assets'
BACKGROUND_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, 'background.png'))
BIRD_IMAGES = [pygame.image.load(os.path.join(ASSETS_PATH, 'bird1.png')),
               pygame.image.load(os.path.join(ASSETS_PATH, 'bird2.png')),
               pygame.image.load(os.path.join(ASSETS_PATH, 'bird3.png'))]
BASE_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, 'base.png'))
PIPE_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, 'pipe.png'))
GAME_FONT = pygame.font.Font(None, 40)

# Set up the game window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Flappy Bird')

# Set up game variables
clock = pygame.time.Clock()
base_x = 0
bird_x = 50
bird_y = int(WINDOW_HEIGHT / 2)
gravity = 0.25
bird_movement = 0
score = 0
highscore = 0

# Function to generate new pipes
def generate_pipes():
    pipe_height = random.randint(100, 300)
    pipe_top = PIPE_IMAGE.get_rect(midbottom=(WINDOW_WIDTH + 100, pipe_height))
    pipe_bottom = PIPE_IMAGE.get_rect(midtop=(WINDOW_WIDTH + 100, pipe_height - 150))
    return pipe_top, pipe_bottom

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

# Function to draw pipes on the screen
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= WINDOW_HEIGHT:
            window.blit(PIPE_IMAGE, pipe)
        else:
            flipped_pipe = pygame.transform.flip(PIPE_IMAGE, False, True)
            window.blit(flipped_pipe, pipe)

# Function to check for collisions
def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= -50 or bird_rect.bottom >= WINDOW_HEIGHT - 90:
        return True
    return False

# Function to update score
def update_score(current_score):
    score_text = GAME_FONT.render(f'Score: {current_score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH / 2, 50))
    window.blit(score_text, score_rect)

# Function to update high score
def update_highscore(current_highscore):
    highscore_text = GAME_FONT.render(f'Highscore: {current_highscore}', True, (255, 255, 255))
    highscore_rect = highscore_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    window.blit(highscore_text, highscore_rect)

# Game loop
running = True
while running:
    # Set up background image
    window.blit(BACKGROUND_IMAGE, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 8

    # Move bird
    bird_movement += gravity
    bird_y += bird_movement

    # Set up base image
    base_x -= 1
    window.blit(BASE_IMAGE, (base_x, WINDOW_HEIGHT - 90))
    window.blit(BASE_IMAGE, (base_x + WINDOW_WIDTH, WINDOW_HEIGHT - 90))
    if base_x <= -WINDOW_WIDTH:
        base_x = 0

    # Set up bird image
    current_bird = BIRD_IMAGES[int(pygame.time.get_ticks() / 100) % 3]
    bird_rect = current_bird.get_rect(center=(bird_x, bird_y))
    window.blit(current_bird, bird_rect)

    # Generate and move pipes
    if pygame.time.get_ticks() % 2000 == 0:
        pipes = generate_pipes()
    pipes = move_pipes(pipes)
    draw_pipes(pipes)

    # Check for collisions
    if check_collisions(pipes):
        if score > highscore:
            highscore = score
        score = 0
        bird_y = int(WINDOW_HEIGHT / 2)
        bird_movement = 0
        pipes = []

    # Check for score increase
    if pipes and bird_x > pipes[0].centerx > bird_x - 2:
        score += 1

    # Update score and high score
    update_score(score)
    update_highscore(highscore)

    # Update the display
    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()