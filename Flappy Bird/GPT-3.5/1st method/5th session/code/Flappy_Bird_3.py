import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions and caption
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load game assets
background_image = pygame.image.load("assets/background.png")
bird_image = pygame.image.load("assets/bird.png")
pipe_image = pygame.image.load("assets/pipe.png")
cloud_image = pygame.image.load("assets/cloud.png")

# Define Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.velocity = 0
        self.gravity = 0.5

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -10

    def check_boundaries(self):
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            return True
        elif self.rect.top <= 0:
            self.rect.top = 0
        return False

# Define Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted):
        super().__init__()
        self.image = pygame.transform.flip(pipe_image, False, inverted)
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.topleft = (x, y - self.rect.height)
        else:
            self.rect.bottomleft = (x, y)
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right <= 0

# Define Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = cloud_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right <= 0

# Create sprite groups for birds, pipes, and clouds
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()

# Initialize game state
def start_game():
    bird_group.empty()
    pipe_group.empty()
    bird = Bird()
    bird_group.add(bird)
    pipe_spawn_timer = 0
    score = 0
    font = pygame.font.Font(None, 40)
    high_score = load_high_score()
    return bird, pipe_spawn_timer, score, font, high_score

# Load high score from file
def load_high_score():
    try:
        with open("assets/high_score.txt", "r") as file:
            high_score = int(file.read())
    except (ValueError, FileNotFoundError):
        high_score = 0
    return high_score

# Save high score to file
def save_high_score(high_score):
    with open("assets/high_score.txt", "w") as file:
        file.write(str(high_score))

# Main game loop
def game_loop():
    bird, pipe_spawn_timer, score, font, high_score = start_game()
    game_over = False

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Update game elements
        bird.update()
        game_over = bird.check_boundaries()

        pipe_spawn_timer += 1
        if pipe_spawn_timer > 100:
            pipe_x = WINDOW_WIDTH
            pipe_y = WINDOW_HEIGHT // 2 + random.randint(-100, 100)
            pipe_inverted = bool(random.getrandbits(1))
            new_pipe = Pipe(pipe_x, pipe_y, pipe_inverted)
            pipe_group.add(new_pipe)
            pipe_spawn_timer = 0

        pipe_group.update()
        cloud_group.update()

        # Check for collisions
        if pygame.sprite.spritecollide(bird, pipe_group, False):
            game_over = True

        # Remove offscreen pipes
        for pipe in pipe_group:
            if pipe.is_offscreen():
                pipe_group.remove(pipe)
                score += 1

        # Draw game elements
        window.blit(background_image, (0, 0))
        bird_group.draw(window)
        pipe_group.draw(window)

        # Draw score
        score_text = font.render(str(score), True, (255, 255, 255))
        high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
        window.blit(score_text, (10, 10))
        window.blit(high_score_text, (10, 50))

        pygame.display.update()
        clock.tick(60)

    # Save high score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    # Game over screen
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        # Draw game over screen
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
        window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
        window.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
        window.blit(high_score_text, (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))

        pygame.display.update()

    pygame.quit()

# Run the game loop
game_loop()