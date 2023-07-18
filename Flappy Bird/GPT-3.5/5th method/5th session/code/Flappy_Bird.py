import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set window size
window_width = 800
window_height = 600
window_size = (window_width, window_height)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Flappy Bird")

# Load bird images
bird_images = [
    pygame.image.load('assets/bird1.png'),
    pygame.image.load('assets/bird2.png'),
    pygame.image.load('assets/bird3.png')
]

# Load ground image
ground_image = pygame.image.load('assets/base.png')

# Load pipe images
pipe_top_image = pygame.image.load('assets/pipe_top.png')
pipe_bottom_image = pygame.image.load('assets/pipe_bottom.png')

# Bird properties
bird_width = 50
bird_height = 50
bird_x = window_width // 4
bird_y = window_height // 2
bird_speed = 0
gravity = 1
flap_height = 10
bird_rotation = 0
rotation_speed = 5

# Ground properties
ground_y = window_height - ground_image.get_height()

# Pipe properties
pipe_width = 100
pipe_gap = bird_height * 5  # Gap size is 5 times bird's height
pipe_speed = 5
pipe_spawn_time = 2000  # Milliseconds
last_pipe_spawn_time = 0
pipes = []

# Score variables
score = 0
highscore = 0

# Load highscore from file
try:
    with open('assets/highscore.txt', 'r') as file:
        highscore = int(file.read())
except FileNotFoundError:
    # If highscore file doesn't exist, create it with a default value of 0
    with open('assets/highscore.txt', 'w') as file:
        file.write(str(highscore))

clock = pygame.time.Clock()

frame_index = 0
animation_speed = 0.2
animation_timer = 0

# Pipe class
class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.passed = False

    def move(self):
        self.x -= pipe_speed

    def draw(self):
        top_pipe_y = self.gap_y - pipe_top_image.get_height()
        bottom_pipe_y = self.gap_y + pipe_gap
        window.blit(pipe_top_image, (self.x, top_pipe_y))
        window.blit(pipe_bottom_image, (self.x, bottom_pipe_y))

    def collide(self, bird_rect):
        top_pipe_rect = pygame.Rect(self.x, self.gap_y - pipe_top_image.get_height(),
                                    pipe_width, pipe_top_image.get_height())
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + pipe_gap, pipe_width, pipe_bottom_image.get_height())

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            return True
        return False

    def passed_bird(self, bird_rect):
        if self.x + pipe_width < bird_rect.x and not self.passed:
            self.passed = True
            return True
        return False

# Function to spawn pipes
def spawn_pipe():
    gap_y = random.randint(100, window_height - pipe_gap - 100)
    pipe = Pipe(window_width, gap_y)
    pipes.append(pipe)

# Function to check collision with ground
def check_collision():
    if bird_rect.colliderect(ground_rect):
        return True

    for pipe in pipes:
        if pipe.collide(bird_rect):
            return True

    return False

# Game over function
def game_over():
    global score, highscore

    # Update highscore if necessary
    if score > highscore:
        highscore = score
        with open('assets/highscore.txt', 'w') as file:
            file.write(str(highscore))

    font = pygame.font.Font(None, 64)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
    highscore_text = font.render(f"Highscore: {highscore}", True, (0, 0, 0))
    highscore_rect = highscore_text.get_rect(center=(window_width // 2, window_height // 2))
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(game_over_text, game_over_rect)
    window.blit(score_text, score_rect)
    window.blit(highscore_text, highscore_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# Score display function
def display_score():
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(score_text, (20, 20))

# Start screen function
def start_screen():
    font = pygame.font.Font(None, 64)
    start_text = font.render("Press Space to Start", True, (0, 0, 0))
    start_rect = start_text.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(start_text, start_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# Game loop
start_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -flap_height

    # Update bird position
    bird_speed += gravity
    bird_y += bird_speed

    # Bird animation
    animation_timer += clock.get_time() / 1000.0  # Convert milliseconds to seconds
    if animation_timer >=animation_speed:
        frame_index = (frame_index + 1) % len(bird_images)
        animation_timer = 0

    # Rotate bird
    bird_rotation = bird_speed * rotation_speed
    rotated_bird = pygame.transform.rotate(bird_images[frame_index], bird_rotation)

    # Adjust rotated bird position to keep it centered
    bird_rect = rotated_bird.get_rect(center=(bird_x, bird_y))

    # Clear the screen with blue color
    window.fill((135, 206, 235))

    # Draw the ground
    window.blit(ground_image, (0, ground_y))
    ground_rect = pygame.Rect(0, ground_y, window_width, ground_image.get_height())

    # Spawn pipes
    current_time = pygame.time.get_ticks()
    if current_time - last_pipe_spawn_time >= pipe_spawn_time:
        spawn_pipe()
        last_pipe_spawn_time = current_time

    # Move and draw pipes
    for pipe in pipes:
        pipe.move()
        pipe.draw()

        if pipe.passed_bird(bird_rect):
            score += 1

    # Draw the rotated bird
    window.blit(rotated_bird, bird_rect)

    # Check collision
    if check_collision():
        game_over()
        score = 0
        pipes.clear()
        start_screen()

    # Display score
    display_score()

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)
