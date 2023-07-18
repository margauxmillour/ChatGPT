import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load the bird images
bird_frames = [pygame.image.load("assets/bird1.png"),
               pygame.image.load("assets/bird2.png"),
               pygame.image.load("assets/bird3.png")]

bird_rect = bird_frames[0].get_rect()
bird_rect.center = (window_width // 4, window_height // 2)

# Load the base (ground) image
base_image = pygame.image.load("assets/base.png")
base_rect = base_image.get_rect()
base_rect.bottom = window_height

# Load the pipe images
pipe_top_image = pygame.image.load("assets/pipe_top.png")
pipe_bottom_image = pygame.image.load("assets/pipe_bottom.png")

# Set up the gravity and jump height
gravity = 0.5
jump_height = 8
bird_speed = 0

# Set up the animation variables
animation_index = 0
animation_speed = 0.1  # Adjust this value to change animation speed

# Set up the clock
clock = pygame.time.Clock()

# Set up the pipes
pipes = []
spawn_pipe_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_pipe_event, 2000)  # Adjust pipe spawn rate here

# Set up the game state
game_state = "start"
game_over = False
score = 0
score_font = pygame.font.Font(None, 36)
highscore = 0

# Load highscore from file
try:
    with open("assets/highscore.txt", "r") as file:
        highscore = int(file.read())
except FileNotFoundError:
    with open("assets/highscore.txt", "w") as file:
        file.write(str(highscore))


class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.scored = False

    def move(self):
        self.x -= 2  # Adjust pipe speed here

    def draw(self):
        pipe_top_rect = pipe_top_image.get_rect(topleft=(self.x, self.gap_y - pipe_top_image.get_height()))
        pipe_bottom_rect = pipe_bottom_image.get_rect(topleft=(self.x, self.gap_y + bird_rect.height * 5))
        window.blit(pipe_top_image, pipe_top_rect)
        window.blit(pipe_bottom_image, pipe_bottom_rect)


def spawn_pipe():
    gap_y = random.randint(100, window_height - bird_rect.height * 5 - 100)
    pipe = Pipe(window_width, gap_y)
    pipes.append(pipe)


def check_collision():
    if bird_rect.colliderect(base_rect):
        return True

    for pipe in pipes:
        pipe_top_rect = pipe_top_image.get_rect(topleft=(pipe.x, pipe.gap_y - pipe_top_image.get_height()))
        pipe_bottom_rect = pipe_bottom_image.get_rect(topleft=(pipe.x, pipe.gap_y + bird_rect.height * 5))
        if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
            return True

    return False


def update_score():
    global score, highscore
    for pipe in pipes:
        if pipe.x + pipe_top_image.get_width() < bird_rect.centerx and not pipe.scored:
            score += 1
            pipe.scored = True
            if score > highscore:
                highscore = score
                with open("assets/highscore.txt", "w") as file:
                    file.write(str(highscore))


def draw_start_screen():
    window.fill((135, 206, 250))
    text_font = pygame.font.Font(None, 48)
    text_surface = text_font.render("Press space to start", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(text_surface, text_rect)


def draw_game_over_screen():
    window.fill((135, 206, 250))
    text_font = pygame.font.Font(None, 48)
    score_surface = text_font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_surface.get_rect(center=(window_width // 2, window_height // 2 - 50))
    window.blit(score_surface, score_rect)
    highscore_surface = text_font.render(f"Highscore: {highscore}", True, (0, 0, 0))
    highscore_rect = highscore_surface.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(highscore_surface, highscore_rect)
    text_surface = text_font.render("Press space to start", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2 + 50))
    window.blit(text_surface, text_rect)


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "start" or game_over:
                    bird_rect.center = (window_width // 4, window_height // 2)
                    bird_speed = 0
                    pipes.clear()
                    score = 0
                    game_over = False
                    pygame.time.set_timer(spawn_pipe_event, 2000)
                    game_state = "playing"
                elif not game_over:
                    bird_speed = -jump_height
        elif event.type == spawn_pipe_event and game_state == "playing" and not game_over:
            spawn_pipe()

    if game_state == "start":
        draw_start_screen()
    elif game_state == "playing":
        # Update bird position
        bird_speed += gravity
        bird_rect.centery += bird_speed

        # Animate the bird
        animation_index += animation_speed
        if animation_index >= len(bird_frames):
            animation_index = 0
        bird_image = bird_frames[int(animation_index)]

        # Rotate the bird
        bird_rotated = pygame.transform.rotate(bird_image, -bird_speed * 2)  # Adjust rotation speed

        # Draw blue background
        window.fill((135, 206, 250))

        # Draw ground
        window.blit(base_image, base_rect)

        # Move and draw pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()

        # Draw bird
        bird_rect = bird_rotated.get_rect(center=bird_rect.center)
        window.blit(bird_rotated, bird_rect)

        # Check collision
        if check_collision():
            game_over = True
            game_state = "game_over"
            pygame.time.set_timer(spawn_pipe_event, 0)

        # Update score
        update_score()

        # Draw score
        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(topleft=(10, 10))
        window.blit(score_text, score_rect)
    elif game_state == "game_over":
        draw_game_over_screen()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)
