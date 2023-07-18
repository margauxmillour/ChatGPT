import pygame
import random
import os

# Assets folder path
ASSETS_PATH = "assets"

# Game window size
WIDTH, HEIGHT = 288, 512

# Colors
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
pygame.font.init()

# Window setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join(ASSETS_PATH, "bird1.png")))),
               pygame.transform.scale2x(pygame.image.load(os.path.join(ASSETS_PATH, "bird2.png")))),
               pygame.transform.scale2x(pygame.image.load(os.path.join(ASSETS_PATH, "bird3.png"))))]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join(ASSETS_PATH, "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join(ASSETS_PATH, "base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join(ASSETS_PATH, "bg.png"))))

FONT = pygame.font.Font(None, 40)

# Bird class
class Bird:
    IMAGES = BIRD_IMAGES
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.IMAGES[0]
        
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        self.tick_count += 1
        
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2
        
        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -= 2
            
        self.y += displacement
        
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.ROTATION_VELOCITY:
                self.tilt = self.ROTATION_VELOCITY
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY
                
    def draw(self):
        self.image_count += 1
        
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.IMAGES[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.image = self.IMAGES[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.image = self.IMAGES[1]
        elif self.image_count == self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0
            
        if self.tilt <= -80:
            self.image = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME * 2
            
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topLeft=(self.x, self.y)).center)
        WIN.blit(rotated_image, new_rect.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

# Pipe class
class Pipe:
    GAP = 200
    VELOCITY = 5
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_pipe = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.bottom_pipe = PIPE_IMAGE
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(50, 450)
        
    def move(self):
        self.x -= self.VELOCITY
        
    def draw(self):
        WIN.blit(self.top_pipe, (self.x, self.height - self.top_pipe.get_height()))
        WIN.blit(self.bottom_pipe, (self.x, self.height + self.GAP))
        
    def collision(self, bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_pipe_mask = pygame.mask.from_surface(self.bottom_pipe)
        
        top_offset = (self.x - bird.x, self.height - round(bird.y))
        bottom_offset = (self.x - bird.x, self.height + self.GAP - round(bird.y))
        
        t_point = bird_mask.overlap(top_pipe_mask, top_offset)
        b_point = bird_mask.overlap(bottom_pipe_mask, bottom_offset)
        
        if t_point or b_point:
            return True
        
        return False

# Base class
class Base:
    VELOCITY = 5
    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
            
    def draw(self):
        WIN.blit(self.IMAGE, (self.x1, self.y))
        WIN.blit(self.IMAGE, (self.x2, self.y))
        
def draw_window(bird, pipes, base, score, high_score):
    WIN.blit(BACKGROUND_IMAGE, (0, 0))
    
    for pipe in pipes:
        pipe.draw()
        
    text = FONT.render("Score: " + str(score), 1, BLACK)
    WIN.blit(text, (WIDTH - 10 - text.get_width(), 10))
    
    text = FONT.render("High Score: " + str(high_score), 1, BLACK)
    WIN.blit(text, (10, 10))
    
    base.draw()
    
    bird.draw()
    
    pygame.display.update()

def main():
    bird = Bird(50, 200)
    base = Base(450)
    pipes = [Pipe(400)]
    
    clock = pygame.time.Clock()
    
    score = 0
    high_score = 0
    running = True
    
    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        
        bird.move()
        
        add_pipe = False
        remove_pipes = []
        
        for pipe in pipes:
            if pipe.collision(bird):
                running = False
                if score > high_score:
                    high_score = score
                break
            
            if pipe.x + pipe.top_pipe.get_width() < 0:
                remove_pipes.append(pipe)
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
                
            pipe.move()
            
        if add_pipe:
            score += 1
            pipes.append(Pipe(400))
            
        for pipe in remove_pipes:
            pipes.remove(pipe)
            
        if bird.y + bird.image.get_height() >= 450:  # game over if bird hits the base
            running = False
            if score > high_score:
                high_score = score
                
        base.move()
        draw_window(bird, pipes, base, score, high_score)

if __name__ == "__main__":
    main()