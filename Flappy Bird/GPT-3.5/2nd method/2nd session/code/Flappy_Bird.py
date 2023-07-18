import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 288
HEIGHT = 512
FPS = 60
GRAVITY = 0.25
JUMP_HEIGHT = -4.5
PIPE_GAP = 100
PIPE_SPEED = 2

# Colors
WHITE = (255, 255, 255)

# Game variables
score = 0
highscore = 0

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
background_img = pygame.image.load("assets/background.png").convert()
clouds_img = pygame.image.load("assets/clouds.png").convert_alpha()
pipes_img = pygame.image.load("assets/pipes.png").convert_alpha()

# Load bird frames
bird_frames = [
    pygame.image.load("assets/bird_frames.png").subsurface((0, 0, 34, 24)),
    pygame.image.load("assets/bird_frames.png").subsurface((34, 0, 34, 24)),
    pygame.image.load("assets/bird_frames.png").subsurface((68, 0, 34, 24))
]

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.y_vel = 0
        self.index = 0
        self.animation_time = pygame.time.get_ticks()

    def update(self):
        # Animation
        if pygame.time.get_ticks() - self.animation_time > 100:
            self.index = (self.index + 1) % 3
            self.image = bird_frames[self.index]
            self.animation_time = pygame.time.get_ticks()

        # Gravity
        self.y_vel += GRAVITY
        self.rect.y += self.y_vel

        # Check collision with the ground
        if self.rect.bottom >= HEIGHT - 70:
            game_over()

    def jump(self):
        self.y_vel = JUMP_HEIGHT

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.flip(pipes_img, False, flipped)
        self.rect = self.image.get_rect()
        if flipped:
            self.rect.bottomleft = (x, y - PIPE_GAP // 2)
        else:
            self.rect.topleft = (x, y + PIPE_GAP // 2)
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()

# Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = clouds_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = WIDTH

# Start screen
def start_screen():
    global highscore
    running = True
    clock = pygame.time.Clock()

    # Load highscore from file
    try:
        with open("assets/highscore.txt", "r") as file:
            highscore = int(file.read())
    except FileNotFoundError:
        highscore = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        screen.blit(background_img, (0, 0))
        draw_text(screen, "Flappy Bird", WIDTH // 2, HEIGHT // 3, 48)
        draw_text(screen, f"Highscore: {highscore}", WIDTH // 2, HEIGHT // 2, 22)
        draw_text(screen, "Press SPACE to Start", WIDTH // 2, HEIGHT * 2 // 3, 22)

        pygame.display.flip()
        clock.tick(FPS)

# Game over screen
def game_over():
    global score, highscore
    running = True
    clock = pygame.time.Clock()

    # Update highscore if necessary
    if score > highscore:
        highscore = score
        with open("assets/highscore.txt", "w") as file:
            file.write(str(highscore))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        screen.blit(background_img, (0, 0))
        draw_text(screen, "Game Over", WIDTH // 2, HEIGHT // 3, 48)
        draw_text(screen, f"Score: {score}", WIDTH // 2, HEIGHT // 2, 22)
        draw_text(screen, f"Highscore: {highscore}", WIDTH // 2, HEIGHT * 2 // 3, 22)
        draw_text(screen, "Press SPACE to Play Again", WIDTH // 2, HEIGHT * 5 // 6, 22)

        pygame.display.flip()
        clock.tick(FPS)

# Draw text on the screen
def draw_text(surface, text, x, y, size):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

# Main game function
def game():
    global score
    running = True
    clock = pygame.time.Clock()

    # Create groups for sprites
    all_sprites = pygame.sprite.Group()
    pipes = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

    # Create bird
    bird = Bird()
    all_sprites.add(bird)

    # Create initial pipes
    for i in range(2):
        pipe = Pipe(WIDTH + i * WIDTH // 2, random.randint(HEIGHT // 4, HEIGHT * 3 // 4), False)
        pipes.add(pipe)
        all_sprites.add(pipe)

    # Create initial clouds
    for i in range(2):
        cloud = Cloud(random.randint(0, WIDTH), random.randint(50, HEIGHT // 3), random.randint(1, 2))
        clouds.add(cloud)
        all_sprites.add(cloud)

    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Update game elements
        all_sprites.update()

        # Check collision with pipes
        hits = pygame.sprite.spritecollide(bird, pipes, False)
        if hits:
            game_over()

        # Check for pass through pipes
        for pipe in pipes:
            if pipe.rect.right < bird.rect.left and not pipe.passed:
                pipe.passed = True
                score += 1

        # Add new pipes
        if len(pipes) < 2:
            last_pipe = pipes.sprites()[-1]
            if last_pipe.rect.centerx < WIDTH - WIDTH // 2:
                new_pipe = Pipe(WIDTH, random.randint(HEIGHT // 4, HEIGHT * 3 // 4), True)
                pipes.add(new_pipe)
                all_sprites.add(new_pipe)

        # Remove offscreen pipes
        for pipe in pipes:
            if pipe.rect.right < 0:
                pipe.kill()

        # Add new clouds
        if len(clouds) < 5:
            if random.random() < 0.01:
                new_cloud = Cloud(WIDTH, random.randint(50, HEIGHT // 3), random.randint(1, 2))
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        # Remove offscreen clouds
        for cloud in clouds:
            if cloud.rect.right < 0:
                cloud.kill()

        # Draw game elements
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, str(score), WIDTH // 2, HEIGHT // 8, 32)

        pygame.display.flip()
        clock.tick(FPS)

# Main game loop
start_screen()
while True:
    game()
