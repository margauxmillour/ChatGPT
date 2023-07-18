import pygame
import sys
from pygame.locals import *
import random

pygame.init()

FPS = 60
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((288, 512))
FONT = pygame.font.Font('freesansbold.ttf', 32)

# Load the images
BIRD_IMG = pygame.image.load('assets/bird.png')
BACKGROUND_IMG = pygame.image.load('assets/background.png')
BASE_IMG = pygame.image.load('assets/base.png')
PIPE_IMG = pygame.image.load('assets/pipe.png')

# Game parameters
GRAVITY = 0.5
FLAP_POWER = 9
FLAP_DELAY = 0
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)
BIRD_HEIGHT = BIRD_IMG.get_height()
PIPE_HEIGHT = PIPE_IMG.get_height()
PIPE_WIDTH = PIPE_IMG.get_width()

def draw_base(base_shift):
    SCREEN.blit(BASE_IMG, (base_shift, 450))
    SCREEN.blit(BASE_IMG, (base_shift + 288, 450))

# New constant for the gap size
PIPE_GAP_SIZE = 150

def create_pipe():
    gap_y = random.randint(100, 350)
    return [
        {'x': 300, 'y': gap_y - PIPE_HEIGHT, 'passed': False},  # Upper pipe
        {'x': 300, 'y': gap_y + PIPE_GAP_SIZE, 'passed': False}  # Lower pipe
    ]

def draw_pipes(pipes):
    for pair in pipes:
        for pipe in pair:
            if pipe['y'] <= 200:  # This is the upper pipe
                SCREEN.blit(pygame.transform.flip(PIPE_IMG, False, True), (pipe['x'], pipe['y']))
            else:  # This is the lower pipe
                SCREEN.blit(PIPE_IMG, (pipe['x'], pipe['y']))

def detect_collision(playerY, pipes):
    for pair in pipes:
        for pipe in pair:
            if BIRD_HEIGHT + playerY > 450 or playerY < 0:
                return True
            bird_rect = pygame.Rect(50, playerY, BIRD_IMG.get_width(), BIRD_IMG.get_height())
            pipe_rect = pygame.Rect(pipe['x'], pipe['y'], PIPE_IMG.get_width(), PIPE_IMG.get_height())
            if bird_rect.colliderect(pipe_rect):
                return True
    return False

def move_pipes(pipes, birdX):
    for pipe in pipes:
        pipe[0]['x'] -= 3
        pipe[1]['x'] -= 3
        if birdX > pipe[0]['x'] + PIPE_WIDTH and not pipe[0]['passed']:
            pipe[0]['passed'] = True
            return True
    return False

def get_high_score():
    try:
        with open("assets/highscore.txt", 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def update_high_score(new_high_score):
    with open("assets/highscore.txt", 'w') as f:
        f.write(str(new_high_score))

def draw_start_screen():
    start_screen_text = FONT.render('Press SPACE to start', True, (255, 255, 255))
    SCREEN.blit(start_screen_text, (10, 256))

def draw_game_over_screen(score, high_score):
    game_over_text = FONT.render('GAME OVER', True, (255, 255, 255))
    SCREEN.blit(game_over_text, (10, 256))
    score_display = FONT.render('Score: ' + str(score), True, (255, 255, 255))
    SCREEN.blit(score_display, (10, 300))
    high_score_display = FONT.render('High score: ' + str(high_score), True, (255, 255, 255))
    SCREEN.blit(high_score_display, (10, 350))

def game_loop():
    game_state = 'start_screen'  # can be 'start_screen', 'main_game', 'game_over_screen'
    score = 0
    high_score = get_high_score()
    base_shift = 0
    birdY = 256
    birdY_change = 0
    pipes = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:
                if game_state == 'start_screen':
                    game_state = 'main_game'
                elif game_state == 'main_game':
                    birdY_change = 0
                    birdY_change -= FLAP_POWER
                elif game_state == 'game_over_screen':
                    game_state = 'start_screen'
                    score = 0
                    birdY_change = 0
                    birdY = 256
                    pipes = []

            if game_state == 'main_game' and event.type == SPAWN_PIPE:
                pipes.append(create_pipe())

        if game_state == 'start_screen':
            SCREEN.blit(BACKGROUND_IMG, (0, 0))
            draw_start_screen()

        elif game_state == 'main_game':
            # Bird
            birdY_change += GRAVITY
            birdY += birdY_change
            SCREEN.blit(BACKGROUND_IMG, (0, 0))
            SCREEN.blit(BIRD_IMG, (50, birdY))

            # Pipes
            if move_pipes(pipes, 50):  # check if bird passed a pipe
                score += 1
            draw_pipes(pipes)

            # Base
            base_shift -= 1
            if base_shift <= -288:
                base_shift = 0
            draw_base(base_shift)

            # Score
            score_display = FONT.render('Score: ' + str(score), True, (255, 255, 255))
            SCREEN.blit(score_display, (10, 10))

            global game_active
            game_active = not detect_collision(birdY, pipes)
            if not game_active:
                game_state = 'game_over_screen'

        elif game_state == 'game_over_screen':
            if score > high_score:  # new condition to update high score
                high_score = score
                update_high_score(high_score)
            SCREEN.blit(BACKGROUND_IMG, (0, 0))
            draw_game_over_screen(score, high_score)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    game_loop()
