import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 288
HEIGHT = 512
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
bg_img = pygame.image.load(os.path.join('assets', 'background.png')).convert()
base_img = pygame.image.load(os.path.join('assets', 'base.png')).convert()
bird_images = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird1.png')).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird2.png')).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird3.png')).convert_alpha())
]
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'pipe.png')).convert_alpha())
# Load highscore
highscore = 0
with open('assets/highscore.txt', 'r') as file:
    highscore = int(file.read())

# Game variables
gravity = 0.25
bird_movement = 0
score = 0
pipe_spawn_time = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn_time, 1500)
pipes = []

# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img_index = 0
        self.img = bird_images[self.img_index]
        self.rect = self.img.get_rect(center=(self.x, self.y))

    def flap(self):
        self.img_index = (self.img_index + 1) % 3
        self.img = bird_images[self.img_index]
    
    def move(self):
        self.rect.centery += bird_movement

    def draw(self):
        win.blit(self.img, self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    def __init__(self, x, y, inverted=False):
        self.x = x
        self.y = y
        self.inverted = inverted
        if inverted:
            self.img = pygame.transform.flip(pipe_img, False, True)
        else:
            self.img = pipe_img
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.rect.x -= 2

    def draw(self):
        win.blit(self.img, self.rect)

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.img)
        bottom_mask = pygame.mask.from_surface(pipe_img)
        top_offset = (self.rect.x - bird.rect.x, self.rect.y - round(bird.rect.y))
        bottom_offset = (self.rect.x - bird.rect.x, self.rect.y + self.rect.height - round(bird.rect.y))
        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        if t_point or b_point:
            return True
        return False


def draw_window(bird, pipes, base, score, highscore):
    win.blit(bg_img, (0, 0))
    for pipe in pipes:
        pipe.draw()
    base_x = base.get_width()
    win.blit(base_img, (base_x, HEIGHT - base.get_height()))
    win.blit(base_img, (0, HEIGHT - base.get_height()))
    bird.draw()
    pygame.draw.rect(win, (255, 255, 255), (10, 10, 60, 40))
    score_text = pygame.font.Font(None, 36).render(str(score), True, (0, 0, 0))
    win.blit(score_text, (20, 20))
    highscore_text = pygame.font.Font(None, 24).render("Highscore: " + str(highscore), True, (255, 255, 255))
    win.blit(highscore_text, (WIDTH - highscore_text.get_width() - 20, 20))
    pygame.display.update()


def main():
    global bird_movement, score, highscore

    bird = Bird(WIDTH/2 - bird_images[0].get_width()/2, HEIGHT/2)
    base = pygame.transform.scale2x(base_img)

    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_movement = -8
                    bird.flap()
                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    bird_movement = 0
                    bird.y = HEIGHT/2
                    pipes.clear()
                    score = 0
                    pygame.time.set_timer(pipe_spawn_time, 1500)

            if event.type == pipe_spawn_time and not game_over:
                random_y = random.choice([150, 200, 250, 300, 350])
                pipes.append(Pipe(WIDTH, random_y))
                if len(pipes) >= 10:
                    pipes.pop(0)

        if not game_over:
            bird_movement += gravity
            bird.move()

            for pipe in pipes:
                pipe.move()
                if pipe.collide(bird):
                    game_over = True
                    if score > highscore:
                        highscore = score
                        with open('assets/highscore.txt', 'w') as file:
                            file.write(str(highscore))
                    pygame.time.set_timer(pipe_spawn_time, 0)

            if bird.rect.bottom >= HEIGHT - base.get_height():
                game_over = True
                if score > highscore:
                    highscore = score
                    with open('assets/highscore.txt', 'w') as file:
                        file.write(str(highscore))
                pygame.time.set_timer(pipe_spawn_time, 0)

            for pipe in pipes:
                if pipe.rect.x <= -pipe.rect.width:
                    pipes.remove(pipe)
                if pipe.rect.x == bird.rect.x:
                    score += 1

        draw_window(bird, pipes, base, score, highscore)


if __name__ == '__main__':
    main()