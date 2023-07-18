import pygame
import random
import os

# Game window dimensions
WIDTH = 288
HEIGHT = 512

# Asset folder paths
ASSET_FOLDER = 'assets'
IMG_FOLDER = os.path.join(ASSET_FOLDER, '')

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(IMG_FOLDER, 'bird.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = 0
        self.gravity = 0.5

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = -8

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(IMG_FOLDER, 'pipe.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.randint(-200, 0)
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed

# Initializing Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game variables
score = 0
highscore = 0

# Loading assets
background = pygame.image.load(os.path.join(IMG_FOLDER, 'background.png')).convert()
base = pygame.image.load(os.path.join(IMG_FOLDER, 'base.png')).convert()
highscore_image = pygame.image.load(os.path.join(IMG_FOLDER, 'highscore.png')).convert_alpha()

# Game fonts
font = pygame.font.Font(None, 40)

# Creating sprite groups
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Creating player object
player = Bird()
all_sprites.add(player)

# Game loop
running = True
game_over = False
while running:
    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    player.flap()
                else:
                    game_over = False
                    score = 0
                    all_sprites.empty()
                    pipes.empty()
                    player.rect.center = (WIDTH // 2, HEIGHT // 2)
                    all_sprites.add(player)

    screen.blit(background, (0, 0))

    if not game_over:
        # Spawning pipes
        if len(pipes) < 5:
            if len(pipes) == 0:
                pipe = Pipe(WIDTH + 100)
            else:
                last_pipe = pipes.sprites()[-1]
                pipe = Pipe(last_pipe.rect.x + random.randint(200, 300))
            pipes.add(pipe)
            all_sprites.add(pipe)

        # Updating sprites
        all_sprites.update()

        # Collisions
        if pygame.sprite.spritecollide(player, pipes, False) or player.rect.y > HEIGHT - 112 or player.rect.y < -30:
            game_over = True

        # Scoring
        for pipe in pipes:
            if pipe.rect.x == player.rect.x:
                score += 1
                if score > highscore:
                    highscore = score

        # Removing offscreen pipes
        for pipe in pipes:
            if pipe.rect.right < 0:
                pipes.remove(pipe)
                all_sprites.remove(pipe)

        # Drawing sprites
        all_sprites.draw(screen)

        # Displaying score
        score_text = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Displaying highscore
        screen.blit(highscore_image, (10, 50))
        highscore_text = font.render(str(highscore), True, (255, 255, 255))
        screen.blit(highscore_text, (50, 60))

        # Moving and drawing base
        screen.blit(base, (0, HEIGHT - 112))
        base_x_pos = -((player.rect.x + 28) // 2 % 336)
        screen.blit(base, (base_x_pos, HEIGHT - 112))

    else:
        # Displaying game over text and instructions
        game_over_text = font.render('Game Over!', True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        restart_text = font.render('Press SPACE to restart', True, (255, 255, 255))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))
    
    pygame.display.flip()

pygame.quit()