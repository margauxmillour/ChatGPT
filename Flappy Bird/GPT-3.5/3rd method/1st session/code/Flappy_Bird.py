import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Load images
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, 'assets')

background_img = pygame.image.load(os.path.join(assets_dir, 'background.png')).convert()

pipe_bottom_img = pygame.image.load(os.path.join(assets_dir, 'pipe.png')).convert_alpha()
pipe_top_img = pygame.transform.flip(pipe_bottom_img, False, True)
pipe_width = pipe_bottom_img.get_width()
pipe_height = pipe_bottom_img.get_height()

bird_img = pygame.image.load(os.path.join(assets_dir, 'bird.png')).convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 40))

# Bird properties
bird_x = 50
bird_y = int(screen_height / 2)
bird_movement = 0
gravity = 0.5

# Pipe properties
pipe_x = screen_width
pipe_gap = 200
pipe_speed = 3

# Score
score = 0
font = pygame.font.Font(None, 36)

# High score
high_score = 0

# Load high score from file
high_score_file = os.path.join(current_dir, 'assets/highscore.txt')
if os.path.exists(high_score_file):
    with open(high_score_file, 'r') as file:
        high_score = int(file.read())

# Game over flag
game_over = False

# Start screen flag
start_screen = True

# Game loop control flag
running = True

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Generate random pipe heights with variable gap position
def generate_pipes():
    top_pipe_height = random.randint(50, screen_height - pipe_gap)
    bottom_pipe_height = screen_height - top_pipe_height - pipe_gap
    return top_pipe_height, bottom_pipe_height

# Initial pipes
pipe_top_height, pipe_bottom_height = generate_pipes()

# Function to display the start screen
def show_start_screen():
    screen.blit(background_img, (0, 0))
    start_text = font.render("Press any key to start", True, (255, 255, 255))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2))
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.update()

# Function to display the game over screen
def show_game_over_screen():
    screen.blit(background_img, (0, 0))
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 + 50))
    restart_text = font.render("Press any key to restart", True, (255, 255, 255))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 100))
    pygame.display.update()

# Main game loop
while running:
    if start_screen:
        show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                start_screen = False
    else:
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_movement = -10

            # Update bird position
            bird_movement += gravity
            bird_y += bird_movement

            # Update pipe position
            pipe_x -= pipe_speed

            # Check collision with the ground
            if bird_y < 0 or bird_y > screen_height - bird_img.get_height():
                game_over = True

            # Check if pipe passed the bird
            if pipe_x < bird_x - pipe_width:
                pipe_x = screen_width
                pipe_top_height, pipe_bottom_height = generate_pipes()
                score += 1

                # Update high score if necessary
                if score > high_score:
                    high_score = score
                    # Save high score to file
                    with open(high_score_file, 'w') as file:
                        file.write(str(high_score))

            # Check collision with the pipes
            if pipe_x < bird_x + bird_img.get_width() < pipe_x + pipe_width:
                if bird_y < pipe_top_height or bird_y + bird_img.get_height() > pipe_top_height + pipe_gap:
                    game_over = True

            # Draw the background
            screen.blit(background_img, (0, 0))

            # Draw the bird
            screen.blit(bird_img, (bird_x, int(bird_y)))

            # Draw the pipes
            screen.blit(pipe_top_img, (pipe_x, pipe_top_height - pipe_height))
            screen.blit(pipe_bottom_img, (pipe_x, pipe_top_height + pipe_gap))

            # Draw the score
            score_text = font.render("Score: " + str(score), True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Update the display
            pygame.display.update()

            # Set the frame rate
            clock.tick(60)

        # Game over screen
        show_game_over_screen()
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    start_screen = True
                    game_over = False
                    bird_y = int(screen_height / 2)
                    bird_movement = 0
                    pipe_x = screen_width
                    score = 0

# Quit the game
pygame.quit()
