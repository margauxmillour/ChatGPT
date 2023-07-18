import pygame
import random
import os

# Game window size
WIDTH = 288
HEIGHT = 512

# Colors
WHITE = (255, 255, 255)

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(os.path.join('assets', 'bird.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = int(WIDTH / 2 - self.rect.width / 2)
        self.rect.y = int(HEIGHT / 2 - self.rect.height / 2)
        self.gravity = 0.5
        self.jump_power = 10
        self.jump = 0

    def update(self):
        self.jump += self.gravity
        self.rect.y += self.jump

    def flap(self):
        self.jump = -self.jump_power


# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(os.path.join('assets', 'pipe.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(-300, -100)
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()


# Base class
class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join('assets', 'base.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - self.rect.height
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < WIDTH:
            self.rect.x = 0


# Game class
class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.background = pygame.image.load(os.path.join('assets', 'background.png')).convert()
        self.font = pygame.font.Font(None, 32)
        self.score = 0
        self.highscore = 0
        self.running = True

        self.base_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.bird = Bird()
        self.base = Base()

        self.all_sprites.add(self.bird)
        self.base_group.add(self.base)

    def new_pipe(self):
        pipe = Pipe()
        self.pipe_group.add(pipe)
        self.all_sprites.add(pipe)

    def run(self):
        while self.running:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.flap()

            self.screen.blit(self.background, (0, 0))

            self.pipe_group.update()
            self.base_group.update()

            self.all_sprites.draw(self.screen)
            self.base_group.draw(self.screen)

            # Collision detection with pipes and base
            if pygame.sprite.spritecollide(self.bird, self.pipe_group, False):
                self.running = False
            if pygame.sprite.spritecollide(self.bird, self.base_group, False):
                self.running = False

            # Update score and high score
            self.score = len(self.pipe_group)

            if self.score > self.highscore:
                self.highscore = self.score

            score_text = self.font.render("Score: " + str(self.score), True, WHITE)
            highscore_text = self.font.render("High Score: " + str(self.highscore), True, WHITE)

            self.screen.blit(score_text, (10, 10))
            self.screen.blit(highscore_text, (10, 50))

            pygame.display.flip()

            # Spawn new pipe every 100 frames
            if self.score % 100 == 0:
                self.new_pipe()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()