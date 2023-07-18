import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512

# Colors
WHITE = (255, 255, 255)

# Game clock
clock = pygame.time.Clock()

# Create game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
background_img = pygame.image.load("assets/background.png").convert()
bird_img = pygame.image.load("assets/bird.png").convert_alpha()
pipe_img = pygame.image.load("assets/pipe.png").convert_alpha()
base_img = pygame.image.load("assets/base.png").convert_alpha()

# Bird dimensions and position
bird_width = 34
bird_height = 24
bird_x = WINDOW_WIDTH // 3
bird_y = WINDOW_HEIGHT // 2

# Gravity and jump velocity
gravity = 1
jump_velocity = -9

# Pipe dimensions and gap
pipe_width = 52
pipe_height = 320
pipe_gap = 100

# Base dimensions and position
base_width = 336
base_height = 112
base_x = 0
base_y = WINDOW_HEIGHT - base_height

# Score
score = 0
high_score = 0
font = pygame.font.Font(None, 40)

# Function to display score on the screen
def display_score():
    score_surface = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
    window.blit(score_surface, score_rect)

# Function to display high score on the screen
def display_high_score():
    high_score_surface = font.render(f"High Score: {high_score}", True, WHITE)
    high_score_rect = high_score_surface.get_rect(center=(WINDOW_WIDTH // 2, 100))
    window.blit(high_score_surface, high_score_rect)

# Function to draw the bird on the screen
def draw_bird():
    window.blit(bird_img, (bird_x, bird_y))

# Function to draw the pipes on the screen
def draw_pipes(pipes):
    for pipe in pipes:
        window.blit(pipe_img, (pipe['x'], pipe['top']))
        window.blit(pipe_img, (pipe['x'], pipe['bottom']))

# Function to move the pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe['x'] -= 3

# Function to generate new pipes
def generate_pipes():
    gap_y = random.randint(WINDOW_HEIGHT - pipe_gap, pipe_gap + pipe_height)
    pipe = {
        'x': WINDOW_WIDTH,
        'top': gap_y - pipe_height,
        'bottom': gap_y + pipe_gap
    }
    return pipe

# Function to check for collisions
def check_collision(pipes):
    if bird_y < 0 or bird_y + bird_height > base_y:
        return True
    for pipe in pipes:
        if bird_x + bird_width > pipe['x'] and bird_x < pipe['x'] + pipe_width:
            if bird_y < pipe['top'] or bird_y + bird_height > pipe['bottom']:
                return True
    return False

# Game loop
running = True
while running:
    # Clear the screen
    window.fill(WHITE)

    # Draw background
    window.blit(background_img, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y += jump_velocity

    # Apply gravity to bird
    bird_y += gravity

    # Draw bird
    draw_bird()

    # Generate and draw pipes
    if 'pipes' not in locals():
        pipes = [generate_pipes()]
    if pipes[-1]['x'] < WINDOW_WIDTH - 150:
        pipes.append(generate_pipes())
    draw_pipes(pipes)

    # Move and remove off-screen pipes
    move_pipes(pipes)
    if pipes[0]['x'] + pipe_width < 0:
        pipes.pop(0)

    # Check for collisions
    if check_collision(pipes):
        if score > high_score:
            high_score = score
        score = 0
        bird_y = WINDOW_HEIGHT // 2
        pipes = []

    # Increase score if bird passes a pair of pipes
    if pipes and bird_x > pipes[0]['x'] + pipe_width:
        score += 1

    # Draw base
    window.blit(base_img, (base_x, base_y))
    base_x -= 1
    if base_x <= -base_width:
        base_x = 0

    # Display score and high score
    display_score()
    display_high_score()

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
