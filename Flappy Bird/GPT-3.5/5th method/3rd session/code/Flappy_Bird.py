import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Window size
window_width = 800
window_height = 600

# Create the window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load the bird images
bird_frames = []
bird_frames.append(pygame.image.load('assets/bird1.png'))
bird_frames.append(pygame.image.load('assets/bird2.png'))
bird_frames.append(pygame.image.load('assets/bird3.png'))

bird_rect = bird_frames[0].get_rect()
bird_rect.center = (window_width // 4, window_height // 2)

# Load the ground image
ground_image = pygame.image.load('assets/base.png')
ground_rect = ground_image.get_rect()
ground_rect.topleft = (0, window_height - ground_rect.height)

# Load the pipe images
pipe_top_image = pygame.image.load('assets/pipe_top.png')
pipe_bottom_image = pygame.image.load('assets/pipe_bottom.png')

# Bird properties
bird_speed = 0
gravity = 0.5
flap_height = 8

# Bird animation
frame_index = 0
frame_count = 0
animation_speed = 8

# Pipe class
class Pipe:
    def __init__(self, x, gap_y):
        self.pipe_top_rect = pipe_top_image.get_rect()
        self.pipe_bottom_rect = pipe_bottom_image.get_rect()
        self.pipe_top_rect.topleft = (x, gap_y - self.pipe_top_rect.height)
        self.pipe_bottom_rect.topleft = (x, gap_y + 5 * bird_rect.height)
        self.scored = False

    def move(self):
        self.pipe_top_rect.x -= 2
        self.pipe_bottom_rect.x -= 2

    def draw(self):
        window.blit(pipe_top_image, self.pipe_top_rect)
        window.blit(pipe_bottom_image, self.pipe_bottom_rect)

# Spawn pipes
pipe_gap = 5 * bird_rect.height
pipe_spawn_timer = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn_timer, 2000)
pipes = []

def spawn_pipe():
    gap_y = random.randint(100, window_height - pipe_gap - 100)
    new_pipe = Pipe(window_width, gap_y)
    pipes.append(new_pipe)

# Score
score = 0
font = pygame.font.Font(None, 36)
score_text = font.render("Score: " + str(score), True, (0, 0, 0))
score_rect = score_text.get_rect(topright=(window_width - 10, 10))

# Highscore
highscore = 0

def load_highscore():
    try:
        with open("assets/highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_highscore(score):
    with open("assets/highscore.txt", "w") as file:
        file.write(str(score))

highscore = load_highscore()

# Game state
game_state = "start"  # "start", "playing", "game_over"

# Game loop
clock = pygame.time.Clock()
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "start":
                    game_state = "playing"
                    pipes.clear()
                    bird_rect.center = (window_width // 4, window_height // 2)
                    bird_speed = 0
                    score = 0
                    pygame.time.set_timer(pipe_spawn_timer, 2000)
                elif game_state == "playing":
                    bird_speed = -flap_height
                elif game_state == "game_over":
                    game_state = "start"

        elif event.type == pipe_spawn_timer:
            if game_state == "playing":
                spawn_pipe()

    if game_state == "start":
        # Start screen
        window.fill((255, 255, 255))
        font = pygame.font.Font(None, 64)
        start_text = font.render("Press space to start", True, (0, 0, 0))
        start_rect = start_text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(start_text, start_rect)

    elif game_state == "playing":
        # Apply gravity
        bird_speed += gravity
        bird_rect.centery += bird_speed

        # Bird animation
        frame_count += 1
        if frame_count % animation_speed == 0:
            frame_index = (frame_index + 1) % len(bird_frames)

        # Rotate the bird
        bird_rotated = pygame.transform.rotate(bird_frames[frame_index], bird_speed * -2)
        bird_rect_rotated = bird_rotated.get_rect(center=bird_rect.center)

        # Check for collisions
        if bird_rect.colliderect(ground_rect):
            game_state = "game_over"
            pygame.time.set_timer(pipe_spawn_timer, 0)  # Stop spawning pipes
            if score > highscore:
                highscore = score
                save_highscore(highscore)
        for pipe in pipes:
            if bird_rect.colliderect(pipe.pipe_top_rect) or bird_rect.colliderect(pipe.pipe_bottom_rect):
                game_state = "game_over"
                pygame.time.set_timer(pipe_spawn_timer, 0)  # Stop spawning pipes
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
            if not pipe.scored and bird_rect.right > pipe.pipe_top_rect.left:
                pipe.scored = True
                score += 1

        # Clear the window
        window.fill((255, 255, 255))

        # Draw the bird
        window.blit(bird_rotated, bird_rect_rotated)

        # Draw the pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.pipe_top_rect.right < 0:
                pipes.remove(pipe)

        # Draw the ground
        window.blit(ground_image, ground_rect)

        # Update and draw the score
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        window.blit(score_text, score_rect)

    elif game_state == "game_over":
        # Game over screen
        window.fill((255, 255, 255))
        font = pygame.font.Font(None, 64)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
        window.blit(game_over_text, game_over_rect)

        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(window_width // 2, window_height // 2 + 10))
        window.blit(score_text, score_rect)

        highscore_text = font.render("Highscore: " + str(highscore), True, (0, 0, 0))
        highscore_rect = highscore_text.get_rect(center=(window_width // 2, window_height // 2 + 70))
        window.blit(highscore_text, highscore_rect)

        press_space_text = font.render("Press space to start", True, (0, 0, 0))
        press_space_rect = press_space_text.get_rect(center=(window_width // 2, window_height // 2 + 150))
        window.blit(press_space_text, press_space_rect)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)
