import pygame
import random

# Initialize Pygame
pygame.init()

# Game dimensions
WIDTH = 400
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("assets/Flappy Bird")

# Load game assets
bird_image = pygame.image.load("assets/bird.png")
bird_image = pygame.transform.flip(bird_image, True, False)  # Flip the bird image horizontally
bird_rect = bird_image.get_rect()
pipe_image = pygame.image.load("assets/pipe.png")

# Bird position
bird_x = int(WIDTH / 2)
bird_y = int(HEIGHT / 2)

# Gravity and jump force
gravity = 0.25
jump_force = 5.5
bird_movement = 0

# Pipes
pipe_width = 70
pipe_height = random.randint(150, 400)
pipe_x = -pipe_width

clock = pygame.time.Clock()
score = 0
running = True

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= jump_force

    bird_movement += gravity
    bird_y += bird_movement

    window.fill(WHITE)
    window.blit(bird_image, (bird_x, bird_y))

    pipe_x += 2
    pygame.draw.rect(window, BLUE, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(window, BLUE, (pipe_x, pipe_height + 150, pipe_width, HEIGHT))

    if bird_y > HEIGHT - 30 or bird_y < 0:
        running = False

    if pipe_x > WIDTH:
        pipe_x = -pipe_width
        pipe_height = random.randint(150, 400)
        score += 1

    if bird_x + 50 > pipe_x > bird_x - pipe_width:
        if bird_y < pipe_height or bird_y > pipe_height + 150:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()