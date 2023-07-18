import pygame
import sys
import random

pygame.init()

# Game window size
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512

# Colors
WHITE = (255, 255, 255)

# Load assets
BACKGROUND_IMAGE = pygame.image.load('assets/background.png')
BIRD_IMAGE = pygame.image.load('assets/bird.png')
BASE_IMAGE = pygame.image.load('assets/base.png')
PIPE_IMAGE = pygame.image.load('assets/pipe.png')
HIGHSCORE_IMAGE = pygame.image.load('assets/highscore.png')

# Bird properties
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_X = 50
BIRD_Y = (WINDOW_HEIGHT / 2) - (BIRD_HEIGHT / 2)

# Base properties
BASE_Y = WINDOW_HEIGHT - 112

# Pipe properties
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 100
PIPE_VELOCITY = 2
PIPE_SPAWN_INTERVAL = 1600

# Initialize the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')

clock = pygame.time.Clock()

def bird_flap():
    global bird_velocity
    bird_velocity = -7

def bird_collision():
    if bird_y < 0 or bird_y + BIRD_HEIGHT > BASE_Y:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
            return True
    return False

def create_pipe():
    random_pipe_pos = random.randint(100, 300)
    new_pipe = {
        'top': pygame.Rect(WINDOW_WIDTH, 0, PIPE_WIDTH, PIPE_HEIGHT - random_pipe_pos),
        'bottom': pygame.Rect(WINDOW_WIDTH, PIPE_HEIGHT + PIPE_GAP - random_pipe_pos, PIPE_WIDTH, random_pipe_pos)
    }
    return new_pipe

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(window, WHITE, pipe['top'])
        pygame.draw.rect(window, WHITE, pipe['bottom'])

def update_pipes(pipes):
    for pipe in pipes:
        pipe['top'].x -= PIPE_VELOCITY
        pipe['bottom'].x -= PIPE_VELOCITY

    if pipes[0]['top'].x + PIPE_WIDTH < 0:
        pipes.pop(0)

def check_score():
    global score, highscore
    for pipe in pipes:
        if 45 < pipe['top'].x < 55 and bird_x == pipe['top'].x + PIPE_WIDTH:
            score += 1
            if score > highscore:
                highscore = score

# Game variables
bird_rect = pygame.Rect(BIRD_X, BIRD_Y, BIRD_WIDTH, BIRD_HEIGHT)
bird_velocity = 0
bird_flapping = False
jump_key_pressed = False
base_x = 0
game_active = True
score = 0
highscore = 0

pipes = []
pipe_spawn_time = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn_time, PIPE_SPAWN_INTERVAL)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_flap()
                bird_flapping = True
                jump_key_pressed = True
            elif event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipes.clear()
                bird_velocity = 0
                bird_rect.y = BIRD_Y
                score = 0
                pygame.time.set_timer(pipe_spawn_time, PIPE_SPAWN_INTERVAL)

        elif event.type == pipe_spawn_time:
            pipes.append(create_pipe())

    if game_active:
        window.blit(BACKGROUND_IMAGE, (0, 0))

        # Bird
        bird_velocity += 0.4
        bird_rect.y += bird_velocity
        window.blit(BIRD_IMAGE, (bird_rect.x, bird_rect.y))

        # Pipes
        draw_pipes(pipes)
        update_pipes(pipes)

        # Base
        base_x -= 1
        window.blit(BASE_IMAGE, (base_x, BASE_Y))
        window.blit(BASE_IMAGE, (base_x + WINDOW_WIDTH, BASE_Y))

        # Score
        check_score()
        score_text = pygame.font.Font('freesansbold.ttf', 24).render(f'Score: {score}', True, WHITE)
        window.blit(score_text, (10, 10))

        # Collision detection
        game_active = not bird_collision()

        # Highscore
        window.blit(HIGHSCORE_IMAGE, (10, 430))
        highscore_text = pygame.font.Font('freesansbold.ttf', 24).render(f'{highscore}', True, WHITE)
        window.blit(highscore_text, (112, 442))

    else:
        window.blit(BACKGROUND_IMAGE, (0, 0))
        window.blit(HIGHSCORE_IMAGE, (10, 430))
        window.blit(BASE_IMAGE, (base_x, BASE_Y))
        window.blit(BASE_IMAGE, (base_x + WINDOW_WIDTH, BASE_Y))
        highscore_text = pygame.font.Font('freesansbold.ttf', 24).render(f'{highscore}', True, WHITE)
        window.blit(highscore_text, (112, 442))

    if base_x <= -WINDOW_WIDTH:
        base_x = 0

    pygame.display.update()
    clock.tick(60)