import pygame
import random

# Initialize pygame
pygame.init()

# Game window dimensions
WIDTH = 288
HEIGHT = 512

# Colors
WHITE = (255, 255, 255)

# Gravity and bird movement
gravity = 0.25
bird_movement = 0

# Game variables
score = 0
highscore = 0
game_active = False

# Create game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load background image
background_img = pygame.image.load("assets/background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load bird image
bird_img = pygame.image.load("assets/bird.png")
bird_rect = bird_img.get_rect(center=(50, HEIGHT / 2))

# Load pipe image
pipe_img = pygame.image.load("assets/pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (52, HEIGHT))

# Set up pipe variables
pipe_gap = 120
pipe_width = pipe_img.get_width()
pipe_height = pipe_img.get_height()

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load the font
font = pygame.font.Font(None, 40)

# Load the high score from file
try:
    with open("assets/highscore.txt", "r") as file:
        highscore = int(file.read())
except FileNotFoundError:
    highscore = 0

# Function to start the game
def start_game():
    global game_active, bird_movement, score
    game_active = True
    bird_movement = 0
    score = 0

# Function to draw the bird
def draw_bird():
    window.blit(bird_img, bird_rect)

# Function to move the bird
def move_bird():
    global bird_movement
    bird_movement += gravity
    bird_rect.centery += bird_movement

# Function to draw the pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            window.blit(pipe_img, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_img, False, True)
            window.blit(flip_pipe, pipe)

# Function to move the pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

# Function to generate new pipes
def generate_pipes():
    pipe_heights = [200, 300, 400]
    random_height = random.choice(pipe_heights)
    bottom_pipe = pipe_img.get_rect(midtop=(WIDTH + 100, random_height))
    top_pipe = pipe_img.get_rect(midbottom=(WIDTH + 100, random_height - pipe_gap))
    return bottom_pipe, top_pipe

# Function to check collisions
def check_collision(pipes):
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True

    return False

# Function to update the score
def update_score(score, highscore):
    if score > highscore:
        highscore = score
    score_surface = font.render("Score: " + str(score), True, WHITE)
    highscore_surface = font.render("High Score: " + str(highscore), True, WHITE)
    score_rect = score_surface.get_rect(center=(WIDTH / 2, 50))
    highscore_rect = highscore_surface.get_rect(center=(WIDTH / 2, 100))
    window.blit(score_surface, score_rect)
    window.blit(highscore_surface, highscore_rect)
    return highscore

# Game loop
running = True
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
start_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and not game_active:
                pipes.clear()
                bird_rect.center = (50, HEIGHT / 2)
                start_game()
        if event.type == SPAWNPIPE:
            pipes.extend(generate_pipes())

    window.blit(background_img, (0, 0))

    if game_active:
        # Bird
        move_bird()
        draw_bird()

        # Pipes
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Collision detection
        if check_collision(pipes):
            game_active = False
            with open("assets/highscore.txt", "w") as file:
                file.write(str(highscore))

        # Update score
        score += 0.01
        highscore = update_score(int(score), highscore)

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
