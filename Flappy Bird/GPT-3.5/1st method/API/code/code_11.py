import pygame
import random
import os

pygame.init()

# Game window dimensions
WIDTH = 288
HEIGHT = 512

# Define colors
WHITE = (255, 255, 255)

# Load assets
ASSETS_PATH = "assets"
BG_IMG = pygame.image.load(os.path.join(ASSETS_PATH, "background.png"))
BIRD_IMG = pygame.image.load(os.path.join(ASSETS_PATH, "bird.png"))
PIPE_IMG = pygame.image.load(os.path.join(ASSETS_PATH, "pipe.png"))
BASE_IMG = pygame.image.load(os.path.join(ASSETS_PATH, "base.png"))
FONT = pygame.font.Font(None, 40)

# Set up game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = BIRD_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vel_y = 0

    def update(self):
        self.vel_y += 1
        self.rect.y += self.vel_y

    def flap(self):
        self.vel_y = -10


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = PIPE_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x -= 5

    def is_offscreen(self):
        return self.rect.right < 0


def collision_detection(bird, pipes):
    if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT - 50:
        return True
    for pipe in pipes:
        if bird.rect.colliderect(pipe.rect): 
            return True
    return False


def show_score(score):
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def show_highscore(highscore):
    highscore_text = FONT.render(f"Highscore: {highscore}", True, WHITE)
    screen.blit(highscore_text, (10, 50))


def game_over(score, highscore):
    game_over_text = FONT.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    show_score(score)
    show_highscore(highscore)
    pygame.display.flip()
    pygame.time.wait(2000)


def main():
    running = True
    bird = Bird()
    
    pipes = pygame.sprite.Group()
    spawn_pipe_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_pipe_event, 2000)
    score = 0
    highscore = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
            elif event.type == spawn_pipe_event:
                pipe_y = random.randint(200, 400)
                pipes.add(Pipe(WIDTH, pipe_y))
        
        bird.update()
        pipes.update()
        
        # Check for collisions
        if collision_detection(bird, pipes):
            if score > highscore:
                highscore = score
            game_over(score, highscore)
            bird.rect.center = (WIDTH // 2, HEIGHT // 2)
            bird.vel_y = 0
            pipes.empty()
            score = 0
        
        # Remove offscreen pipes
        for pipe in pipes:
            if pipe.is_offscreen():
                pipes.remove(pipe)
        
        # Check for passing pipes
        for pipe in pipes:
            if pipe.rect.right < bird.rect.centerx and not pipe.rect.right < bird.rect.centerx - 5:
                score += 1
        
        screen.blit(BG_IMG, (0, 0))
        bird_group = pygame.sprite.Group(bird)
        bird_group.draw(screen)
        pipes.draw(screen)
        screen.blit(BASE_IMG, (0, HEIGHT - 50))
        show_score(score)
        show_highscore(highscore)
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()