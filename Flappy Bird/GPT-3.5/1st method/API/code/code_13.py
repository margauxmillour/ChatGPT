import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512

# Bird dimensions and position
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_X = 50
BIRD_Y = int(WINDOW_HEIGHT / 2)

# Pipe dimensions and position
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 100
PIPE_SPEED = 2
PIPE_SPAWN_INTERVAL = 120  # In frames

# Base dimensions and position
BASE_WIDTH = 336
BASE_HEIGHT = 112
BASE_Y = int(WINDOW_HEIGHT * 0.79)

# Load assets
BACKGROUND_IMG = pygame.image.load('assets/background.png')
BIRD_IMG = pygame.image.load('assets/bird.png')
PIPE_IMG = pygame.image.load('assets/pipe.png')
BASE_IMG = pygame.image.load('assets/base.png')
HIGHSCORE_IMG = pygame.image.load('assets/highscore.png')

# Set the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Define bird class
class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = BIRD_Y
        self.velocity = 0
        self.gravity = 0.25

    def flap(self):
        self.velocity = -6

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self):
        window.blit(BIRD_IMG, (self.x, self.y))

    def check_collision(self):
        if self.y > BASE_Y - BIRD_HEIGHT or self.y < 0:
            return True
        for pipe in pipes:
            if pipe.collides_with(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT):
                return True
        return False

# Define pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = PIPE_HEIGHT
        self.top_pipe = pygame.transform.flip(PIPE_IMG, False, True)
        self.bottom_pipe = PIPE_IMG

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        window.blit(self.top_pipe, (self.x, self.height - PIPE_HEIGHT))
        window.blit(self.bottom_pipe, (self.x, self.height + PIPE_GAP))

    def collides_with(self, bird_x, bird_y, bird_width, bird_height):
        return pygame.Rect(self.x, self.height - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT).colliderect(
            pygame.Rect(bird_x, bird_y, bird_width, bird_height))
        

# Define base class
class Base:
    def __init__(self):
        self.x = 0

    def update(self):
        self.x -= PIPE_SPEED
        if self.x <= -BASE_WIDTH:
            self.x = 0

    def draw(self):
        window.blit(BASE_IMG, (self.x, BASE_Y))
        window.blit(BASE_IMG, (self.x + BASE_WIDTH, BASE_Y))

# Define text render function
def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    rect.midtop = (x, y)
    window.blit(surface, rect)

# Game variables
score = 0
highscore = 0
game_over = False

# Load highscore from external file, if it exists
try:
    with open('assets/highscore.txt', 'r') as file:
        highscore = int(file.read())
except FileNotFoundError:
    pass

# Create bird, pipes and base
bird = Bird()
pipes = [Pipe(WINDOW_WIDTH + i * PIPE_SPAWN_INTERVAL) for i in range(2)]
base = Base()


# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save highscore to external file
            with open('assets/highscore.txt', 'w') as file:
                file.write(str(highscore))
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird.flap()
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                pipes = [Pipe(WINDOW_WIDTH + i * PIPE_SPAWN_INTERVAL) for i in range(2)]
                bird = Bird()
                score = 0

    # Update bird, pipes and base
    bird.update()
    base.update()
    for pipe in pipes:
        pipe.update()

    # Check collision
    if bird.check_collision():
        game_over = True
        if score > highscore:
            highscore = score

    # Draw background, bird, pipes, base, score and highscore
    window.blit(BACKGROUND_IMG, (0, 0))
    bird.draw()
    for pipe in pipes:
        pipe.draw()
    base.draw()
    draw_text(str(score), pygame.font.Font(None, 40), (255, 255, 255), WINDOW_WIDTH / 2, 30)
    window.blit(HIGHSCORE_IMG, (50, 50))
    draw_text(str(highscore), pygame.font.Font(None, 20), (255, 255, 255), 70, 80)

    # Score logic
    if not game_over:
        for pipe in pipes:
            if bird.x > pipe.x + PIPE_WIDTH and not pipe.passed:
                pipe.passed = True
                score += 1
            if pipe.x <= -PIPE_WIDTH:
                pipes.remove(pipe)
                pipes.append(Pipe(WINDOW_WIDTH + PIPE_SPAWN_INTERVAL))

    # Game over logic
    if game_over:
        draw_text('Game Over!', pygame.font.Font(None, 40), (255, 255, 255), WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        draw_text('Press Space to Restart', pygame.font.Font(None, 20), (255, 255, 255), WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) + 50)

    # Update display
    pygame.display.update()
    clock.tick(60)