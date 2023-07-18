# Flappy Bird Pygame Implementation

#### You:
Create a Flappy Bird game using Pygame. The game window should have a width of 288 and a height of 512, with the caption "Flappy Bird". The game should include the following elements: 
1. Load the game assets: a background image ("assets/background.png"), a bird image ("assets/bird.png"), a pipe image ("assets/pipe.png"), and a cloud image (“assets/cloud.png”). 
2. Define a Bird class that represents the player's bird. The bird should have an initial position at the center of the window, no initial velocity, and a gravity of 0.5. The class should have methods to update the bird's position, make it jump, and check for collisions with the window boundaries. 
3. Define a Pipe class that represents the pipes the bird has to navigate through. The class should have parameters for the pipe's x and y positions, as well as a Boolean parameter indicating whether the pipe is inverted or not. The class should have a method to update the pipe's position and check if it is offscreen. 
4. Define a Cloud class that represents the clouds in the background. The class should have parameters for the cloud's x and y positions, as well as its speed. The class should have a method to update the cloud's position and check if it is offscreen. 
5. Create groups for the birds, pipes, and clouds using the Pygame sprite module. 
6. Implement a start_game() function that initializes the game state, including the bird, pipe spawn timer, score, and font. The function should return these initialized variables. 
7. Implement functions to load and save the high score from a file called "high_score.txt". The high score should be initialized as 0 if the file does not exist or is empty. 
8. Set up the game loop, which will continue running until the user closes the game window. Inside the loop, handle events such as quitting the game, jumping the bird with the space key, and spawning new pipes using a timer. Update the game state, including the bird's position, collisions, score, pipe speed, and pipe spawn timer interval. Finally, draw the game elements, including the background, clouds, birds, pipes, and score, and update the display. 
9. When the game is over, display a game over screen that shows the player's score and the high score. Offer an option to restart the game by pressing the space key. 
10. Quit the game and close the Pygame window when the game loop is exited. Make sure to use the provided images and code structure to create a functional Flappy Bird game.

#### ChatGPT:
Sure! Here's an implementation of the Flappy Bird game using Pygame:

```python
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH = 288
HEIGHT = 512

# Caption
pygame.display.set_caption("Flappy Bird")

# Load game assets
background = pygame.image.load("assets/background.png")
bird_image = pygame.image.load("assets/bird.png")
pipe_image = pygame.image.load("assets/pipe.png")
cloud_image = pygame.image.load("assets/cloud.png")

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = 0
        self.gravity = 0.5

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -8

    def check_boundaries(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            return True
        elif self.rect.top <= 0:
            self.rect.top = 0
        return False

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        super().__init__()
        self.image = pygame.transform.flip(pipe_image, False, inverted)
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.speed = 4

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right <= 0

# Cloud class
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

def start_game():
    bird = Bird()
    pipes = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    all_sprites.add(bird)

    score = 0
    pipe_spawn_timer = pygame.USEREVENT
    pygame.time.set_timer(pipe_spawn_timer, 1500)

    font = pygame.font.Font(None, 40)

    return bird, pipes, clouds, all_sprites, score, pipe_spawn_timer, font

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except (IOError, ValueError):
        high_score = 0
    return high_score

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

def game_over(screen, score, high_score):
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialize game variables
bird, pipes, clouds, all_sprites, score, pipe_spawn_timer, font = start_game()
high_score = load_high_score()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
        elif event.type == pipe_spawn_timer:
            pipe_x = WIDTH + 10
            pipe_y = random.randint(200, 400)
            pipe = Pipe(pipe_x, pipe_y)
            inverted_pipe = Pipe(pipe_x, pipe_y - 400, inverted=True)
            pipes.add(pipe, inverted_pipe)
            all_sprites.add(pipe, inverted_pipe)

    bird.update()
    bird.check_boundaries()

    pipes.update()
    clouds.update()

    for pipe in pipes:
        if pipe.is_offscreen():
            pipes.remove(pipe)
            all_sprites.remove(pipe)
            score += 1

    for cloud in clouds:
        if cloud.is_offscreen():
            clouds.remove(cloud)
            all_sprites.remove(cloud)

    collided_pipes = pygame.sprite.spritecollide(bird, pipes, False)
    if collided_pipes or bird.check_boundaries():
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        game_over(screen, score, high_score)
        bird, pipes, clouds, all_sprites, score, pipe_spawn_timer, font = start_game()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 50))

    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
```

Make sure to have the `assets` folder with the required images (`background.png`, `bird.png`, `pipe.png`, `cloud.png`) in the same directory as the script.
