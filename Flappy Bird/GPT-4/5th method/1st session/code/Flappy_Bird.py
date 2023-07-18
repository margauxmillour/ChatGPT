import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set window size
WIN_WIDTH = 800
WIN_HEIGHT = 600

# Set gravity constant
GRAVITY = 0.8

# Set flap power
FLAP_POWER = 10

# Set pipe speed
PIPE_SPEED = 5

# Set clock
clock = pygame.time.Clock()

# Load bird images for animation
bird_frames = [pygame.image.load(f'assets/bird{i}.png') for i in range(1, 4)]
bird_index = 0

# Set bird start position
bird_rect = bird_frames[0].get_rect()
bird_rect.center = (WIN_WIDTH // 4, WIN_HEIGHT // 2)

# Set bird speed
bird_speed = 0

# Load ground image
base = pygame.image.load('assets/base.png')
base_rect = base.get_rect(bottomleft=(0, WIN_HEIGHT))

# Set background color
BG_COLOR = (0, 120, 255)  # RGB for light blue

# Create window
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Time counter for animations
ANIMATION_TIME = 200
time_since_last_frame = 0

# Pipe images
pipe_top = pygame.image.load('assets/pipe_top.png')
pipe_bottom = pygame.image.load('assets/pipe_bottom.png')

# Pipe list
pipes = []

class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.top = self.gap_y - bird_rect.height * 2.5  # gap size is 5 bird heights
        self.bottom = self.gap_y + bird_rect.height * 2.5
        self.passed = False

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self):
        win.blit(pipe_top, (self.x, self.top - pipe_top.get_height()))  # pipe_top's bottom at self.top
        win.blit(pipe_bottom, (self.x, self.bottom))  # pipe_bottom's top at self.bottom

def spawn_pipe():
    gap_y = random.randrange(100, WIN_HEIGHT - bird_rect.height * 5 - 100)  # bird_rect.height * 5 is the gap size
    pipes.append(Pipe(WIN_WIDTH, gap_y))

spawn_time = 0

# Set initial score
score = 0

# Load high score
try:
    with open('assets/high_score.txt', 'r') as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0

# Set game state
game_state = 'start'

# Start and game over messages
start_msg = pygame.font.Font(None, 36).render('Press space to start', True, (255, 255, 255))
game_over_msg = pygame.font.Font(None, 36).render('Press space to start', True, (255, 255, 255))

# Bird image
bird = bird_frames[bird_index]

# Main game loop
while True:
    dt = clock.tick(60)  # time elapsed since last frame in milliseconds

    for event in pygame.event.get():
        # Quit game if close button is pressed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Make the bird flap if spacebar is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == 'start':
                    game_state = 'play'
                elif game_state == 'game over':
                    game_state = 'start'
                    bird_rect.center = (WIN_WIDTH // 4, WIN_HEIGHT // 2)
                    bird_speed = 0
                    pipes.clear()
                    score = 0
                elif game_state == 'play':
                    bird_speed = 0
                    bird_speed -= FLAP_POWER

    # Draw background
    win.fill(BG_COLOR)

    if game_state == 'start':
        # Draw start message
        win.blit(start_msg, (WIN_WIDTH//2 - start_msg.get_width()//2, WIN_HEIGHT//2))

    elif game_state == 'play':
        # Apply gravity
        bird_speed += GRAVITY
        bird_rect.centery += bird_speed

        # Check collision with ground
        if bird_rect.colliderect(base_rect):
            game_state = 'game over'
            # Update high score
            if score > high_score:
                high_score = score
                with open('assets/high_score.txt', 'w') as f:
                    f.write(str(high_score))

        # Rotate bird
        bird_angle = bird_speed * -1  # invert angle for natural direction

        # Animate bird
        time_since_last_frame += dt
        if time_since_last_frame > ANIMATION_TIME:
            time_since_last_frame = 0
            bird_index = (bird_index + 1) % 3  # loop over 3 frames
            bird = bird_frames[bird_index]

        rotated_bird = pygame.transform.rotate(bird, bird_angle)

        # Move and draw pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()

            # Check if bird has passed pipe
            if bird_rect.centerx > pipe.x + pipe_top.get_width() and not pipe.passed:
                pipe.passed = True
                score += 1

        # Draw bird
        win.blit(rotated_bird, bird_rect)

        # Spawn new pipes every 2 seconds
        spawn_time += dt
        if spawn_time > 1000:  # 2000 milliseconds = 2 seconds
            spawn_time = 0
            spawn_pipe()

        # Check collision with pipes
        for pipe in pipes:
            if bird_rect.colliderect(pygame.Rect(pipe.x, 0, pipe_top.get_width(), pipe.top)) or \
            bird_rect.colliderect(pygame.Rect(pipe.x, pipe.bottom, pipe_bottom.get_width(), WIN_HEIGHT - pipe.bottom)):
                game_state = 'game over'
                # Update high score
                if score > high_score:
                    high_score = score
                    with open('assets/high_score.txt', 'w') as f:
                        f.write(str(high_score))

        # Remove pipes that have gone off screen
        pipes = [pipe for pipe in pipes if pipe.x + pipe_top.get_width() > 0]

        # Display score
        score_surface = pygame.font.Font(None, 36).render(str(score), True, (255, 255, 255))
        win.blit(score_surface, (WIN_WIDTH//2, 50))

    elif game_state == 'game over':
        # Draw game over message
        game_over_surface = pygame.font.Font(None, 36).render(f'Score: {score} High Score: {high_score} Press space to start', True, (255, 255, 255))
        win.blit(game_over_surface, (WIN_WIDTH//2 - game_over_surface.get_width()//2, WIN_HEIGHT//2))

    # Draw ground
    win.blit(base, base_rect)

    # Update display
    pygame.display.update()
