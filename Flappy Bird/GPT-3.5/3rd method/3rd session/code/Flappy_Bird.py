import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load game assets
background_img = pygame.image.load("assets/background.png")
bird_img = pygame.image.load("assets/bird.png")
pipe_img = pygame.image.load("assets/pipe.png")

# Bird properties
bird_width = 40
bird_height = 30
bird_x = 100
bird_y = int((WINDOW_HEIGHT - bird_height) / 2)
bird_y_movement = 0
bird_gravity = 0.5
bird_jump_power = 9

# Pipe properties
pipe_width = 70
min_pipe_height = 150
max_pipe_height = int(WINDOW_HEIGHT * 0.9)
gap_size = 150
pipe_x = WINDOW_WIDTH
pipe_y = random.randint(min_pipe_height, max_pipe_height)
pipe_speed = 4

score = 0
high_score = 0
font = pygame.font.Font(None, 36)

game_active = False

def display_score():
    text = font.render("Score: " + str(score), True, WHITE)
    window.blit(text, (10, 10))

def display_high_score():
    text = font.render("High Score: " + str(high_score), True, WHITE)
    window.blit(text, (10, 50))

def display_bird():
    window.blit(bird_img, (bird_x, bird_y))

def display_pipe():
    window.blit(pipe_img, (pipe_x, pipe_y))
    window.blit(pygame.transform.flip(pipe_img, False, True), (pipe_x, pipe_y - pipe_img.get_height() - gap_size))

def check_collision():
    if bird_y < 0 or bird_y + bird_height > WINDOW_HEIGHT:
        return True

    if bird_x + bird_width > pipe_x and bird_x < pipe_x + pipe_width:
        if bird_y < pipe_y - gap_size or bird_y + bird_height > pipe_y:
            return True

    return False

def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))

def show_start_screen():
    window.blit(background_img, (0, 0))
    start_text = font.render("Press SPACE to Start", True, WHITE)
    window.blit(start_text, (60, WINDOW_HEIGHT // 2 - 50))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def show_game_over_screen():
    window.blit(background_img, (0, 0))
    game_over_text = font.render("Game Over", True, WHITE)
    window.blit(game_over_text, (120, WINDOW_HEIGHT // 2 - 50))
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (170, WINDOW_HEIGHT // 2))
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    window.blit(high_score_text, (140, WINDOW_HEIGHT // 2 + 50))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def load_high_score():
    global high_score
    try:
        with open("highscore.txt", "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0

load_high_score()
show_start_screen()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_y_movement = -bird_jump_power
                else:
                    game_active = True
                    bird_y = int((WINDOW_HEIGHT - bird_height) / 2)
                    bird_y_movement = 0
                    pipe_x = WINDOW_WIDTH
                    score = 0

    if game_active:
        bird_y_movement += bird_gravity
        bird_y += bird_y_movement

        if bird_x + bird_width < 0:
            bird_x = WINDOW_WIDTH

        if pipe_x + pipe_width < 0:
            pipe_x = WINDOW_WIDTH
            pipe_y = random.randint(min_pipe_height, max_pipe_height)
            score += 1

        pipe_x -= pipe_speed

        window.blit(background_img, (0, 0))
        display_bird()
        display_pipe()
        display_score()
        update_high_score()
        display_high_score()

        if check_collision():
            game_active = False
            show_game_over_screen()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
