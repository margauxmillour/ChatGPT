import pygame
import random

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH = 400
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Game variables
gravity = 0.25
bird_movement = 0
score = 0
high_score = 0

# Display the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load background image
background = pygame.image.load("assets/background.png").convert()

# Load bird image
bird_img = pygame.image.load("assets/bird.png").convert()
bird_rect = bird_img.get_rect(center=(100, HEIGHT/2))

# Load pipe images
pipe_img = pygame.image.load("assets/pipe.png").convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2000)
pipe_heights = [200, 300, 400]

# Load font for displaying score
font = pygame.font.Font("freesansbold.ttf", 32)

# Load high score from file
try:
    with open("assets/highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

# Function to create new pipes
def create_pipe():
    random_height = random.choice(pipe_heights)
    bottom_pipe = pipe_img.get_rect(midtop=(WIDTH + 100, random_height))
    top_pipe = pipe_img.get_rect(midbottom=(WIDTH + 100, random_height - 150))
    return bottom_pipe, top_pipe

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            window.blit(pipe_img, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            window.blit(flipped_pipe, pipe)

# Function to check for collisions
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True

    if bird_rect.top <= -100 or bird_rect.bottom >= HEIGHT:
        return True

    return False

# Function to display score
def display_score(game_state):
    if game_state == "main_game":
        score_surface = font.render(str(int(score)), True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH/2, 50))
        window.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = font.render(f"Score: {int(score)}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH/2, 50))
        window.blit(score_surface, score_rect)

        high_score_surface = font.render(f"High Score: {int(high_score)}", True, WHITE)
        high_score_rect = high_score_surface.get_rect(center=(WIDTH/2, HEIGHT-50))
        window.blit(high_score_surface, high_score_rect)

# Function to update the high score
def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Game loop
running = True
game_active = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, HEIGHT/2)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    window.blit(background, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        window.blit(bird_img, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Collision
        game_active = not check_collision(pipe_list)

        # Score
        score += 0.01
        display_score("main_game")

        # Increase difficulty
        if int(score) % 5 == 0:
            pygame.time.set_timer(SPAWNPIPE, 1500)
            gravity += 0.02

    else:
        window.blit(background, (0, 0))
        display_score("game_over")
        high_score = update_high_score(score, high_score)

    pygame.display.update()

# Save high score to file
with open("assets/highscore.txt", "w") as file:
    file.write(str(int(high_score)))

# Quit Pygame
pygame.quit()
