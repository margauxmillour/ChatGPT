import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set window size
window_width = 288
window_height = 512

# Load assets
background = pygame.image.load("assets/background.png")
bird = pygame.image.load("assets/bird.png")
base = pygame.image.load("assets/base.png")
pipe = pygame.image.load("assets/pipe.png")
highscore = pygame.image.load("assets/highscore.png")

# Set up the window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Set up clock
clock = pygame.time.Clock()

# Game variables
gravity = 0.25
bird_movement = 0
bird_position = [50, window_height // 2 - bird.get_height() // 2]
base_position = [0, window_height - base.get_height()]
pipe_heights = [200, 300, 400]
pipe_width = pipe.get_width()
pipe_gap = 100
pipe_spawn_time = 2100
last_pipe_spawn_time = pygame.time.get_ticks()
score = 0
high_score = 0
game_over = False

# Function to display the score
def show_score():
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {str(score)}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

# Function to display the highest score
def show_high_score():
    font = pygame.font.Font(None, 30)
    high_score_text = font.render(f"Highest Score: {str(high_score)}", True, (255, 255, 255))
    window.blit(high_score_text, (window_width - high_score.get_width() - 10, 10))

# Function to check collision with pipes
def check_collision():
    if bird_position[1] >= base_position[1] - bird.get_height():
        return True

    for pipe_info in pipes:
        if bird_position[1] <= pipe_info[0] + pipe.get_height() and \
                bird_position[1] + bird.get_height() >= pipe_info[0] + pipe.get_height():
            if bird_position[0] + bird.get_width() >= pipe_info[1] and bird_position[0] <= pipe_info[1] + pipe_width:
                return True
        if bird_position[1] <= pipe_info[0]:
            if bird_position[0] + bird.get_width() >= pipe_info[1] and bird_position[0] <= pipe_info[1] + pipe_width:
                return True

    return False

# Game loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_movement = 0
                bird_movement -= 6

    # Update bird position
    bird_movement += gravity
    bird_position[1] += bird_movement

    # Check for collision with the base or pipes
    if check_collision():
        if score > high_score:
            high_score = score
        score = 0
        bird_position = [50, window_height // 2 - bird.get_height() // 2]
        pipes = []
        game_over = True

    # Scroll the base
    base_position[0] -= 1

    if base_position[0] <= -48:
        base_position[0] = 0

    # Generate new pipes
    current_time = pygame.time.get_ticks()
    if current_time - last_pipe_spawn_time >= pipe_spawn_time and not game_over:
        new_pipe_height = random.choice(pipe_heights)
        pipes.append([new_pipe_height, window_width])
        last_pipe_spawn_time = current_time

    # Move pipes
    for pipe_info in pipes:
        pipe_info[1] -= 2

        if pipe_info[1] + pipe_width < 0:
            pipes.remove(pipe_info)
            score += 1

    # Update the window
    window.blit(background, (0, 0))

    for pipe_info in pipes:
        window.blit(pipe, (pipe_info[1], pipe_info[0]))
        window.blit(pygame.transform.flip(pipe, False, True), (pipe_info[1], pipe_info[0] - pipe_gap - pipe.get_height()))

    window.blit(base, base_position)
    window.blit(bird, bird_position)

    if game_over:
        show_high_score()
        window.blit(highscore, (window_width // 2 - highscore.get_width() // 2, window_height // 2 - highscore.get_height() // 2))

    show_score()

    pygame.display.update()
    clock.tick(60)