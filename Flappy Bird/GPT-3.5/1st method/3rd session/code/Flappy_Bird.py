import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH = 288
HEIGHT = 512

# Caption
pygame.display.set_caption("Flappy Bird")

# Load game assets
background = pygame.image.load("assets/background.png")
bird_image = pygame.image.load("assets/bird.png")
pipe_image = pygame.image.load("assets/pipe.png")
cloud_image = pygame.image.load("assets/cloud.png")

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = 0
        self.gravity = 0.5

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -8

    def check_boundaries(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            return True
        elif self.rect.top <= 0:
            self.rect.top = 0
        return False

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        super().__init__()
        self.image = pygame.transform.flip(pipe_image, False, inverted)
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.speed = 4

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right <= 0

# Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = cloud_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right <= 0

def start_game():
    bird = Bird()
    pipes = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    all_sprites.add(bird)

    score = 0
    pipe_spawn_timer = pygame.USEREVENT
    pygame.time.set_timer(pipe_spawn_timer, 1500)

    font = pygame.font.Font(None, 40)

    return bird, pipes, clouds, all_sprites, score, pipe_spawn_timer, font

def load_high_score():
    try:
        with open("assets/high_score.txt", "r") as file:
            high_score = int(file.read())
    except (IOError, ValueError):
        high_score = 0
    return high_score

def save_high_score(score):
    with open("assets/high_score.txt", "w") as file:
        file.write(str(score))

def game_over(screen, score, high_score):
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialize game variables
bird, pipes, clouds, all_sprites, score, pipe_spawn_timer, font = start_game()
high_score = load_high_score()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
        elif event.type == pipe_spawn_timer:
            pipe_x = WIDTH + 10
            pipe_y = random.randint(200, 400)
            pipe = Pipe(pipe_x, pipe_y)
            inverted_pipe = Pipe(pipe_x, pipe_y - 400, inverted=True)
            pipes.add(pipe, inverted_pipe)
            all_sprites.add(pipe, inverted_pipe)

    bird.update()
    bird.check_boundaries()

    pipes.update()
    clouds.update()

    is_passed=False
    for pipe in pipes:
        if pipe.is_offscreen():
            pipes.remove(pipe)
            all_sprites.remove(pipe)
            if not is_passed:
                score += 1
                is_passed=True

    for cloud in clouds:
        if cloud.is_offscreen():
            clouds.remove(cloud)
            all_sprites.remove(cloud)

    collided_pipes = pygame.sprite.spritecollide(bird, pipes, False)
    if collided_pipes or bird.check_boundaries():
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        game_over(screen, score, high_score)
        bird, pipes, clouds, all_sprites, score, pipe_spawn_timer, font = start_game()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 50))

    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
