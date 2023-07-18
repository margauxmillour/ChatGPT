import pygame
import sys
import random

class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 600))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("assets/background.png").convert()
        self.birdSprites = [pygame.image.load("assets/bird.png").convert_alpha(),
                            pygame.image.load("assets/bird2.png").convert_alpha(),
                            pygame.image.load("assets/bird3.png").convert_alpha()]
        self.wallUp = pygame.image.load("assets/pipe_bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/pipe_top.png").convert_alpha()
        self.gap = 150
        self.wallx = 400
        self.birdY = 200
        self.jump = 0
        self.jumpSpeed = 8
        self.gravity = 0.5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.running = False

        # Load the high score
        with open('assets/highscore.txt', 'r') as f:
            self.highscore = int(f.read())

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.counter += 1

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx, 360 + self.gap - self.offset + 10, self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx, 0 - self.gap - self.offset - 10, self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True
        if not 0 < self.bird[1] < 720:
            self.dead = True

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if not self.running and not self.dead:
                        self.running = True
                    elif not self.dead:
                        self.jump = 17
                        self.gravity = 5
                        self.jumpSpeed = 10
                    elif self.dead:
                        self.dead = False
                        self.running = True
                        if self.counter > self.highscore:
                            self.highscore = self.counter
                            with open('assets/highscore.txt', 'w') as f:
                                f.write(str(self.highscore))
                        self.counter = 0
                        self.birdY = 200
                        self.bird[1] = self.birdY
                        self.wallx = 400
                        self.gravity = 5

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp, (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown, (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter), -1, (255, 255, 255)), (200, 50))

            if self.dead:
                self.sprite = 2
                self.running = False
                self.screen.blit(font.render("Game Over", -1, (255, 255, 255)), (70, 250))
                self.screen.blit(font.render("High Score: " + str(self.highscore), -1, (255, 255, 255)), (70, 300))
                self.screen.blit(font.render("Press any key to play again", -1, (255, 255, 255)), (20, 350))
            elif not self.running and not self.dead:
                self.screen.blit(font.render("Flappy Bird", -1, (255, 255, 255)), (50, 250))
                self.screen.blit(font.render("Press any key to start", -1, (255, 255, 255)), (30, 300))
            else:
                if not self.dead:
                    self.sprite = 0
                self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))

            if self.running and not self.dead:
                self.updateWalls()
                self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()