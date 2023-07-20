import pygame
import sys
import random

# Define the screen size
screen_width = 288
screen_height = 512

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Define the bird
bird_img = pygame.image.load('assets/bird.png')
background_img = pygame.image.load('assets/background.png')
bird_x = 50
bird_y = screen_height / 2
bird_vel = 0
gravity = 1

# Define the pipes
pipe_height = [200, 300, 400]
pipe_img = pygame.image.load('assets/pipe.png')
pipe_x = screen_width

# The game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_vel = -10
                
    # Bird movement
    bird_vel += gravity
    bird_y += bird_vel
    
    # Pipe movement
    pipe_x -= 5
    if pipe_x < -pipe_img.get_width():
        pipe_x = screen_width
        pipe_height = random.choice(pipe_height)
    
    # Collision detection
    bird_rect = bird_img.get_rect(topleft = (bird_x, bird_y))
    pipe_rect_upper = pipe_img.get_rect(topleft = (pipe_x, 0))
    pipe_rect_lower = pipe_img.get_rect(topleft = (pipe_x, pipe_height + 100))
    
    if bird_rect.colliderect(pipe_rect_upper) or bird_rect.colliderect(pipe_rect_lower):
        break
    
    # Drawing everything on the screen
    screen.blit(background_img, (0, 0))
    screen.blit(bird_img, (bird_x, bird_y))
    screen.blit(pipe_img, (pipe_x, 0))
    screen.blit(pygame.transform.flip(pipe_img, False, True), (pipe_x, pipe_height + 100))
    pygame.display.update()
