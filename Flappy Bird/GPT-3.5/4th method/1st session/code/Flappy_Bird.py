import pygame
import random
import json

# Initialize pygame
pygame.init()

# Set up the game window
WIDTH = 288
HEIGHT = 512
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
background = pygame.image.load("assets/background.png")
bird_img = pygame.image.load("assets/bird.png")
pipe_img = pygame.image.load("assets/pipe.png")
font = pygame.font.Font(None, 40)

# Game variables
gravity = 0.25
bird_movement = 0
score = 0
highscore = 0

# Load highscore from file
try:
    with open("assets/highscore.txt", "r") as file:
        highscore = int(file.read())
except FileNotFoundError:
    with open("assets/highscore.txt", "w") as file:
        file.write("0")

# Function to display score
def show_score():
    score_surface = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
    window.blit(score_surface, score_rect)

    highscore_surface = font.render("Highscore: " + str(highscore), True, (255, 255, 255))
    highscore_rect = highscore_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(highscore_surface, highscore_rect)

# Function to update highscore
def update_highscore():
    global highscore
    if score > highscore:
        highscore = score
        with open("highscore.txt", "w") as file:
            file.write(str(highscore))

# Function to display the start screen
def show_start_screen():
    global game_active, score
    while not game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    score = 0

        window.blit(background, (0, 0))
        highscore_surface = font.render("Highscore: " + str(highscore), True, (255, 255, 255))
        highscore_rect = highscore_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(highscore_surface, highscore_rect)
        pygame.display.update()
        clock.tick(60)

# Function to display the game over screen
def show_game_over_screen():
    window.blit(background, (0, 0))
    game_over_surface = font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    window.blit(game_over_surface, game_over_rect)

    score_surface = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    window.blit(score_surface, score_rect)

    highscore_surface = font.render("Highscore: " + str(highscore), True, (255, 255, 255))
    highscore_rect = highscore_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    window.blit(highscore_surface, highscore_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# Game loop
running = True
game_active = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement -= 6.5
                else:
                    game_active = True
                    score = 0

    window.blit(background, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect = bird_img.get_rect(center=(50, bird_movement))
        window.blit(bird_img, bird_rect)

        # Pipes
        pipe_height = [200, 300, 400]
        pipe_list = []
        pipe_speed = 3
        if len(pipe_list) < 3:
            random_height = random.choice(pipe_height)
            bottom_pipe = pipe_img.get_rect(midtop=(350, random_height))
            top_pipe = pipe_img.get_rect(midbottom=(350, random_height - 150))
            pipe_list.extend([bottom_pipe, top_pipe])

        for pipe in pipe_list:
            pipe.centerx -= pipe_speed
            window.blit(pipe_img, pipe)

            if pipe.colliderect(bird_rect):
                game_active = False
                update_highscore()
                show_game_over_screen()

            if pipe.right < 0:
                pipe_list.remove(pipe)
                score += 1

        show_score()

        # Bird movement
        bird_movement += gravity
        bird_rect.centery += bird_movement
        window.blit(bird_img, bird_rect)

        # Floor
        floor_x_pos = 0
        floor_y_pos = 450
        floor_speed = 2
        floor_rect = background.get_rect(midtop=(WIDTH // 2, floor_y_pos))
        window.blit(background, floor_rect)

        if floor_rect.right < 0:
            floor_rect.x = 0

        pygame.display.update()
        clock.tick(60)
    else:
        show_start_screen()
