import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set window size
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# Load bird images
bird_images = [
    pygame.image.load('assets/bird1.png'),
    pygame.image.load('assets/bird2.png'),
    pygame.image.load('assets/bird3.png')
]

# Load ground image
ground_image = pygame.image.load('assets/base.png')

# Set initial bird position
bird_x = window_width // 2 - bird_images[0].get_width() // 2
bird_y = window_height // 2 - bird_images[0].get_height() // 2

# Set gravity and jump height
gravity = 0.5
jump_height = 8

# Set initial bird speed
bird_speed = 0

# Set animation variables
animation_index = 0
animation_speed = 0.2
animation_timer = 0

# Set pipe variables
pipe_gap = bird_images[0].get_height() * 5
pipe_spawn_time = 2000  # in milliseconds
last_spawn_time = 0
pipes = []

# Game state variables
game_over = False
score = 0
start_screen = True

# High score
high_score = 0

# Load high score from file
try:
    with open("assets/high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    # If the file does not exist, create it with a high score of 0
    with open("assets/high_score.txt", "w") as file:
        file.write("0")

# Pipe class
class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.pipe_top_image = pygame.image.load('assets/pipe_top.png')
        self.pipe_bottom_image = pygame.image.load('assets/pipe_bottom.png')
        self.scored = False

    def move(self):
        self.x -= 2  # Pipe movement speed

    def draw(self):
        top_pipe_y = self.gap_y - self.pipe_top_image.get_height()
        bottom_pipe_y = self.gap_y + pipe_gap

        window.blit(self.pipe_top_image, (self.x, top_pipe_y))
        window.blit(self.pipe_bottom_image, (self.x, bottom_pipe_y))

    def collide(self, bird_rect):
        top_pipe_rect = pygame.Rect(self.x, self.gap_y - self.pipe_top_image.get_height(), self.pipe_top_image.get_width(), self.pipe_top_image.get_height())
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + pipe_gap, self.pipe_bottom_image.get_width(), self.pipe_bottom_image.get_height())

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            return True
        return False

    def check_score(self, bird_rect):
        if not self.scored and bird_rect.x > self.x + self.pipe_top_image.get_width():
            self.scored = True
            return True
        return False

# Function to spawn a pair of pipes
def spawn_pipe():
    gap_y = random.randint(100, window_height - pipe_gap - 100)
    pipe = Pipe(window_width, gap_y)
    pipes.append(pipe)

# Show start screen
def show_start_screen():
    window.fill((135, 206, 235))  # Set background color to blue
    font = pygame.font.Font(None, 64)
    text = font.render("Press Space to Start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(text, text_rect)

# Show game over screen
def show_game_over_screen():
    window.fill((135, 206, 235))  # Set background color to blue
    font_large = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 36)
    text_large = font_large.render("Game Over", True, (255, 0, 0))
    text_small = font_small.render("Score: " + str(score), True, (255, 255, 255))
    high_score_text = font_small.render("High Score: " + str(high_score), True, (255, 255, 255))
    text_large_rect = text_large.get_rect(center=(window_width // 2, window_height // 2 - 50))
    text_small_rect = text_small.get_rect(center=(window_width // 2, window_height // 2 + 50))
    high_score_text_rect = high_score_text.get_rect(center=(window_width // 2, window_height // 2 + 100))
    window.blit(text_large, text_large_rect)
    window.blit(text_small, text_small_rect)
    window.blit(high_score_text, high_score_text_rect)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start_screen:
                    # Start the game
                    start_screen = False
                elif game_over:
                    # Reset the game
                    game_over = False
                    score = 0
                    bird_speed = 0
                    bird_y = window_height // 2 - bird_images[0].get_height() // 2
                    pipes.clear()
                    last_spawn_time = pygame.time.get_ticks()
                else:
                    # Bird jump
                    bird_speed = -jump_height

    if start_screen:
        # Show start screen
        show_start_screen()
    else:
        if not game_over:
            # Update bird position and speed
            bird_y += bird_speed
            bird_speed += gravity

            # Animate the bird
            animation_timer += clock.get_time()
            if animation_timer >= animation_speed * 1000:
                animation_index = (animation_index + 1) % len(bird_images)
                animation_timer = 0

            # Rotate the bird based on its speed
            bird_rotated = pygame.transform.rotate(bird_images[animation_index], bird_speed * -2)
            bird_rect = bird_rotated.get_rect(center=(bird_x, bird_y))

            # Check for collisions with pipes
            for pipe in pipes:
                if pipe.collide(bird_rect):
                    game_over = True

            # Check for collision with the ground
            if bird_y + bird_images[0].get_height() >= window_height - ground_image.get_height():
                game_over = True

            if not game_over:
                # Clear the screen
                window.fill((135, 206, 235))  # Set background color to blue

                # Draw ground
                ground_y = window_height - ground_image.get_height()
                window.blit(ground_image, (0, ground_y))

                # Draw pipes
                for pipe in pipes:
                    pipe.move()
                    pipe.draw()
                    if pipe.check_score(bird_rect):
                        score += 1

                # Spawn pipes
                current_time = pygame.time.get_ticks()
                if current_time - last_spawn_time >= pipe_spawn_time:
                    spawn_pipe()
                    last_spawn_time = current_time

                # Draw bird
                window.blit(bird_rotated, bird_rect)

                # Draw score
                font = pygame.font.Font(None, 36)
                text = font.render("Score: " + str(score), True, (255, 255, 255))
                window.blit(text, (10, 10))

        else:
            # Show game over screen
            show_game_over_screen()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

    # Update high score
    if score > high_score:
        high_score = score

    # Save high score to file
    with open("assets/high_score.txt", "w") as file:
        file.write(str(high_score))
