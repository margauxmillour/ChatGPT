import pygame
import os
import random

# Game constants
WIN_WIDTH = 288
WIN_HEIGHT = 512
FPS = 30

# Assets paths
ASSETS_PATH = 'assets'
BG_IMG = 'background.png'  # replace with your image file
BASE_IMG = 'base.png'  # replace with your image file
BIRD_IMG = 'bird.png'  # replace with your image file
PIPE_IMG = 'pipe.png'  # replace with your image file

# Pygame initialization
pygame.init()
pygame.font.init()  # you need to call this at the start if you want to use this module.

# Setting up the display window
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Define font
font = pygame.font.Font('freesansbold.ttf', 32)  # replace 'freesansbold.ttf' with your font file

# Load images
bg = pygame.image.load(os.path.join(ASSETS_PATH, BG_IMG))
base = pygame.image.load(os.path.join(ASSETS_PATH, BASE_IMG))
bird = pygame.image.load(os.path.join(ASSETS_PATH, BIRD_IMG))
pipe = pygame.image.load(os.path.join(ASSETS_PATH, PIPE_IMG))

# Game loop
run = True
clock = pygame.time.Clock()

class Bird:
    IMG = bird
    GRAVITY = 0.5
    JUMP_SPEED = -7

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0

    def jump(self):
        self.speed = self.JUMP_SPEED

    def move(self):
        self.speed += self.GRAVITY
        self.y += self.speed

    def get_mask(self):
        return pygame.mask.from_surface(self.IMG)


class Pipe:
    IMG = pipe
    GAP = 150
    SPEED = -4

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(self.IMG, False, True)
        self.PIPE_BOTTOM = self.IMG

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 350)
        self.top = self.height - self.IMG.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x += self.SPEED

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if t_point or b_point:
            return True

        return False

# Create bird
bird = Bird(WIN_WIDTH // 3, WIN_HEIGHT // 2)

# Create pipes
pipes = [Pipe(WIN_WIDTH)]
pipe_time = 0

def load_high_score():
    try:
        with open('high_score.txt', 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def save_high_score(high_score):
    with open('high_score.txt', 'w') as f:
        f.write(str(high_score))

# Load the high score from file
high_score = load_high_score()

# Initialize score
score = 0

def start_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 64)  # replace 'freesansbold.ttf' with your font file
    instructions_font = pygame.font.Font('freesansbold.ttf', 32)  # replace 'freesansbold.ttf' with your font file

    title = title_font.render('Flappy Bird', True, (255, 255, 255))
    instructions = instructions_font.render('Press any key to start', True, (255, 255, 255))

    win.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, WIN_HEIGHT // 4))
    win.blit(instructions, (WIN_WIDTH // 2 - instructions.get_width() // 2, WIN_HEIGHT // 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                return

def game_over_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 64)  # replace 'freesansbold.ttf' with your font file
    instructions_font = pygame.font.Font('freesansbold.ttf', 32)  # replace 'freesansbold.ttf' with your font file

    title = title_font.render('Game Over', True, (255, 255, 255))
    instructions = instructions_font.render('Press any key to play again', True, (255, 255, 255))

    win.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, WIN_HEIGHT // 4))
    win.blit(instructions, (WIN_WIDTH // 2 - instructions.get_width() // 2, WIN_HEIGHT // 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                return

def game_loop():
    global pipe_time, high_score
    # Initialize bird and pipes
    bird = Bird(WIN_WIDTH // 2, WIN_HEIGHT // 2)
    pipes = []

    # Initialize score
    score = 0

    run = True

    while run:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                bird.jump()

        # Add new pipes
        pipe_time += 1
        if pipe_time > FPS * 1.5:
            pipe_time = 0
            pipes.append(Pipe(WIN_WIDTH))

        # Check if the bird has hit the ground or flown off the top of the screen
        if bird.y + bird.IMG.get_height() >= WIN_HEIGHT or bird.y < 0:
            run = False

        bird.move()

        # Draw the background, base, and bird
        win.blit(bg, (0, 0))
        win.blit(base, (0, WIN_HEIGHT - base.get_height()))
        win.blit(bird.IMG, (bird.x, bird.y))

        # Move and draw pipes
        for pipe in pipes:
            pipe.move()

            # Check for collisions
            if pipe.collide(bird):
                run = False

            # Check if the bird has passed the pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1

                # Update high score
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)

            pipe.draw(win)

        # Render the current score and high score
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        high_score_text = font.render(f'High Score: {high_score}', True, (255, 255, 255))

        # Draw the score and high score
        win.blit(score_text, (10, 10))
        win.blit(high_score_text, (10, 50))

        # Update the display
        pygame.display.update()

        # Cap the framerate
        clock.tick(FPS)
        
    return score

# Show the start screen
start_screen()

# Main game loop
while True:
    # Run the game and get the score
    score = game_loop()

    # Update high score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    # Show the game over screen
    game_over_screen()
