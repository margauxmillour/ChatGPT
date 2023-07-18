import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load the bird images
bird_frames = [
    pygame.image.load('assets/bird1.png'),
    pygame.image.load('assets/bird2.png'),
    pygame.image.load('assets/bird3.png')
]
bird_index = 0
bird_image = bird_frames[bird_index]
bird_rect = bird_image.get_rect()
bird_rect.center = (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)

# Load the ground image
ground_image = pygame.image.load('assets/base.png')
ground_rect = ground_image.get_rect()
ground_rect.topleft = (0, WINDOW_HEIGHT - ground_rect.height)

# Pipe class
class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.pipe_top_image = pygame.image.load('assets/pipe_top.png')
        self.pipe_bottom_image = pygame.image.load('assets/pipe_bottom.png')
        self.passed = False

    def move(self):
        self.x -= 5

    def draw(self):
        window.blit(self.pipe_top_image, (self.x, self.gap_y - self.pipe_top_image.get_height()))
        window.blit(self.pipe_bottom_image, (self.x, self.gap_y + 5 * bird_rect.height))

    def collides_with_bird(self):
        top_rect = pygame.Rect(self.x, self.gap_y - self.pipe_top_image.get_height(),
                               self.pipe_top_image.get_width(), self.pipe_top_image.get_height())
        bottom_rect = pygame.Rect(self.x, self.gap_y + 5 * bird_rect.height,
                                  self.pipe_bottom_image.get_width(), self.pipe_bottom_image.get_height())

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
        return False

    def has_passed_bird(self):
        if self.x + self.pipe_top_image.get_width() < bird_rect.centerx and not self.passed:
            self.passed = True
            return True
        return False

# Function to spawn a pair of pipes
def spawn_pipe():
    x = WINDOW_WIDTH
    gap_y = random.randint(100, WINDOW_HEIGHT - bird_rect.height * 5 - 100)
    pipe = Pipe(x, gap_y)
    return pipe

# Bird variables
bird_speed = 0
gravity = 0.5
flap_height = 8
rotation_angle = 30

# Game variables
game_active = False
game_over = False
score = 0
high_score = 0

# Load high score from file
try:
    with open('assets/highscore.txt', 'r') as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

# Game loop
clock = pygame.time.Clock()

pipes = []
spawn_time = 0

def start_screen():
    # Display "Press space to start" text
    start_text = pygame.font.Font(None, 64).render("Press space to start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(start_text, start_rect)

def game_over_screen():
    # Display "Game Over", score, and high score text
    game_over_text = pygame.font.Font(None, 64).render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    high_score_text = pygame.font.Font(None, 36).render(f"High Score: {high_score}", True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))

    window.blit(game_over_text, game_over_rect)
    window.blit(score_text, score_rect)
    window.blit(high_score_text, high_score_rect)

def restart_game():
    global bird_speed, game_active, game_over, score, pipes, spawn_time

    # Reset bird variables
    bird_speed = 0
    bird_rect.center = (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)

    # Reset game variables
    game_active = True
    game_over = False
    score = 0

    # Reset pipes
    pipes = []
    spawn_time = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save high score to file
            with open('assets/highscore.txt', 'w') as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_speed -= flap_height
                else:
                    restart_game()

    # Draw blue background
    window.fill((135, 206, 250))  # Light blue background color

    if game_active:
        # Update bird position
        bird_speed += gravity
        bird_rect.centery += bird_speed

        # Rotate the bird
        bird_rotated = pygame.transform.rotate(bird_image, -bird_speed * rotation_angle)
        bird_rotated_rect = bird_rotated.get_rect(center=bird_rect.center)

        # Draw ground
        window.blit(ground_image, ground_rect)

        # Draw pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()

            # Check collision with pipes
            if pipe.collides_with_bird():
                game_active = False
                game_over = True

            # Check if bird has passed the pipe
            if pipe.has_passed_bird():
                score += 1

            # Check if pipe has gone off the screen
            if pipe.x + pipe.pipe_top_image.get_width() < 0:
                pipes.remove(pipe)

        # Spawn pipes
        current_time = pygame.time.get_ticks()
        if current_time - spawn_time > 2000:
            pipes.append(spawn_pipe())
            spawn_time = current_time

        # Check collision with ground
        if bird_rect.colliderect(ground_rect):
            game_active = False
            game_over = True

        # Draw bird
        window.blit(bird_rotated, bird_rotated_rect)

        # Update bird animation
        bird_index = (bird_index + 1) % len(bird_frames)
        bird_image = bird_frames[bird_index]

        # Display score
        score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))

    else:
        if game_over:
            game_over_screen()
        else:
            start_screen()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)
