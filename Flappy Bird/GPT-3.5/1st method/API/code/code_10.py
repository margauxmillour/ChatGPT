import pygame
import random
import os

# Set assets folder path
ASSETS_FOLDER = 'assets'

# Initialize Pygame
pygame.init()

# Set the game window size
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512

# Load assets
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_FOLDER, 'background.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))
BIRD_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_FOLDER, 'bird.png')), (34, 24))
BASE_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_FOLDER, 'base.png')), (WINDOW_WIDTH, 100))
PIPE_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_FOLDER, 'pipe.png')), (52, 320))
FONT = pygame.font.Font(None, 40)

# Set game colors
WHITE = (255, 255, 255)

# Set game variables
GRAVITY = 0.25
BIRD_FLAP_SPEED = -7
BASE_Y = WINDOW_HEIGHT - 100
BASE_SPEED = 1
PIPE_GAP = 100
PIPE_FREQUENCY = 1500
BIRD_X = 50

# Set game score
score = 0
highscore = 0

# Create game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Define Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = BIRD_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (BIRD_X, WINDOW_HEIGHT//2)
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def flap(self):
        self.vel_y = BIRD_FLAP_SPEED

# Define Pipe class
class Pipe():
    def __init__(self, x):
        self.image = PIPE_IMG
        self.rect_top = self.image.get_rect().move(x, -random.randint(150, 250))
        self.rect_bottom = self.image.get_rect().move(x, self.rect_top.bottom + PIPE_GAP)

    def update(self):
        self.rect_top.x -= BASE_SPEED
        self.rect_bottom.x -= BASE_SPEED

    def get_passed(self):
        return self.rect_top.right < BIRD_X

    def collide(self, bird_rect):
        return bird_rect.colliderect(self.rect_top) or bird_rect.colliderect(self.rect_bottom)

# Define Base class
class Base():
    def __init__(self):
        self.image = BASE_IMG
        self.rect = self.image.get_rect()
        self.rect.y = BASE_Y
        self.rect2 = self.image.get_rect()
        self.rect2.y = BASE_Y

    def update(self):
        self.rect.x -= BASE_SPEED
        self.rect2.x -= BASE_SPEED
        if self.rect.right == 0:
            self.rect.x = WINDOW_WIDTH
        if self.rect2.right == 0:
            self.rect2.x = WINDOW_WIDTH

# Create Bird object
bird = Bird()

# Create Base object
base = Base()

# Create Pipes group
pipes = pygame.sprite.Group()

# Create Clock object to control game speed
clock = pygame.time.Clock()

# Define game functions
def draw_objects():
    window.blit(BACKGROUND_IMG, (0, 0))
    pipes.draw(window)
    window.blit(base.image, base.rect)
    window.blit(base.image, base.rect2)
    window.blit(bird.image, bird.rect)
    window.blit(FONT.render(str(score), True, WHITE), (10, 10))
    window.blit(FONT.render("Highscore: " + str(highscore), True, WHITE), (10, 50))
    pygame.display.update()

def restart_game():
    global score
    bird.rect.center = (BIRD_X, WINDOW_HEIGHT // 2)
    bird.vel_y = 0
    base.rect.x = 0
    base.rect2.x = WINDOW_WIDTH
    pipes.empty()
    score = 0

# Game loop
running = True
while running:
    # Set game FPS
    clock.tick(60)

    # Handle game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bird.rect.top > 0:
                bird.flap()

    # Update game objects
    bird.update()
    base.update()
    pipes.update()

    # Check collisions
    if bird.rect.bottom >= BASE_Y or pygame.sprite.spritecollideany(bird, pipes):
        if score > highscore:
            highscore = score
        restart_game()

    # Check if bird passed a pair of pipes
    for pipe in pipes:
        if pipe.get_passed() and not pipe.passed:
            score += 1
            pipe.passed = True

    # Check for pipe spawn
    if len(pipes) == 0 or WINDOW_WIDTH - pipes.sprites()[-1].rect_top.x > PIPE_FREQUENCY:
        new_pipe = Pipe(WINDOW_WIDTH)
        pipes.add(new_pipe)

    # Remove pipes that are offscreen
    for pipe in pipes.sprites():
        if pipe.rect_top.right < 0:
            pipes.remove(pipe)

    # Draw game objects
    draw_objects()

# Quit the game when the loop ends
pygame.quit()