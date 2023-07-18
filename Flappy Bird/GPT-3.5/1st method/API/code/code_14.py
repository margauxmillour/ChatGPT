import pygame
import random
import os

# Setting up assets folder
assets_path = os.path.join(os.path.dirname(__file__), 'assets')

# Setting up the game window
WIDTH = 288
HEIGHT = 512
FPS = 60

# Setting up colors
WHITE = (255, 255, 255)

# Initializing pygame and creating the game window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Loading game assets
background = pygame.image.load(os.path.join(assets_path, 'background.png')).convert()
bird = pygame.image.load(os.path.join(assets_path, 'bird.png')).convert()
base = pygame.image.load(os.path.join(assets_path, 'base.png')).convert()
pipe = pygame.image.load(os.path.join(assets_path, 'pipe.png')).convert()

# Scaling the assets to the required sizes
bird = pygame.transform.scale(bird, (34, 24))
base = pygame.transform.scale(base, (336, 112))
pipe = pygame.transform.scale(pipe, (52, 320))

# Setting up bird position and velocity
bird_x = 50
bird_y = HEIGHT // 2
bird_vel_y = 0
bird_flap_power = -9

# Setting up pipe variables
pipe_gap = 100  # Gap between upper and lower pipes
pipe_frequency = 90  # Number of frames between each pipe spawn
pipe_spawn_timer = pipe_frequency
pipes = []

# Setting up gameplay variables
score = 0
highscore = 0
game_over = False

# Function to draw text on the screen
def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# Function to draw the base on the screen
def draw_base():
    screen.blit(base, (0, HEIGHT - base.get_height()))

# Function to draw the bird on the screen
def draw_bird():
    screen.blit(bird, (bird_x, bird_y))

# Function to draw a pipe on the screen
def draw_pipe(pipe_x, pipe_y):
    screen.blit(pipe, (pipe_x, pipe_y))

# Function to check for collisions
def check_collisions():
    global game_over, score, highscore

    # Check collision with base
    if bird_y + bird.get_height() >= HEIGHT - base.get_height():
        game_over = True

    # Check collision with pipes
    for pipe in pipes:
        # Check collision with upper pipe
        if bird_x + bird.get_width() >= pipe['x'] and bird_x <= pipe['x'] + pipe['width'] and bird_y <= pipe['y'] + pipe['height']:
            game_over = True
        # Check collision with lower pipe
        if bird_x + bird.get_width() >= pipe['x'] and bird_x <= pipe['x'] + pipe['width'] and bird_y + bird.get_height() >= pipe['y'] + pipe['height'] + pipe_gap:
            game_over = True

    # Check if bird passed the pipes and update the score
    for pipe in pipes:
        if pipe['x'] + pipe['width'] < bird_x and not pipe['passed']:
            pipe['passed'] = True
            score += 1

    # Update highscore
    if score > highscore:
        highscore = score

# Function to restart the game
def restart_game():
    global bird_y, bird_vel_y, score, game_over, pipes
    bird_y = HEIGHT // 2
    bird_vel_y = 0
    score = 0
    game_over = False
    pipes = []

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_vel_y = bird_flap_power
            elif event.key == pygame.K_SPACE and game_over:
                restart_game()

    if not game_over:
        # Update bird position and velocity
        bird_vel_y += 1
        bird_y += bird_vel_y

        # Update pipe positions
        for pipe in pipes:
            pipe['x'] -= 2

        # Spawn new pipes
        if pipe_spawn_timer == 0:
            pipe_x = WIDTH + 10
            pipe_y = random.randint(-200, 0)
            pipes.append({'x': pipe_x, 'y': pipe_y, 'width': pipe.get_width(), 'height': pipe.get_height(), 'passed': False})
            pipe_spawn_timer = pipe_frequency
        else:
            pipe_spawn_timer -= 1

        # Remove off-screen pipes
        if pipes and pipes[0]['x'] + pipes[0]['width'] < 0:
            pipes.pop(0)

        # Check for collisions
        check_collisions()

    # Draw background, bird, pipes and base
    screen.blit(background, (0, 0))
    for pipe in pipes:
        draw_pipe(pipe['x'], pipe['y'])
    draw_bird()
    draw_base()

    if game_over:
        draw_text("Game Over", 48, WIDTH // 2, HEIGHT // 3)
        draw_text("Press SPACE to Restart", 22, WIDTH // 2, HEIGHT // 2)
    else:
        draw_text(str(score), 56, WIDTH // 2, 50)

    draw_text("Highscore: " + str(highscore), 22, WIDTH // 2, HEIGHT - 50)

    # Updating the display
    pygame.display.flip()

# Quit pygame
pygame.quit()