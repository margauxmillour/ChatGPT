import pygame
import random
import sys

# Game constants
WIDTH = 288
HEIGHT = 512
FPS = 60
GRAVITY = 0.5
PIPE_SPEED = 3
PIPE_SPAWN_INTERVAL = 1500
FONT_NAME = pygame.font.match_font('arial')
HIGH_SCORE_FILE = 'assets/high_score.txt'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load assets
background_img = pygame.image.load('assets/background.png').convert()
bird_img = pygame.image.load('assets/bird.png').convert_alpha()
pipe_img = pygame.image.load('assets/pipe.png').convert_alpha()
cloud_img = pygame.image.load('assets/cloud.png').convert_alpha()

# Define Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.velocity = 0
        self.gravity = GRAVITY

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -9

    def check_boundaries(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            return True
        if self.rect.top <= 0:
            self.rect.top = 0
            return True
        return False

# Define Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.flip(pipe_img, False, inverted)
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.speed = PIPE_SPEED

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right < 0

# Define Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = cloud_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right < 0

# Create sprite groups
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
clouds = pygame.sprite.Group()

def start_game():
    bird = Bird()
    all_sprites.add(bird)

    pipe_spawn_timer = pygame.time.get_ticks()
    score = 0
    high_score = load_high_score()

    return bird, pipe_spawn_timer, score, high_score

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            high_score = int(file.read())
    except (IOError, ValueError):
        high_score = 0
    return high_score

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))

def game_over(score, high_score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        screen.fill(BLACK)
        draw_text(screen, "Game Over", 50, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, f"Score: {score}", 30, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, f"High Score: {high_score}", 30, WIDTH / 2, HEIGHT / 2 + 50)
        draw_text(screen, "Press SPACE to play again", 20, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.update()
        clock.tick(FPS)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

bird, pipe_spawn_timer, score, high_score = start_game()

# Game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

    # Update
    all_sprites.update()

    # Check for collisions
    if bird.check_boundaries():
        game_over(score, high_score)
        bird, pipe_spawn_timer, score, high_score = start_game()

    # Spawn new pipes
    if pygame.time.get_ticks() - pipe_spawn_timer > PIPE_SPAWN_INTERVAL:
        pipe_x = WIDTH
        pipe_y = random.randint(200, 400)
        pipe = Pipe(pipe_x, pipe_y)
        pipes.add(pipe)
        all_sprites.add(pipe)
        pipe_spawn_timer = pygame.time.get_ticks()

    # Remove offscreen pipes
    for pipe in pipes:
        if pipe.is_offscreen():
            pipes.remove(pipe)
            all_sprites.remove(pipe)

    # Update score
    pipe_passed = pygame.sprite.spritecollideany(bird, pipes, False)
    if pipe_passed and not pipe_passed.passed:
        pipe_passed.passed = True
        score += 1
        if score > high_score:
            high_score = score

    # Draw
    screen.blit(background_img, (0, 0))
    clouds.draw(screen)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH / 2, 50)

    # Update display
    pygame.display.update()
    clock.tick(FPS)