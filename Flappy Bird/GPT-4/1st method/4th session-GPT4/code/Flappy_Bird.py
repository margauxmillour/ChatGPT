import pygame
import sys
import random

# Game Variables
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
GRAVITY = 1
BIRD_JUMP = 8
GAME_SPEED = 5
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # Milliseconds
HIGH_SCORE_FILE = "assets/high_score.txt"

# Pygame Initialization
pygame.init()

# Game Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game Clock
clock = pygame.time.Clock()

# Game Over Font
font = pygame.font.Font(None, 50)

# Load Assets
bg = pygame.image.load('assets/background.png')
base = pygame.image.load('assets/base.png')
bird = pygame.image.load('assets/bird.png')
pipe = pygame.image.load('assets/pipe.png')

def draw_base():
    screen.blit(base, (0, SCREEN_HEIGHT - base.get_height()))

def draw_background():
    screen.blit(bg, (0, 0))

def get_high_score():
    with open(HIGH_SCORE_FILE, "r") as f:
        return int(f.read().strip())

def set_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def start_screen():
    screen.blit(font.render('Press Any Key to Start', True, (255, 255, 255)), (20, SCREEN_HEIGHT // 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def game_over_screen(score, high_score):
    screen.blit(font.render('Game Over', True, (255, 255, 255)), (50, SCREEN_HEIGHT // 2 - 50))
    screen.blit(font.render('Score: ' + str(score), True, (255, 255, 255)), (50, SCREEN_HEIGHT // 2))
    screen.blit(font.render('High Score: ' + str(high_score), True, (255, 255, 255)), (50, SCREEN_HEIGHT // 2 + 50))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return


class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.speed = 0

    def jump(self):
        self.speed = -BIRD_JUMP

    def update(self):
        self.speed += GRAVITY
        self.y += self.speed

    def draw(self, screen):
        screen.blit(bird, (self.x, self.y))
    
    def get_width(self):
        return bird.get_width()

    def get_height(self):
        return bird.get_height()


class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.gap_y = random.randint(80, SCREEN_HEIGHT - 80 - PIPE_GAP)
        self.passed = False

    def draw(self, screen):
        screen.blit(pipe, (self.x, SCREEN_HEIGHT - self.gap_y))
        screen.blit(pygame.transform.flip(pipe, False, True), (self.x, SCREEN_HEIGHT - self.gap_y - PIPE_GAP - pipe.get_height()))

    def update(self):
        self.x -= GAME_SPEED
        if self.x + pipe.get_width() < 0:
            self.passed = True

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x + 5, bird.y + 5, bird.get_width() - 10, bird.get_height() - 10)
        upper_pipe_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.gap_y - PIPE_GAP - pipe.get_height(), pipe.get_width(), pipe.get_height())
        lower_pipe_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.gap_y, pipe.get_width(), SCREEN_HEIGHT - self.gap_y - PIPE_GAP)
        return upper_pipe_rect.colliderect(bird_rect) or lower_pipe_rect.colliderect(bird_rect) or bird_rect.top < 0 or bird_rect.bottom > SCREEN_HEIGHT - base.get_height()

def main():
    pipe_img = pygame.image.load('assets/pipe.png')
    start_screen()
    bird_instance = Bird()
    pipes = []
    pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)
    score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                bird_instance.jump()
            if event.type == pygame.USEREVENT:
                pipes.append(Pipe())

        bird_instance.update()
        for pipe in pipes:
            pipe.update()
            if not pipe.passed and pipe.x + pipe_img.get_width() < bird_instance.x:
                pipe.passed = True
                score += 1
            if pipe.collide(bird_instance):
                high_score = get_high_score()
                if score > high_score:
                    set_high_score(score)
                game_over_screen(score, high_score)
                return
        draw_background()
        for pipe in pipes:
            pipe.draw(screen)
        bird_instance.draw(screen)
        screen.blit(font.render(str(score), True, (255, 255, 255)), (SCREEN_WIDTH // 2, 50))
        draw_base()
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    with open(HIGH_SCORE_FILE, "a+") as f:  # Create the high score file if it doesn't exist
        pass
    while True:
        main()
