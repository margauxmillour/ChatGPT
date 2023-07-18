import pygame
import sys
import random

# game variables
screen_width = 400
screen_height = 600
gravity = 0.3
bird_movement = 0
bird_y = screen_height / 2
gap = 150
score = 0
high_score = 0
game_active = False

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# set up game clock
clock = pygame.time.Clock()

# load the bird and background images
bird = pygame.image.load('assets/bird.png').convert_alpha()
background = pygame.image.load('assets/background.png').convert_alpha()

# load font for score display
game_font = pygame.font.Font(None, 50)

# list to store pipes
pipes = []

# load high score from file
try:
    with open('assets/high_score.txt', 'r') as f:
        high_score = int(f.read())
except:
    high_score = 0

# initialize bird_rect
bird_rect = bird.get_rect(center = (100, bird_y))

def create_pipe():
    random_pipe_pos = random.randint(200, 400)
    bottom_pipe = pygame.image.load('assets/pipe_bottom.png').convert_alpha()
    top_pipe = pygame.image.load('assets/pipe_top.png').convert_alpha()
    bottom_pipe_rect = bottom_pipe.get_rect(midtop = (500, random_pipe_pos))
    top_pipe_rect = top_pipe.get_rect(midbottom = (500, random_pipe_pos - gap))
    return bottom_pipe, bottom_pipe_rect, top_pipe, top_pipe_rect

def move_pipes(pipes):
    for pipe in pipes:
        pipe[1].centerx -= 3
        pipe[3].centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe[0], pipe[1])
        screen.blit(pipe[2], pipe[3])

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe[1]) or bird_rect.colliderect(pipe[3]):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
        return False

    return True

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def draw_start_screen():
    # Draw a semi-transparent rectangle
    s = pygame.Surface((screen_width, screen_height))  # the size of your rect
    s.set_alpha(128)  # alpha level
    s.fill((255, 255, 255))  # this fills the entire surface
    screen.blit(s, (0,0))  # (0,0) are the top-left coordinates

    # Display the title
    title_surface = game_font.render('Flappy Bird', True, (0, 0, 0))
    title_rect = title_surface.get_rect(center = (screen_width / 2, 100))
    screen.blit(title_surface, title_rect)

    # Display the instructions
    instructions_surface = game_font.render('Press SPACE to play', True, (0, 0, 0))
    instructions_rect = instructions_surface.get_rect(center = (screen_width / 2, 200))
    screen.blit(instructions_surface, instructions_rect)

def draw_game_over_screen(score, high_score):
    # Draw a semi-transparent rectangle
    s = pygame.Surface((screen_width, screen_height))  # the size of your rect
    s.set_alpha(128)  # alpha level
    s.fill((255, 255, 255))  # this fills the entire surface
    screen.blit(s, (0,0))  # (0,0) are the top-left coordinates

    # Display the score
    score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 0))
    score_rect = score_surface.get_rect(center = (screen_width / 2, 100))
    screen.blit(score_surface, score_rect)

    # Display the high score
    high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (0, 0, 0))
    high_score_rect = high_score_surface.get_rect(center = (screen_width / 2, 200))
    screen.blit(high_score_surface, high_score_rect)

    # Display the instructions
    instructions_surface = game_font.render('Press SPACE to play again', True, (0, 0, 0))
    instructions_rect = instructions_surface.get_rect(center = (screen_width / 2, 300))
    screen.blit(instructions_surface, instructions_rect)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipes.clear()
                bird_rect.center = (100, bird_y)
                bird_movement = 0
                score = 0
                
    if game_active:
        bird_movement += gravity
        bird_y += bird_movement
        bird_rect.center = (100, bird_y)
        screen.blit(background, (0,0))
        screen.blit(bird, bird_rect)
        
        # pipes
        if len(pipes) == 0 or pipes[-1][1].x < screen_width - 200:
            pipes.append(create_pipe())
        pipes = move_pipes(pipes)
        draw_pipes(pipes)
        
        # check for collisions
        game_active = check_collision(pipes)
        
        # update score
        score += 0.01
        high_score = update_score(score, high_score)
        score_display = game_font.render(str(int(score)), True, (0, 0, 0))
        high_score_display = game_font.render(str(int(high_score)), True, (0, 0, 0))
        screen.blit(score_display, (screen_width / 2, 50))
        screen.blit(high_score_display, (screen_width / 2, 100))
        
        # remove off-screen pipes
        if pipes[0][1].right < 0:
            pipes.pop(0)
    else:
        if score == 0:
            draw_start_screen()
        else:
            draw_game_over_screen(score, high_score)
    
    pygame.display.update()
    clock.tick(120)
