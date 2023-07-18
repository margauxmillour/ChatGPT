import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 288
window_height = 512
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Flappy Bird')

# Load assets
background_image = pygame.image.load('assets/background.png')
bird_images = [pygame.image.load('assets/bird1.png'), pygame.image.load('assets/bird2.png'), pygame.image.load('assets/bird3.png')]
pipe_image = pygame.image.load('assets/pipe.png')
base_image = pygame.image.load('assets/base.png')

# Game variables
gravity = 0.25
bird_movement = 0
bird_position = pygame.Rect(50, 200, bird_images[0].get_rect().width, bird_images[0].get_rect().height)
base_position = 0
base_speed = 2
pipe_gap = 150
pipe_distance = 200
pipe_width = 52
pipe_height = 320
pipe_list = []
score = 0
high_score = 0
game_active = True
game_state = "START"  # Can be "START", "ACTIVE", or "GAME_OVER"
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

# Function to draw score on the screen
def draw_score():
    score_surface = font.render(str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(window_width // 2, 50))
    window.blit(score_surface, score_rect)

# Function to draw high score on the screen
def draw_high_score():
    high_score_surface = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    high_score_rect = high_score_surface.get_rect(center=(window_width // 2, 100))
    window.blit(high_score_surface, high_score_rect)

# Function to create new pipes
def create_pipe():
    random_pipe_position = random.randint(100,350)
    bottom_pipe = pipe_image.get_rect(topleft=(window_width, random_pipe_position + pipe_gap // 2))
    top_pipe = pipe_image.get_rect(bottomleft=(window_width, random_pipe_position - pipe_gap // 2))
    return bottom_pipe, top_pipe

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

# Function to draw pipes on the screen
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= window_height:
            window.blit(pipe_image, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_image, False, True)
            window.blit(flip_pipe, pipe)

# Function to check for collisions
def check_collisions(pipes):
    if bird_position.top <= 0 or bird_position.bottom >= window_height - base_image.get_height():
        return False
    for pipe in pipes:
        if bird_position.colliderect(pipe):
            return False
    return True

# Load the high score from a text file
def load_high_score():
    try:
        with open('assets/highscore.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Save the high score to a text file
def save_high_score(score):
    with open('assets/highscore.txt', 'w') as file:
        file.write(str(score))

# Load the high score
high_score = load_high_score()

# Game loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the high score before quitting
            save_high_score(high_score)
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "START":
                    game_state = "ACTIVE"
                elif game_state == "ACTIVE":
                    bird_movement = 0
                    bird_movement -= 5
                elif game_state == "GAME_OVER":
                    game_state = "START"
                    pipe_list.clear()
                    bird_position.center = (50, 200)
                    bird_movement = 0
                    score = 0
                    score_counted = False

    # Update bird movement
    if game_state == "ACTIVE":
        bird_movement += gravity
        bird_position.y += bird_movement

        # Pipes
        pipe_list = move_pipes(pipe_list)
        pipe_list = [pipe for pipe in pipe_list if pipe.right > -pipe_width]

        if len(pipe_list) < 2:
            pipe_list.extend(create_pipe())

        game_active = check_collisions(pipe_list)

        # Score
        score_counted = False
        for pipe in pipe_list:
            if abs(pipe.centerx - bird_position.centerx) < 2 and not score_counted:
                score += 1
                score_counted = True
        
        if score > high_score:
            high_score = score

        draw_score()
        draw_high_score()


    # Draw background
    window.blit(background_image, (0, 0))

    if game_state == "START":
        # Draw start screen
        start_surface = font.render("Press SPACE to Start", True, (255, 255, 255))
        start_rect = start_surface.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(start_surface, start_rect)
        draw_high_score()
    elif game_state == "ACTIVE":
        # Draw pipes
        draw_pipes(pipe_list)

        # Draw bird
        bird_rotated = pygame.transform.rotozoom(bird_images[int((pygame.time.get_ticks() / 100) % 3)], -bird_movement * 3, 1)
        window.blit(bird_rotated, bird_position)

        # Draw score
        draw_score()
        draw_high_score()

        # Check for game over
        if not game_active:
            game_state = "GAME_OVER"
    elif game_state == "GAME_OVER":
        # Draw game over screen
        game_over_surface = font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(game_over_surface, game_over_rect)
        draw_score()
        draw_high_score()

    # Base
    base_position -= base_speed
    window.blit(base_image, (base_position, window_height - base_image.get_height()))
    window.blit(base_image, (base_position + window_width, window_height - base_image.get_height()))
    if base_position <= -window_width:
        base_position = 0

    # Update display
    pygame.display.update()
    clock.tick(60)
