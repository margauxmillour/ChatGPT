import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 288
HEIGHT = 512
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
background_img = pygame.image.load("assets/background.png").convert()
bird_img = pygame.image.load("assets/bird.png").convert_alpha()
base_img = pygame.image.load("assets/base.png").convert_alpha()
pipe_img = pygame.image.load("assets/pipe.png").convert_alpha()

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = 200
        self.velocity = 0
        self.gravity = 0.5

    def jump(self):
        self.velocity = -10

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self):
        window.blit(bird_img, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(-200, 0)
        self.gap = 150
        self.speed = 3

    def update(self):
        self.x -= self.speed

    def draw(self):
        window.blit(pipe_img, (self.x, self.y))
        window.blit(pipe_img, (self.x, self.y + self.gap + 320))

    def collide(self, bird):
        if bird.y < self.y + 320 or bird.y + 24 > self.y + self.gap + 320:
            if bird.x + 34 > self.x and bird.x < self.x + 52:
                return True
        return False

# Base class
class Base:
    def __init__(self):
        self.x = 0
        self.y = 400
        self.speed = 3

    def update(self):
        self.x -= self.speed

    def draw(self):
        window.blit(base_img, (self.x, self.y))
        window.blit(base_img, (self.x + 336, self.y))

# Game variables
bird = Bird()
base = Base()
pipes = [Pipe()]
score = 0
highest_score = 0
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    clock.tick(30)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # Update game objects
    bird.update()
    base.update()

    # Check for collisions
    if bird.y + 24 > base.y or bird.y < 0:
        running = False
    for pipe in pipes:
        if pipe.collide(bird):
            running = False

    # Check for score
    for pipe in pipes:
        if pipe.x + 52 < bird.x and not pipe.passed:
            pipe.passed = True
            score += 1
            if score > highest_score:
                highest_score = score

    # Spawn new pipes
    if pipes[-1].x < WIDTH - 200:
        pipes.append(Pipe())

    # Remove off-screen pipes
    if pipes[0].x < -52:
        pipes.pop(0)

    # Draw game objects
    window.blit(background_img, (0, 0))
    for pipe in pipes:
        pipe.update()
        pipe.draw()
    bird.draw()
    base.draw()

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))
    highest_score_text = font.render("Highest Score: " + str(highest_score), True, (255, 255, 255))
    window.blit(highest_score_text, (10, 50))

    # Update the display
    pygame.display.update()

# Game over screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Display game over message
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    # Display final score
    font = pygame.font.Font(None, 36)
    final_score_text = font.render("Final Score: " + str(score), True, (255, 255, 255))
    window.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 50))

    # Display highest score
    highest_score_text = font.render("Highest Score: " + str(highest_score), True, (255, 255, 255))
    window.blit(highest_score_text, (WIDTH // 2 - highest_score_text.get_width() // 2, HEIGHT // 2 + 100))

    # Display restart message
    restart_text = font.render("Press R to restart", True, (255, 255, 255))
    window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 200))

    # Update the display
    pygame.display.update()

    # Restart the game
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        bird = Bird()
        base = Base()
        pipes = [Pipe()]
        score = 0
        running = True
        break