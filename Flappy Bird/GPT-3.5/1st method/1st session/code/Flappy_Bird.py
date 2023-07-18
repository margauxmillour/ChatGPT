import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH = 288
HEIGHT = 512

# Game assets
BACKGROUND_IMAGE = "assets/background.png"
BIRD_IMAGE = "assets/bird.png"
PIPE_IMAGE = "assets/pipe.png"
FONT_STYLE = "Arial"
FONT_SIZE = 40

# Bird properties
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_GRAVITY = 0.5
BIRD_FLAP_POWER = 6

# Pipe properties
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 150
PIPE_SPEED = 2

# Cloud properties
CLOUD_WIDTH = 64
CLOUD_HEIGHT = 32
CLOUD_SPEED = 1

# Initialize the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load game assets
background_image = pygame.image.load(BACKGROUND_IMAGE).convert()
bird_image = pygame.image.load(BIRD_IMAGE).convert_alpha()
pipe_image = pygame.image.load(PIPE_IMAGE).convert_alpha()

# Create game clock
clock = pygame.time.Clock()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = 0

    def update(self):
        self.velocity += BIRD_GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -BIRD_FLAP_POWER

    def check_boundaries(self):
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            return True
        return False


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted):
        super().__init__()
        self.image = pygame.transform.flip(pipe_image, False, inverted)
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.bottomleft = (x, y - PIPE_GAP // 2)
        else:
            self.rect.topleft = (x, y + PIPE_GAP // 2)

    def update(self):
        self.rect.x -= PIPE_SPEED

    def is_offscreen(self):
        return self.rect.right < 0


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((CLOUD_WIDTH, CLOUD_HEIGHT))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        pygame.draw.ellipse(self.image, (200, 200, 200), self.image.get_rect())
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right < 0


def start_game():
    bird = Bird()
    pipes = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.LayeredUpdates()
    all_sprites.add(bird)

    # Initialize game state
    score = 0
    pipe_spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(pipe_spawn_timer, 1500)
    font = pygame.font.SysFont(FONT_STYLE, FONT_SIZE, bold=True)
    high_score = load_high_score()

    return bird, pipes, clouds, all_sprites, score, pipe_spawn_timer, font, high_score


def load_high_score():
    try:
        with open("assets/high_score.txt", "r") as file:
            high_score = int(file.read())
    except (FileNotFoundError, ValueError):
        high_score = 0
    return high_score


def save_high_score(high_score):
    with open("assets/high_score.txt", "w") as file:
        file.write(str(high_score))


def draw_score(score, high_score, font):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)
    window.blit(score_text, score_rect)

    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect()
    high_score_rect.topright = (WIDTH - 10, 10)
    window.blit(high_score_text, high_score_rect)


def game_over(score, high_score, font):
    game_over_font = pygame.font.SysFont(FONT_STYLE, FONT_SIZE * 2, bold=True)
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
    window.blit(game_over_text, game_over_rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.center = (WIDTH // 2, HEIGHT // 2 + 10)
    window.blit(score_text, score_rect)

    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect()
    high_score_rect.center = (WIDTH // 2, HEIGHT // 2 + 60)
    window.blit(high_score_text, high_score_rect)

    restart_text = font.render("Press SPACE to restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect()
    restart_rect.center = (WIDTH // 2, HEIGHT // 2 + 120)
    window.blit(restart_text, restart_rect)


def main():
    bird, pipes, clouds, all_sprites, score, pipe_spawn_timer, font, high_score = start_game()

    running = True
    game_over_flag = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over_flag:
                        bird.jump()
                    else:
                        bird, pipes, clouds, all_sprites, score, pipe_spawn_timer, font, high_score = start_game()
                        game_over_flag = False
            elif event.type == pipe_spawn_timer:
                if not game_over_flag:
                    pipe_x = WIDTH
                    pipe_y = random.randint(100, HEIGHT - 100)
                    pipe = Pipe(pipe_x, pipe_y, False)
                    inverted_pipe = Pipe(pipe_x, pipe_y, True)
                    pipes.add(pipe, inverted_pipe)
                    all_sprites.add(pipe, inverted_pipe)

        if not game_over_flag:
            # Update bird
            bird.update()
            if bird.check_boundaries():
                game_over_flag = True

            # Update pipes
            pipes.update()
            for pipe in pipes:
                if pipe.is_offscreen():
                    pipes.remove(pipe)
                    all_sprites.remove(pipe)
                    score += 1

            # Update clouds
            clouds.update()
            for cloud in clouds:
                if cloud.is_offscreen():
                    clouds.remove(cloud)
                    all_sprites.remove(cloud)

            # Check for collisions
            if pygame.sprite.spritecollideany(bird, pipes):
                game_over_flag = True

            # Update display
            window.blit(background_image, (0, 0))
            all_sprites.draw(window)
            draw_score(score, high_score, font)

        if game_over_flag:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            game_over(score, high_score,font)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
