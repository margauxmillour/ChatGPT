import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
background_image = pygame.image.load("assets/background.png").convert()
bird_image = pygame.image.load("assets/bird.png").convert_alpha()
base_image = pygame.image.load("assets/base.png").convert_alpha()
pipe_image = pygame.image.load("assets/pipe.png").convert_alpha()
game_over_image = pygame.image.load("assets/background.png").convert_alpha()

# Set up game variables
bird_x = 50
bird_y = 200
bird_movement = 0
gravity = 0.25
base_x = 0
base_speed = 2
pipe_gap = 100
pipe_frequency = 1800
pipe_list = []
score = 0
highscore = 0
game_over = False

# Set up game clock
clock = pygame.time.Clock()

# Function to draw the base
def draw_base():
    window.blit(base_image, (base_x, 450))
    window.blit(base_image, (base_x + 288, 450))

# Function to create pipes
def create_pipe():
    pipe_height = random.randint(150, 300)
    pipe_top = pipe_image.get_rect(midbottom=(WINDOW_WIDTH, pipe_height - pipe_gap // 2))
    pipe_bottom = pipe_image.get_rect(midtop=(WINDOW_WIDTH, pipe_height + pipe_gap // 2))
    return pipe_top, pipe_bottom

# Function to move pipes and check collision
def move_pipes():
    for pipe in pipe_list:
        pipe.centerx -= 5
        if pipe.centerx < -50:
            pipe_list.remove(pipe)
        if pipe.colliderect(bird_rect):
            return False
    return True

# Function to draw pipes
def draw_pipes():
    for pipe in pipe_list:
        if pipe.bottom >= WINDOW_HEIGHT:
            window.blit(pipe_image, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_image, False, True)
            window.blit(flip_pipe, pipe)

# Function to update high score
def update_highscore():
    global highscore
    if score > highscore:
        highscore = score

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_movement = -8
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                pipe_list.clear()
                bird_y = 200
                bird_movement = 0
                score = 0

    # Draw background
    window.blit(background_image, (0, 0))

    if not game_over:
        # Bird movement
        bird_movement += gravity
        bird_y += bird_movement
        bird_rect = bird_image.get_rect(center=(bird_x, bird_y))
        window.blit(bird_image, bird_rect)

        game_over = not move_pipes()
        draw_pipes()
        
        # Score display
        score += 0.01
        pygame.display.set_caption(f"Flappy Bird | Score: {int(score)} | Highscore: {int(highscore)}")

    # Update high score
    update_highscore()

    # Base movement
    base_x -= base_speed
    draw_base()

    if base_x < -288:
        base_x = 0

    # Update display
    pygame.display.update()
    clock.tick(120)