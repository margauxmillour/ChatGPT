import pygame
import sys
import random

# Game variables
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
GRAVITY = 0.25
BIRD_JUMP = -6
SPEED = 2
GAP = 150

class Bird:
    def __init__(self, bird_image):
        self.image = bird_image
        self.x = 50
        self.y = 150
        self.speed = 0

    def update(self):
        self.speed += GRAVITY
        self.y += self.speed

    def jump(self):
        self.speed = BIRD_JUMP

class Pipe:
    def __init__(self, pipe_image, x):
        self.image = pipe_image
        self.x = x
        self.top = random.randint(50, 350)
        self.bottom = self.top + GAP
        self.passed = False  # Add this line

    def update(self):
        self.x -= SPEED

    def is_off_screen(self):
        return self.x + self.image.get_width() < 0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.bird_image = pygame.image.load('assets/bird.png').convert_alpha()
        self.pipe_image = pygame.image.load('assets/pipe.png').convert_alpha()
        self.base_image = pygame.image.load('assets/base.png').convert_alpha()
        self.background_image = pygame.image.load('assets/background.png').convert_alpha()
        self.score = 0
        self.font = pygame.font.Font(None, 36)  # creates a default font of size 36
        self.highscore = self.load_highscore()

    def start_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            self.screen.blit(self.background_image, (0, 0))
            title_text = self.font.render("Flappy Bird", True, (255, 255, 255))
            instruction_text = self.font.render("Press SPACE to start", True, (255, 255, 255))
            self.screen.blit(title_text, (WINDOW_WIDTH / 2 - title_text.get_width() / 2, WINDOW_HEIGHT / 2))
            self.screen.blit(instruction_text, (WINDOW_WIDTH / 2 - instruction_text.get_width() / 2, WINDOW_HEIGHT / 2 + 50))
            pygame.display.update()
            self.clock.tick(60)

    def game_over_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            self.screen.blit(self.background_image, (0, 0))
            game_over_text = self.font.render("Game Over", True, (255, 255, 255))
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            highscore_text = self.font.render(f"High Score: {self.highscore}", True, (255, 255, 255))
            restart_text = self.font.render("Press SPACE to restart", True, (255, 255, 255))
            self.screen.blit(game_over_text, (WINDOW_WIDTH / 2 - game_over_text.get_width() / 2, WINDOW_HEIGHT / 2))
            self.screen.blit(score_text, (WINDOW_WIDTH / 2 - score_text.get_width() / 2, WINDOW_HEIGHT / 2 + 50))
            self.screen.blit(highscore_text, (WINDOW_WIDTH / 2 - highscore_text.get_width() / 2, WINDOW_HEIGHT / 2 + 100))
            self.screen.blit(restart_text, (WINDOW_WIDTH / 2 - restart_text.get_width() / 2, WINDOW_HEIGHT / 2 + 150))
            pygame.display.update()
            self.clock.tick(60)

    def start(self):
        self.start_screen()
        self.bird = Bird(self.bird_image)
        self.pipes = [Pipe(self.pipe_image, 300)]
        while True:
            self.handle_input()
            self.update()
            self.draw()

    def game_over(self):
        self.game_over_screen()
        self.start()

    def load_highscore(self):
        try:
            with open("assets/highscore.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        with open("assets/highscore.txt", "w") as file:
            file.write(str(self.highscore))

    def start(self):
        self.start_screen()
        self.bird = Bird(self.bird_image)
        self.pipes = [Pipe(self.pipe_image, 300)]
        while True:
            self.handle_input()
            self.update()
            self.draw()
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jump()

    def update(self):
        self.bird.update()
        for pipe in self.pipes:
            pipe.update()
        if self.pipes[0].is_off_screen():
            self.pipes.pop(0)
        if not self.pipes or self.pipes[-1].x < WINDOW_WIDTH - 200:  # spawns a new pipe when the last one is 200px from the right edge
            self.pipes.append(Pipe(self.pipe_image, WINDOW_WIDTH))
        if self.bird.y <= 0 or self.bird.y + self.bird.image.get_height() >= WINDOW_HEIGHT:
            self.game_over()
        for pipe in self.pipes:
            if self.bird.x < pipe.x + pipe.image.get_width() and self.bird.x + self.bird.image.get_width() > pipe.x:
                if self.bird.y < pipe.top or self.bird.y + self.bird.image.get_height() > pipe.bottom:
                    self.game_over()
                if not pipe.passed:
                    pipe.passed = True  # Mark the pipe as passed
                    self.score += 1
                    if self.score > self.highscore:
                        self.highscore = self.score
                        self.save_highscore()
        
    def game_over(self):
        self.game_over_screen()
        self.score = 0
        self.start()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        for pipe in self.pipes:
            self.screen.blit(self.pipe_image, (pipe.x, 0), (0, 0, self.pipe_image.get_width(), pipe.top))
            self.screen.blit(self.pipe_image, (pipe.x, pipe.bottom), (0, 0, self.pipe_image.get_width(), WINDOW_HEIGHT - pipe.bottom))
        score_text = self.font.render(str(self.score), True, (255, 255, 255))  # creates a white text surface
        self.screen.blit(score_text, (WINDOW_WIDTH / 2, 10))  # draws the text at the top center of the screen
        self.screen.blit(self.bird_image, (self.bird.x, self.bird.y))
        pygame.display.update()
        self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.start()
