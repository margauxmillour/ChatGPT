import pygame
import random
import os

# Set up game window
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
FPS = 60

# Set up colors
WHITE = (255, 255, 255)

# Set up assets folders
ASSETS_FOLDER = 'assets'
IMAGES_FOLDER = os.path.join(ASSETS_FOLDER, '')

# Load assets
BACKGROUND_IMAGE = pygame.image.load(os.path.join(IMAGES_FOLDER, 'background.png'))
BIRD_IMAGE = pygame.image.load(os.path.join(IMAGES_FOLDER, 'bird.png'))
PIPE_IMAGE = pygame.image.load(os.path.join(IMAGES_FOLDER, 'pipe.png'))
BASE_IMAGE = pygame.image.load(os.path.join(IMAGES_FOLDER, 'base.png'))

# Initialize game
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

def show_score(score):
    # Render score display
    font = pygame.font.Font(None, 40)
    text = font.render("Score: " + str(score), True, WHITE)
    game_window.blit(text, (10, 10))

def show_highscore(highscore):
    # Render highscore display
    font = pygame.font.Font(None, 40)
    text = font.render("Highscore: " + str(highscore), True, WHITE)
    game_window.blit(text, (10, 50))

def draw_bird(bird_rect):
    # Draw bird on game window
    game_window.blit(BIRD_IMAGE, bird_rect)

def draw_pipes(pipes):
    # Draw pipes on game window
    for pipe in pipes:
        game_window.blit(PIPE_IMAGE, pipe)

def draw_base(base_x_position):
    # Draw base on game window
    game_window.blit(BASE_IMAGE, (base_x_position, WINDOW_HEIGHT - BASE_IMAGE.get_height()))

def is_collision(bird_rect, pipes, base_y_position):
    if bird_rect.top <= 0 or bird_rect.bottom >= WINDOW_HEIGHT - BASE_IMAGE.get_height():
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False

def flappy_bird():
    # Game variables
    gravity = 0.25
    bird_movement = 0
    flap_power = -7
    base_x_position = 0
    score = 0

    # Pipes variables
    pipes = []
    pipe_height = PIPE_IMAGE.get_height()
    pipe_spawn_timer = pygame.USEREVENT
    pygame.time.set_timer(pipe_spawn_timer, 1200)
    pipe_gap = 100

    # Load and display background
    background = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Game loop
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement = flap_power
            if event.type == pipe_spawn_timer:
                pipe_x_position = WINDOW_WIDTH
                pipe_y_position = random.randint(-200, 0)
                bottom_pipe = PIPE_IMAGE.get_rect(midtop=(pipe_x_position, pipe_y_position))
                top_pipe = PIPE_IMAGE.get_rect(midbottom=(pipe_x_position, pipe_y_position + pipe_height + pipe_gap))
                pipes.extend((bottom_pipe, top_pipe))

        bird_movement += gravity
        bird_rect = BIRD_IMAGE.get_rect(center=(50, bird_movement))
        game_window.blit(background, (0, 0))

        # Bird movement and collision detection
        bird_movement = min(bird_movement, WINDOW_HEIGHT - BASE_IMAGE.get_height())
        if is_collision(bird_rect, pipes, base_x_position):
            game_running = False
        else:
            game_running = True
            # Update pipes positions
            pipes = [pipe.move(-5, 0) for pipe in pipes if pipe.right > -50]
            draw_pipes(pipes)
            # Update bird position
            bird_movement += gravity
            rotated_bird = pygame.transform.rotate(BIRD_IMAGE, -bird_movement * 4)
            bird_rect = rotated_bird.get_rect(center=(50, bird_movement))
            draw_bird(bird_rect)
            # Update and draw base position
            base_x_position -= 1
            draw_base(base_x_position)
            if base_x_position <= -15:
                base_x_position = 0
            show_score(score)
            show_highscore(highscore)
            score += 0.01
        pygame.display.update()
        clock.tick(FPS)
    return score

def game_over(score, highscore):
    # Show game over screen
    game_window.fill(WHITE)
    font = pygame.font.Font(None, 40)
    text = font.render("Game Over", True, (0, 0, 0))
    game_window.blit(text, (100, WINDOW_HEIGHT // 2 - 40))
    show_score(score)
    show_highscore(highscore)
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    # Load highscore
    highscore = 0
    if os.path.isfile('assets/highscore.txt'):
        with open('assets/highscore.txt', 'r') as file:
            highscore = float(file.read())

    # Start game loop
    while True:
        score = flappy_bird()
        highscore = max(score, highscore)
        # Save highscore
        with open('assets/highscore.txt', 'w') as file:
            file.write(str(highscore))
        game_over(score, highscore)

if __name__ == '__main__':
    main()