import pygame
import random

# Initialize the game
pygame.init()

# Game window dimensions
window_width = 400
window_height = 600

# Colors (RGB format)
black = (0, 0, 0)
white = (255, 255, 255)

# Game window creation
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Bird attributes
bird_width = 50
bird_height = 50
bird_x = 50
bird_y = window_height // 2
bird_velocity = 0
gravity = 0.5

# Pipe attributes
pipe_width = 80
pipe_height = random.randint(100, 400)
pipe_x = window_width
pipe_y = random.randint(200, 400)
pipe_velocity = 3

# Clock to control frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -10

    # Bird movement
    bird_velocity += gravity
    bird_y += bird_velocity

    # Pipe movement
    pipe_x -= pipe_velocity

    # Collision detection
    if bird_y <= 0 or bird_y + bird_height >= window_height:
        running = False

    if bird_x + bird_width >= pipe_x and bird_x <= pipe_x + pipe_width:
        if bird_y <= pipe_y + pipe_height or bird_y + bird_height >= pipe_y + pipe_height + 100:
            running = False


    # Drawing the game objects
    game_window.fill(black)
    pygame.draw.rect(game_window, white, [bird_x, bird_y, bird_width, bird_height])
    pygame.draw.rect(game_window, white, [pipe_x, pipe_y, pipe_width, pipe_height])

    # Update the game display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
