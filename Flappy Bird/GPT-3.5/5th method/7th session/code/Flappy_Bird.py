import pygame
import sys
import random

pygame.init()

# Window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Bird size
BIRD_WIDTH = 64
BIRD_HEIGHT = 48

# Bird initial position
bird_x = WINDOW_WIDTH // 4
bird_y = WINDOW_HEIGHT // 2 - BIRD_HEIGHT // 2

# Bird speed
bird_speed = 0

# Gravity
gravity = 0.5

# Flap height
flap_height = -10

# Bird animation frames
bird_frames = ['assets/bird1.png', 'assets/bird2.png', 'assets/bird3.png']
current_frame = 0
frame_counter = 0
frame_delay = 10  # Increase to slow down the animation

# Pipe gap size
pipe_gap = 5 * BIRD_HEIGHT

# Pipe speed
pipe_speed = 3

# Initialize the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('assets/Flappy Bird')

# Load the bird images
bird_images = []
for frame in bird_frames:
    bird_images.append(pygame.image.load(frame))

# Rotate the bird images
rotated_bird_images = []
for image in bird_images:
    rotated_bird_images.append(pygame.transform.rotate(image, -bird_speed * 3))

# Load the background image
background_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background_image.fill((135, 206, 250))  # Light blue color

# Load the ground image
ground_image = pygame.image.load('assets/base.png')

# Ground position
ground_y = WINDOW_HEIGHT - ground_image.get_rect().height

# Load the pipe images
pipe_top_image = pygame.image.load('assets/pipe_top.png')
pipe_bottom_image = pygame.image.load('assets/pipe_bottom.png')

# Font for displaying the score and messages
font = pygame.font.SysFont(None, 48)

# High score
high_score = 0

# Load the high score from file
try:
    with open("assets/high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

# Clock to control the frame rate
clock = pygame.time.Clock()


class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.passed = False

    def move(self):
        self.x -= pipe_speed

    def draw(self):
        # Draw the top pipe
        top_pipe_rect = pipe_top_image.get_rect(x=self.x, y=self.gap_y - pipe_top_image.get_height())
        window.blit(pipe_top_image, top_pipe_rect)

        # Draw the bottom pipe
        bottom_pipe_rect = pipe_bottom_image.get_rect(x=self.x, y=self.gap_y + pipe_gap)
        window.blit(pipe_bottom_image, bottom_pipe_rect)

    def collides_with_bird(self, bird_rect):
        top_pipe_rect = pipe_top_image.get_rect(x=self.x, y=self.gap_y - pipe_top_image.get_height())
        bottom_pipe_rect = pipe_bottom_image.get_rect(x=self.x, y=self.gap_y + pipe_gap)

        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

    def check_passed(self, bird_x):
        if not self.passed and self.x + pipe_top_image.get_width() < bird_x:
            self.passed = True
            return True
        return False


def spawn_pipe():
    gap_y = random.randint(100, WINDOW_HEIGHT - pipe_gap - 100)
    pipes.append(Pipe(WINDOW_WIDTH, gap_y))


def draw_start_screen():
    window.blit(background_image, (0, 0))
    start_text = font.render("Press space to start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(start_text, start_rect)
    pygame.display.update()


def draw_game_over_screen(score):
    window.blit(background_image, (0, 0))
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    window.blit(game_over_text, game_over_rect)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(score_text, score_rect)
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    window.blit(high_score_text, high_score_rect)
    pygame.display.update()


def reset_game():
    global bird_y, bird_speed, pipes, score, game_over

    bird_y = WINDOW_HEIGHT // 2 - BIRD_HEIGHT // 2
    bird_speed = 0
    pipes = []
    score = 0
    game_over = False


pipes = []
score = 0
game_over = False
start_screen = True
spawn_timer = 0
spawn_interval = 1600

while True:
    if start_screen:
        draw_start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    start_screen = False

    elif not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_speed = flap_height

        bird_speed += gravity
        bird_y += bird_speed

        # Animation
        frame_counter += 1
        if frame_counter >= frame_delay:
            current_frame = (current_frame + 1) % len(bird_frames)
            frame_counter = 0

        # Clear the window
        window.blit(background_image, (0, 0))

        # Rotate the current bird image
        rotated_bird = pygame.transform.rotate(bird_images[current_frame], -bird_speed * 3)

        # Draw the bird
        bird_rect = rotated_bird.get_rect(center=(bird_x + BIRD_WIDTH / 2, bird_y + BIRD_HEIGHT / 2))
        window.blit(rotated_bird, bird_rect)

        # Draw the ground
        ground_rect = ground_image.get_rect(x=0, y=ground_y)
        window.blit(ground_image, ground_rect)

        # Spawn pipes at regular intervals
        current_time = pygame.time.get_ticks()
        if current_time - spawn_timer >= spawn_interval:
            spawn_pipe()
            spawn_timer = current_time

        # Move and draw pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()

            if pipe.collides_with_bird(bird_rect):
                game_over = True
                break

            if pipe.check_passed(bird_x):
                score += 1

        # Remove pipes that have gone off the screen
        pipes = [pipe for pipe in pipes if pipe.x > -pipe_top_image.get_width()]

        # Check for collision with the ground
        if bird_rect.colliderect(ground_rect):
            game_over = True

        # Display the score
        score_text = font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        window.blit(score_text, score_rect)

        # Update the display
        pygame.display.update()

        # Limit the frame rate
        clock.tick(60)

    else:
        if score > high_score:
            high_score = score
            # Save the high score to the file
            with open("assets/high_score.txt", "w") as file:
                file.write(str(high_score))

        draw_game_over_screen(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    start_screen = True