import pygame
import random
import os

# Game Constants
WIDTH = 288
HEIGHT = 512
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Set up assets folders
game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, "assets")

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(assets_folder, "bird.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.y_speed = 0

    def update(self):
        self.y_speed += 0.8
        self.rect.y += self.y_speed

    def flap(self):
        self.y_speed = -10

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(assets_folder, "pipe.png")).convert_alpha()
        self.rect = self.image.get_rect()
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - 100)
        else:
            self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= 4

# Game initialization
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load assets
background_img = pygame.image.load(os.path.join(assets_folder, "background.png")).convert()
base_img = pygame.image.load(os.path.join(assets_folder, "base.png")).convert_alpha()
highscore_img = pygame.image.load(os.path.join(assets_folder, "highscore.png")).convert_alpha()
font = pygame.font.Font(None, 48)

# Create sprites
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
bird = Bird()
all_sprites.add(bird)

# Game variables
score = 0
highscore = 0

# Spawn pipes
pipe_heights = [200, 300, 400]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

running = True
game_over = False

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird.flap()
            if event.key == pygame.K_RETURN and game_over:
                game_over = False
                score = 0
                all_sprites.empty()
                pipes.empty()
                bird.rect.center = (WIDTH // 2, HEIGHT // 2)
                all_sprites.add(bird)

        elif event.type == SPAWNPIPE:
            pipe_y = random.choice(pipe_heights)
            top_pipe = Pipe(WIDTH, pipe_y, True)
            bottom_pipe = Pipe(WIDTH, pipe_y + 250)
            pipes.add(top_pipe)
            pipes.add(bottom_pipe)
            all_sprites.add(top_pipe)
            all_sprites.add(bottom_pipe)

    # Update
    if not game_over:
        all_sprites.update()

        # Check collisions
        hits = pygame.sprite.spritecollide(bird, pipes, False)
        if hits or bird.rect.bottom >= HEIGHT - 100:
            game_over = True
        
        # Update score
        for pipe in pipes:
            if pipe.rect.right < bird.rect.left and not pipe.rect.y == 0 and not pipe.rect.y == HEIGHT - 100:
                score += 1

        # Remove offscreen pipes
        for pipe in pipes:
            if pipe.rect.right <= 0:
                pipes.remove(pipe)
                all_sprites.remove(pipe)

    # Draw
    screen.blit(background_img, (0, 0))
    pipes.draw(screen)
    all_sprites.draw(screen)
    screen.blit(base_img, (0, HEIGHT - 100))

    # Display score and highscore
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    if score > highscore:
        highscore = score

    highscore_text = font.render(str(highscore), True, WHITE)
    screen.blit(highscore_img, (WIDTH // 2 - highscore_img.get_width() // 2, 70))
    screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, 120))

    if game_over:
        screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, 280))
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 360))
        restart_text = font.render("Press Enter to Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 420))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()