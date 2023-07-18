import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load game assets
background_img = pygame.image.load("assets/background.png").convert()
bird_img = pygame.image.load("assets/bird.png").convert_alpha()
pipe_img = pygame.image.load("assets/pipe.png").convert_alpha()
cloud_img = pygame.image.load("assets/cloud.png").convert_alpha()

# Define Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.velocity = 0
        self.gravity = 0.5

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -9

    def check_boundaries(self):
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            return True
        elif self.rect.top <= 0:
            self.rect.top = 0
            return True
        return False

# Define Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        super().__init__()
        self.image = pygame.transform.flip(pipe_img, False, inverted)
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.bottomleft = (x, y - 100)
        else:
            self.rect.topleft = (x, y)

    def update(self, speed):
        self.rect.x -= speed

    def is_offscreen(self):
        return self.rect.right <= 0

# Define Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = cloud_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right <= 0

# Create sprite groups
birds = pygame.sprite.Group()
pipes = pygame.sprite.Group()
clouds = pygame.sprite.Group()

# Define start_game function
def start_game():
    birds.empty()
    bird = Bird()
    birds.add(bird)

    pipe_spawn_timer = pygame.USEREVENT
    pygame.time.set_timer(pipe_spawn_timer, 1200)

    score = 0
    font = pygame.font.Font(None, 48)

    return bird, pipe_spawn_timer, score, font

# Load and save high score
def load_high_score():
    try:
        with open("assets/high_score.txt", "r") as file:
            high_score = int(file.read())
    except (IOError, ValueError):
        high_score = 0
    return high_score

def save_high_score(high_score):
    with open("assets/high_score.txt", "w") as file:
        file.write(str(high_score))

# Game states
START_SCREEN = 0
GAME_PLAYING = 1
GAME_OVER = 2

# Set initial game state
game_state = START_SCREEN

# Set up the game loop
clock = pygame.time.Clock()
bird, pipe_spawn_timer, score, font = start_game()
high_score = load_high_score()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == START_SCREEN or game_state == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    game_state = GAME_PLAYING
                    bird, pipe_spawn_timer, score, font = start_game()
            elif game_state == GAME_PLAYING:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if event.type == pipe_spawn_timer and game_state == GAME_PLAYING:
            pipe_x = WINDOW_WIDTH + 10
            pipe_y = random.randint(200, 380)
            pipe = Pipe(pipe_x, pipe_y)
            pipes.add(pipe)

    if game_state == GAME_PLAYING:
        window.blit(background_img, (0, 0))

        # Update birds
        birds.update()
        for bird in birds:
            if bird.check_boundaries():
                game_state = GAME_OVER

        # Update pipes
        pipes.update(2)
        for pipe in pipes:
            if pipe.is_offscreen():
                pipes.remove(pipe)

        # Update clouds
        clouds.update()
        for cloud in clouds:
            if cloud.is_offscreen():
                clouds.remove(cloud)

        # Check for collisions
        if pygame.sprite.spritecollide(bird, pipes, False):
            game_state = GAME_OVER

        # Draw game elements
        clouds.draw(window)
        birds.draw(window)
        pipes.draw(window)

        # Draw score
        score_text = font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 40))
        window.blit(score_text, score_rect)

        # Update score
        if score > high_score:
            high_score = score

        score += 1

    elif game_state == START_SCREEN or game_state == GAME_OVER:
        window.blit(background_img, (0, 0))

        # Draw score and high score
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        window.blit(score_text, score_rect)

        high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        window.blit(high_score_text, high_score_rect)

        if game_state == START_SCREEN:
            # Draw start screen message
            start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
            start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
            window.blit(start_text, start_rect)
        elif game_state == GAME_OVER:
            # Draw game over message
            game_over_text = font.render("Game Over", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
            window.blit(game_over_text, game_over_rect)

            # Draw restart message
            restart_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200))
            window.blit(restart_text, restart_rect)

    pygame.display.update()
    clock.tick(60)

# Save high score
save_high_score(high_score)

# Quit the game
pygame.quit()
