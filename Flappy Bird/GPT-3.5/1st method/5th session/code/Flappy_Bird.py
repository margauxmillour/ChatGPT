import pygame
import random
import sys

# Game dimensions
WIDTH = 288
HEIGHT = 512

# Colors
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load game assets
background_img = pygame.image.load("assets/background.png").convert()
bird_img = pygame.image.load("assets/bird.png").convert_alpha()
pipe_img = pygame.image.load("assets/pipe.png").convert_alpha()

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_img
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
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            return True
        return False

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_img
        self.rect = self.image.get_rect()
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - 100)
        else:
            self.rect.topleft = (x, y + 100)
        self.speed = 4

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right < 0

# Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((64, 32))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(self.image, WHITE, (32, 16), 16)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right < 0

# Start the game
def start_game():
    bird = Bird()
    pipes = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    all_sprites.add(bird)

    pipe_spawn_timer = pygame.USEREVENT
    pygame.time.set_timer(pipe_spawn_timer, 2000)
    score = 0
    font = pygame.font.Font(None, 36)

    high_score = load_high_score()

    return bird, pipes, clouds, all_sprites, pipe_spawn_timer, score, font, high_score

# Load high score from file
def load_high_score():
    try:
        with open("assets/high_score.txt", "r") as file:
            high_score = int(file.read())
    except (IOError, ValueError):
        high_score = 0
    return high_score

# Save high score to file
def save_high_score(high_score):
    with open("assets/high_score.txt", "w") as file:
        file.write(str(high_score))

# Game loop
def game_loop():
    clock = pygame.time.Clock()
    FPS = 60

    bird, pipes, clouds, all_sprites, pipe_spawn_timer, score, font, high_score = start_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
            elif event.type == pipe_spawn_timer:
                inverted = random.choice([False, True])
                pipe = Pipe(WIDTH, HEIGHT // 2, inverted)
                pipes.add(pipe)
                all_sprites.add(pipe)

        bird.update()
        pipes.update()
        clouds.update()

        if bird.check_boundaries():
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            break

        for pipe in pipes:
            if pygame.sprite.collide_rect(bird, pipe):
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                break

            if pipe.is_offscreen():
                pipes.remove(pipe)
                all_sprites.remove(pipe)
                score += 1

        if score > high_score:
            high_score = score

        clouds.add(Cloud(WIDTH, random.randint(50, 200), random.randint(1, 3)))

        screen.blit(background_img, (0, 0))
        clouds.draw(screen)
        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

game_loop()
