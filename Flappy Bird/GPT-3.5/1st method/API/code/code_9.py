import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 288
window_height = 512
game_window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# Load assets
background = pygame.image.load("assets/background.png")
base = pygame.image.load("assets/base.png")
bird = pygame.image.load("assets/bird.png")
pipe = pygame.image.load("assets/pipe.png")
pipe_height = pipe.get_height()
highscore = 0
font = pygame.font.Font(None, 40)

def display_score(score):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    game_window.blit(score_text, (10, 10))

def display_highscore():
    highscore_text = font.render("Highscore: " + str(highscore), True, (255, 255, 255))
    game_window.blit(highscore_text, (10, 50))

def display_game_over():
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    game_window.blit(game_over_text, (window_width // 2 - 80, window_height // 2 - 20))

def restart_game():
    global pipe_x, bird_y, bird_velocity, score, game_over
    pipe_x = window_width
    bird_y = window_height // 2
    bird_velocity = 0
    score = 0
    game_over = False

# Game variables
pipe_x = window_width
bird_y = window_height // 2
bird_velocity = 0
gravity = 0.25
jump = -5
score = 0
game_over = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump
            elif event.key == pygame.K_SPACE and game_over:
                restart_game()
    
    # Update bird position and velocity
    bird_velocity += gravity
    bird_y += bird_velocity
    
    # Check for collision with pipes, top of screen, and base
    if bird_y <= 0 or bird_y >= window_height - base.get_height():
        game_over = True
    for i in range(pipe_x, pipe_x + pipe.get_width()):
        if 0 <= bird_y <= pipe_height and i == window_width // 2:
            score += 1
        if 0 <= bird_y <= pipe_height + 100 and i == window_width // 2:
            game_over = True
    
    # Move pipes
    pipe_x -= 3
    if pipe_x + pipe.get_width() < 0:
        pipe_x = window_width
        pipe_height = random.randint(100, 300)
    
    # Draw objects on the screen
    game_window.blit(background, (0, 0))
    game_window.blit(pipe, (pipe_x, 0))
    game_window.blit(base, (0, window_height - base.get_height()))
    game_window.blit(bird, (window_width // 2 - bird.get_width() // 2, bird_y))
    
    display_score(score)
    
    if game_over:
        display_game_over()
        if score > highscore:
            highscore = score
        display_highscore()
    
    pygame.display.update()
    clock.tick(60)

# Quit Pygame
pygame.quit()