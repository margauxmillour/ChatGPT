import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load bird images
bird_frames = [
    pygame.image.load("assets/bird1.png"),
    pygame.image.load("assets/bird2.png"),
    pygame.image.load("assets/bird3.png")
]

# Load pipe images
pipe_top_image = pygame.image.load("assets/pipe_top.png")
pipe_bottom_image = pygame.image.load("assets/pipe_bottom.png")

# Load base image
base_image = pygame.image.load("assets/base.png")

# Set bird initial position
bird_x = window_width // 4  # Centered on the left side
bird_y = window_height // 2

# Set bird motion variables
bird_y_velocity = 0
gravity = 0.25
flap_height = -5

# Animation variables
animation_frame = 0
animation_speed = 0.15  # Delay between animation frames

# Pipe variables
pipe_width = 100
pipe_gap = 5 * bird_frames[0].get_height()  # Gap size is 5 times the bird's height
pipe_spawn_timer = 0
pipes = []

# Score variables
score = 0
score_font = pygame.font.Font(None, 36)

# Game over flag
game_over = False

# Start screen flag
start_screen = True
class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y

    def move(self):
        self.x -= 4  # Move the pipe from right to left

    def draw(self):
        # Draw top pipe
        window.blit(pipe_top_image, (self.x, self.gap_y - pipe_top_image.get_height()))

        # Draw bottom pipe
        bottom_pipe_y = self.gap_y + pipe_gap
        window.blit(pipe_bottom_image, (self.x, bottom_pipe_y))

def spawn_pipe():
    gap_y = random.randint(100, window_height - pipe_gap - 100)  # Random height for the gap
    new_pipe = Pipe(window_width, gap_y)
    pipes.append(new_pipe)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start_screen or game_over:
                    # Reset game state
                    start_screen = False
                    game_over = False
                    bird_y = window_height // 2
                    bird_y_velocity = 0
                    score = 0
                    pipes.clear()
                else:
                    bird_y_velocity = flap_height

    # Update bird position
    if not start_screen and not game_over:
        bird_y_velocity += gravity
        bird_y += bird_y_velocity

    # Animation logic
    animation_frame += animation_speed
    if animation_frame >= len(bird_frames):
        animation_frame = 0

    # Rotate bird image based on velocity
    bird_image = pygame.transform.rotate(bird_frames[int(animation_frame)], bird_y_velocity * -3)

    # Clear the window
    window.fill((255, 255, 255))

    if start_screen:
        # Draw start screen text
        start_text = score_font.render("Press SPACE to start", True, (0, 0, 0))
        text_width = start_text.get_width()
        text_height = start_text.get_height()
        window.blit(start_text, (window_width // 2 - text_width // 2, window_height // 2 - text_height // 2))
    elif game_over:
        # Draw game over screen text
        game_over_text = score_font.render("Game Over", True, (0, 0, 0))
        score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))
        text_width = game_over_text.get_width()
        text_height = game_over_text.get_height()
        score_width = score_text.get_width()
        score_height = score_text.get_height()
        window.blit(game_over_text, (window_width // 2 - text_width // 2, window_height // 2 - text_height))
        window.blit(score_text, (window_width // 2 - score_width // 2, window_height // 2 + text_height))

    else:
        # Draw pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()

            # Check for collision with pipes
            if pipe.x < bird_x + bird_image.get_width() and bird_x < pipe.x + pipe_width:
                if bird_y < pipe.gap_y or bird_y + bird_image.get_height() > pipe.gap_y + pipe_gap:
                    game_over = True

            # Check if bird passed the pipe
            if bird_x == pipe.x + pipe_width:
                score += 1

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x > -pipe_width]

        # Spawn new pipes every 2 seconds
        pipe_spawn_timer += 1
        if pipe_spawn_timer >= 120:
            spawn_pipe()
            pipe_spawn_timer = 0

        # Check for collision with ground
        if bird_y + bird_image.get_height() > window_height - base_image.get_height():
            game_over = True

        # Draw base (ground)
        base_x = 0
        base_y = window_height - base_image.get_height()
        window.blit(base_image, (base_x, base_y))

        # Draw bird
        window.blit(bird_image, (bird_x, bird_y))

        # Draw score
        score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))
        window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
