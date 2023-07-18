import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Game states
START_SCREEN = 0
GAMEPLAY = 1
GAME_OVER_SCREEN = 2

# Initial game state
current_state = START_SCREEN

# High score
high_score = 0

# Load font
font = pygame.font.Font(None, 36)

# Load images
bird_image = pygame.image.load("bird.png")
pipe_image = pygame.image.load("pipe.png")
background_image = pygame.image.load("background.png")

# Bird properties
bird_x = 100
bird_y = screen_height // 2
bird_dy = 0
bird_jump_power = -8

# Pipe properties
pipe_width = 70
pipe_height = random.randint(200, 400)
pipe_x = screen_width
pipe_y = random.randint(200, 400)
pipe_speed = 3

# Score
score = 0

# Game loop variables
clock = pygame.time.Clock()
is_running = True

while is_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_state == START_SCREEN:
                    # Transition from start screen to gameplay
                    current_state = GAMEPLAY
                elif current_state == GAME_OVER_SCREEN:
                    # Transition from game over screen to gameplay
                    current_state = GAMEPLAY
                    # Reset the game state
                    bird_y = screen_height // 2
                    bird_dy = 0
                    pipe_x = screen_width
                    score = 0
                else:
                    # Bird jumps when spacebar is pressed
                    bird_dy = bird_jump_power

    # Update game state
    if current_state == START_SCREEN:
        # Handle start screen logic
        # Draw the start screen
        screen.blit(background_image, (0, 0))
        title_text = font.render("Flappy Bird", True, (255, 255, 255))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))

        instructions_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, 300))

        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, 400))

    elif current_state == GAMEPLAY:
        # Handle gameplay logic
        # Update bird position
        bird_y += bird_dy
        bird_dy += 0.4  # Gravity effect

        # Update pipe position
        pipe_x -= pipe_speed

        # Check for collisions
        if bird_y >= screen_height or bird_y < 0:
            # Collided with the ground or ceiling, end the game
            current_state = GAME_OVER_SCREEN
            if score > high_score:
                high_score = score
        elif bird_x + bird_image.get_width() >= pipe_x and bird_x <= pipe_x + pipe_width:
            if bird_y <= pipe_y or bird_y + bird_image.get_height() >= pipe_y + pipe_height:
                # Collided with a pipe, end the game
                current_state = GAME_OVER_SCREEN
                if score > high_score:
                    high_score = score

        # Check if bird passed a pipe
        if bird_x > pipe_x + pipe_width:
            score += 1
            # Randomize pipe properties for the next pipe
            pipe_height = random.randint(200, 400)
            pipe_x = screen_width

        # Draw the gameplay screen
        screen.blit(background_image, (0, 0))
        screen.blit(pipe_image, (pipe_x, pipe_y))
        screen.blit(bird_image, (bird_x, bird_y))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    elif current_state == GAME_OVER_SCREEN:
        # Handle game over screen logic
        # Draw the game over screen
        screen.blit(background_image, (0, 0))
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 200))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 300))

        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, 400))

        instructions_text = font.render("Press SPACE to Play Again", True, (255, 255, 255))
        screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, 500))

    # Draw the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)  # Limit the frame rate to 60 FPS
