import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512

# Colors
WHITE = (255, 255, 255)

# Load assets
BACKGROUND_IMG = pygame.image.load('assets/background.png')
BIRD_IMG = pygame.image.load('assets/bird.png')
BASE_IMG = pygame.image.load('assets/base.png')
PIPE_IMG = pygame.image.load('assets/pipe.png')

# Bird dimensions and position
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_X = 50
BIRD_Y = (WINDOW_HEIGHT // 2) - (BIRD_HEIGHT // 2)

# Pipe dimensions
PIPE_WIDTH = PIPE_IMG.get_rect().width
PIPE_HEIGHT = PIPE_IMG.get_rect().height
PIPE_GAP = 150  # Adjust the gap between the pipes
PIPE_SPEED = 2

# Initialize the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')

clock = pygame.time.Clock()

def draw_background():
    window.blit(BACKGROUND_IMG, (0, 0))

def draw_bird(bird_y):
    window.blit(BIRD_IMG, (BIRD_X, bird_y))

def draw_pipes(pipes):
    for pipe in pipes:
        window.blit(PIPE_IMG, (pipe['x'], pipe['y_bottom']))
        window.blit(pygame.transform.flip(PIPE_IMG, False, True), (pipe['x'], pipe['y_top']))

def move_bird(bird_y, bird_movement):
    bird_y += bird_movement
    return bird_y

def move_pipes(pipes):
    for pipe in pipes:
        pipe['x'] -= PIPE_SPEED
    return pipes

def check_collision(bird_y, pipes):
    if bird_y < 0 or bird_y + BIRD_HEIGHT > WINDOW_HEIGHT - BASE_IMG.get_rect().height:
        return True

    bird_rect = pygame.Rect(BIRD_X, bird_y, BIRD_WIDTH, BIRD_HEIGHT)

    for pipe in pipes:
        pipe_top_rect = pygame.Rect(pipe['x'], pipe['y_top'], PIPE_WIDTH, PIPE_HEIGHT)
        pipe_bottom_rect = pygame.Rect(pipe['x'], pipe['y_bottom'], PIPE_WIDTH, PIPE_HEIGHT)

        if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
            return True

    return False

def update_score(bird_x, pipes, score):
    for pipe in pipes:
        if bird_x > pipe['x'] + PIPE_WIDTH and not pipe['scored']:
            pipe['scored'] = True
            score += 1
    return score

def draw_score(score):
    font = pygame.font.Font(None, 48)
    text = font.render(str(score), True, WHITE)
    window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 50))

def show_game_over(score, high_score):
    font = pygame.font.Font(None, 48)
    text1 = font.render("Game Over", True, WHITE)
    text2 = font.render("Score: " + str(score), True, WHITE)
    text3 = font.render("High Score: " + str(high_score), True, WHITE)
    text4 = font.render("Press Space to Restart", True, WHITE)
    window.blit(text1, (WINDOW_WIDTH // 2 - text1.get_width() // 2, WINDOW_HEIGHT // 2 - 100))
    window.blit(text2, (WINDOW_WIDTH // 2 - text2.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
    window.blit(text3, (WINDOW_WIDTH // 2 - text3.get_width() // 2, WINDOW_HEIGHT // 2))
    window.blit(text4, (WINDOW_WIDTH // 2 - text4.get_width() // 2, WINDOW_HEIGHT // 2 + 50))

def save_high_score(high_score):
    with open('assets/high_score.txt', 'w') as file:
        file.write(str(high_score))

def load_high_score():
    try:
        with open('assets/high_score.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Generate a new pair of pipes
def generate_pipes():
    gap_y = random.randint(100, 300)
    pipes = [
        {'x': WINDOW_WIDTH, 'y_top': gap_y - PIPE_HEIGHT, 'y_bottom': gap_y + PIPE_GAP, 'scored': False}
    ]
    return pipes

# Game loop
def game_loop():
    bird_y = BIRD_Y
    bird_movement = 0

    pipes = generate_pipes()

    score = 0
    high_score = load_high_score()

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_movement = -5

                if event.key == pygame.K_SPACE and game_over:
                    save_high_score(high_score)
                    game_loop()

        draw_background()

        if not game_over:
            # Move bird
            bird_y = move_bird(bird_y, bird_movement)
            bird_movement += 0.2

            # Move pipes
            pipes = move_pipes(pipes)

            # Check collision
            if check_collision(bird_y, pipes):
                game_over = True
                if score > high_score:
                    high_score = score

            # Update score
            score = update_score(BIRD_X, pipes, score)

            # Generate new pipes if the existing ones move off the screen
            if pipes[0]['x'] <= -PIPE_WIDTH:
                pipes = generate_pipes()

            # Draw pipes
            draw_pipes(pipes)

            # Draw base
            window.blit(BASE_IMG, (0, WINDOW_HEIGHT - BASE_IMG.get_rect().height))

            # Draw bird
            draw_bird(bird_y)

            # Draw score
            draw_score(score)

        if game_over:
            show_game_over(score, high_score)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Start the game
game_loop()
