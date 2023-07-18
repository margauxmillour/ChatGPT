import pygame
import random

# Game dimensions
WIDTH = 288
HEIGHT = 512

# Bird dimensions and properties
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_FRAMES = 3
BIRD_FLAP_SPEED = 5
BIRD_JUMP_SPEED = 10
# Constants
GRAVITY = 0.75  # Adjust this value as needed
# Constants
MAX_FALL_VELOCITY = 10  # Adjust this value as needed

# Pipe dimensions and properties
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 100
PIPE_SPEED = 2
PIPE_SPAWN_TIME = 1600

# Colors
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_frames = [pygame.image.load(f"assets/bird_frame{i}.png") for i in range(1, BIRD_FRAMES + 1)]
background = pygame.image.load("assets/background.png")
pipe_image = pygame.image.load("assets/pipe.png")
start_screen = pygame.image.load("assets/start_screen.png")
game_over_screen = pygame.image.load("assets/game_over_screen.png")

# Load font
font = pygame.font.Font(None, 36)

# Load high score from file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Save high score to file
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_frames[0]
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.vel_y = 0
        self.score = 0

    def update(self):
        if flap_active:  # Check flap_active status
            self.flap()  # Call flap() method to make bird jump

        self.vel_y += GRAVITY
        self.vel_y = min(self.vel_y, MAX_FALL_VELOCITY)  # Limit maximum downward velocity
        self.rect.y += self.vel_y

        if self.rect.bottom >= HEIGHT:
            self.game_over()

    def flap(self):
        self.vel_y = -BIRD_JUMP_SPEED

    def game_over(self):
        self.rect.y = HEIGHT // 2
        self.vel_y = 0
        if self.score > load_high_score():
            save_high_score(self.score)
        self.score = 0

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.flip(pipe_image, False, True)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x -= PIPE_SPEED

        if self.rect.right <= 0:
            self.kill()
            bird.score += 1

# Group for all sprites
all_sprites = pygame.sprite.Group()

# Group for pipes
pipe_group = pygame.sprite.Group()

# Create bird
bird = Bird()
all_sprites.add(bird)

# Game loop
clock = pygame.time.Clock()
running = True
playing = False
game_over = False
flap_active = False  # New variable to track spacebar key status

while running:
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    game_over = False
                    bird.score = 0
                    pipe_group.empty()
                    bird.rect.y = HEIGHT // 2
                elif not playing:
                    playing = True
                    flap_active = True  # Set flap_active to True when spacebar is pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                flap_active = False  # Set flap_active to False when spacebar is released

    # Scroll background
    screen.blit(background, (0, 0))

    if playing:
        # Update bird
        bird.update()
        screen.blit(bird_frames[(pygame.time.get_ticks() // BIRD_FLAP_SPEED) % BIRD_FRAMES], bird.rect)

        # Generate new pipes
        if pygame.time.get_ticks() % PIPE_SPAWN_TIME == 0:
            pipe_height = random.randint(100, HEIGHT - 100 - PIPE_GAP)
            pipe_group.add(Pipe(WIDTH, pipe_height))
        
        # Update pipes
        pipe_group.update()
        pipe_group.draw(screen)

        # Collision detection
        if pygame.sprite.spritecollide(bird, pipe_group, False):
            playing = False
            game_over = True

        # Display score
        score_text = font.render(f"Score: {bird.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    elif game_over:
        # Game over screen
        screen.blit(game_over_screen, (0, 0))

        # Display score and high score
        score_text = font.render(f"Score: {bird.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
        high_score = load_high_score()
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 20))

    else:
        # Start screen
        screen.blit(start_screen, (0, 0))

        # Display high score
        high_score = load_high_score()
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()

# Quit the game
pygame.quit()