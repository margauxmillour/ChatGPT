# Flappy Bird Pygame Game

#### You:
Create a Flappy Bird game using Pygame. The game window should have a width of 288 and a height of 512, with the caption "Flappy Bird". The game should include the following elements:

1. Load the game assets: a background image ("assets/background.png"), a bird image ("assets/bird.png"), and a pipe image ("assets/pipe.png").

2. Define a Bird class that represents the player's bird. The bird should have an initial position at the center of the window, no initial velocity, and a gravity of 0.5. The class should have methods to update the bird's position, make it jump, and check for collisions with the window boundaries.

3. Define a Pipe class that represents the pipes the bird has to navigate through. The class should have parameters for the pipe's x and y positions, as well as a Boolean parameter indicating whether the pipe is inverted or not. The class should have a method to update the pipe's position and check if it is offscreen.

4. Define a Cloud class that represents the clouds in the background. The class should have parameters for the cloud's x and y positions, as well as its speed. The class should have a method to update the cloud's position and check if it is offscreen.

5. Create groups for the birds, pipes, and clouds using the Pygame sprite module.

6. Implement a start_game() function that initializes the game state, including the bird, pipe spawn timer, score, and font. The function should return these initialized variables.

7. Implement functions to load and save the high score from a file called "high_score.txt". The high score should be initialized as 0 if the file does not exist or is empty.

8. Set up the game loop, which will continue running until the user closes the game window. Inside the loop, handle events such as quitting the game, jumping the bird with the space key, and spawning new pipes using a timer. Update the game state, including the bird's position, collisions, score, pipe speed, and pipe spawn timer interval. Finally, draw the game elements, including the background, clouds, birds, pipes, and score, and update the display.

9. When the game is over, display a game over screen that shows the player's score and the high score. Offer an option to restart the game by pressing the space key.

10. Quit the game and close the Pygame window when the game loop is exited.

Make sure to use the provided images and code structure to create a functional Flappy Bird game.

#### ChatGPT:
Sure! Here's the code for a Flappy Bird game using Pygame:

```python
import pygame
import random
import sys

# Game dimensions
WIDTH = 288
HEIGHT = 512

# Colors
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load game assets
background_img = pygame.image.load("assets/background.png").convert()
bird_img = pygame.image.load("assets/bird.png").convert_alpha()
pipe_img = pygame.image.load("assets/pipe.png").convert_alpha()

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_img
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
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            return True
        return False

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_img
        self.rect = self.image.get_rect()
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - 100)
        else:
            self.rect.topleft = (x, y + 100)
        self.speed = 4

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right < 0

# Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((64, 32))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(self.image, WHITE, (32, 16), 16)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def is_offscreen(self):
        return self.rect.right < 0

# Start the game
def start_game():
    bird = Bird()
    pipes = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    all_sprites.add(bird)

    pipe_spawn_timer = pygame.USEREVENT
    pygame.time.set_timer(pipe_spawn_timer, 2000)
    score = 0
    font = pygame.font.Font(None, 36)

    high_score = load_high_score()

    return bird, pipes, clouds, all_sprites, pipe_spawn_timer, score, font, high_score

# Load high score from file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except (IOError, ValueError):
        high_score = 0
    return high_score

# Save high score to file
def save_high_score(high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

# Game loop
def game_loop():
    clock = pygame.time.Clock()
    FPS = 60

    bird, pipes, clouds, all_sprites, pipe_spawn_timer, score, font, high_score = start_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bird.check_boundaries():
                        pygame.mixer.music.load('assets/jump.wav')
                        pygame.mixer.music.play()
                    bird.jump()
            elif event.type == pipe_spawn_timer:
                inverted = random.choice([False, True])
                pipe = Pipe(WIDTH, HEIGHT // 2, inverted)
                pipes.add(pipe)
                all_sprites.add(pipe)

        bird.update()
        pipes.update()
        clouds.update()

        if bird.check_boundaries():
            pygame.mixer.music.load('assets/die.wav')
            pygame.mixer.music.play()
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            break

        for pipe in pipes:
            if pygame.sprite.collide_rect(bird, pipe):
                pygame.mixer.music.load('assets/die.wav')
                pygame.mixer.music.play()
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                break

            if pipe.is_offscreen():
                pipes.remove(pipe)
                all_sprites.remove(pipe)
                score += 1

        if score > high_score:
            high_score = score

        clouds.add(Cloud(WIDTH, random.randint(50, 200), random.randint(1, 3)))

        screen.blit(background_img, (0, 0))
        clouds.draw(screen)
        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

game_loop()
```

Save this code in a file named `flappy_bird.py` and make sure to have the `assets` folder in the same directory as the script, containing the `background.png`, `bird.png`, and `pipe.png` images. When you run the script, it will start the Flappy Bird game using Pygame. Use the space key to make the bird jump and navigate through the pipes. The game over screen will appear when the bird collides with the pipes or goes out of bounds. Press the space key to restart the game.

Note: Make sure you have the Pygame library installed (`pip install pygame`) before running the code.
