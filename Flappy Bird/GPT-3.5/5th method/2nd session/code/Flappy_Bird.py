import pygame
import sys

# Initialize pygame
pygame.init()

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)

# Bird properties
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
BIRD_SPEED = 5
GRAVITY = 0.5
FLAP_HEIGHT = 10

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load the bird image
bird_img = pygame.image.load('assets/bird.png')

# Set the initial position of the bird
bird_x = WIDTH // 4
bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2

# Set the initial speed of the bird
bird_speed = 0

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -FLAP_HEIGHT

    # Update bird's position due to gravity
    bird_speed += GRAVITY
    bird_y += bird_speed

    # Clear the screen
    screen.fill(WHITE)

    # Draw the bird
    screen.blit(bird_img, (bird_x, bird_y))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)
