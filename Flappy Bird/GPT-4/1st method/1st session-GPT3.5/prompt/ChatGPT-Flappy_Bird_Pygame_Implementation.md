# Flappy Bird Pygame Implementation

#### You:
Create a Flappy Bird game using Pygame. The game should have the following features:

- The game window should be 288x512 pixels in size.
- The background, bird, base, and pipe assets should be loaded and displayed on the screen.
- The bird should be able to jump when the spacebar is pressed.
- Pipes should spawn at regular intervals and move from right to left.
- The bird should be able to collide with the pipes, the top/bottom of the screen, or the base.
- The score should increase when the bird successfully passes a pair of pipes.
- The game should end when the bird collides with an obstacle.
- The highest score achieved should be displayed on the screen, along with the option to restart the game.

Please provide the necessary code to implement the above features using the Pygame library.

#### ChatGPT:
I would be glad to help with that. However, please note that I can't run Pygame directly in this environment because it requires a display and user interaction. However, I can certainly help write the Python code using Pygame for the Flappy Bird game based on your requirements.

Before we proceed, make sure you have the following assets in the same directory as your Python script:

- The bird image file (let's call it "bird.png")
- The pipe image file (let's call it "pipe.png")
- The base image file (let's call it "base.png")
- The background image file (let's call it "background.png")

Here is a basic example of how you could implement a Flappy Bird game with Pygame:

```python
import pygame
import sys
import random

# Game variables
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
GRAVITY = 0.25
BIRD_JUMP = -8
SPEED = 2
GAP = 100

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

    def update(self):
        self.x -= SPEED

    def is_off_screen(self):
        return self.x + self.image.get_width() < 0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.bird_image = pygame.image.load('bird.png').convert_alpha()
        self.pipe_image = pygame.image.load('pipe.png').convert_alpha()
        self.base_image = pygame.image.load('base.png').convert_alpha()
        self.background_image = pygame.image.load('background.png').convert_alpha()
        self.score = 0

    def start(self):
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
            self.pipes.append(Pipe(self.pipe_image, self.pipes[-1].x + 200))
        if self.bird.y <= 0 or self.bird.y + self.bird.image.get_height() >= WINDOW_HEIGHT:
            self.game_over()
        for pipe in self.pipes:
            if self.bird.x < pipe.x + pipe.image.get_width() and self.bird.x + self.bird.image.get_width() > pipe.x:
                if self.bird.y < pipe.top or self.bird.y + self.bird.image.get_height() > pipe.bottom:
                    self.game_over()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        for pipe in self.pipes:
            self.screen.blit(self.pipe_image, (pipe.x, 0), (0, 0, self.pipe_image.get_width(), pipe.top))
            self.screen.blit(self.pipe_image, (pipe.x, pipe.bottom), (0, 0, self.pipe_image.get_width(), WINDOW_HEIGHT - pipe.bottom))
        self.screen.blit(self.bird_image, (self.bird.x, self.bird.y))
        pygame.display.update()
        self.clock.tick(60)

    def game_over(self):
        print("Game Over")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.start()
```

In this code:

- `Bird` class represents the bird player, with `jump` method for jumping and `update` for gravity.
- `Pipe` class represents a pair of pipes, with `update` for moving the pipes and `is_off_screen` to check if the pipe is off-screen.
- `Game` class controls the game loop, user input, game over condition, and drawing on the screen.

This is a basic version of the game. For advanced features like scoring and game restarts, you would need to add more logic to the `Game` class. Furthermore, remember to adjust the values of `WINDOW_WIDTH`, `WINDOW_HEIGHT`, `GRAVITY`, `BIRD_JUMP`, `SPEED`, and `GAP` to better suit your game's difficulty and display settings.


#### You:
Traceback (most recent call last):
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT4\sessions\Flappy_Bird_2.py", line 97, in <module>
    game.start()
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT4\sessions\Flappy_Bird_2.py", line 56, in start
    self.update()
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT4\sessions\Flappy_Bird_2.py", line 73, in update
    self.pipes.append(Pipe(self.pipe_image, self.pipes[-1].x + 200))
IndexError: list index out of range

#### ChatGPT:
The error message indicates that you are trying to access an element in the list `self.pipes` that does not exist. This happens because you are trying to access the last element of the list using `self.pipes[-1]` but you've just removed the only element in the list with `self.pipes.pop(0)` in the previous line.

Here's a quick fix: We can add a check to ensure there is at least one pipe left in the list before adding a new one.

```python
def update(self):
    self.bird.update()
    for pipe in self.pipes:
        pipe.update()
    if self.pipes[0].is_off_screen():
        self.pipes.pop(0)
        if self.pipes:  # Add this line
            self.pipes.append(Pipe(self.pipe_image, self.pipes[-1].x + 200))
    if self.bird.y <= 0 or self.bird.y + self.bird.image.get_height() >= WINDOW_HEIGHT:
        self.game_over()
    for pipe in self.pipes:
        if self.bird.x < pipe.x + pipe.image.get_width() and self.bird.x + self.bird.image.get_width() > pipe.x:
            if self.bird.y < pipe.top or self.bird.y + self.bird.image.get_height() > pipe.bottom:
                self.game_over()
```

In the above code, I've added an extra check `if self.pipes:` before appending a new pipe. This line will check if there are any pipes left in the `self.pipes` list before trying to add a new one.


#### You:
Traceback (most recent call last):
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT4\sessions\Flappy_Bird_2.py", line 99, in <module>
    game.start()
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT4\sessions\Flappy_Bird_2.py", line 56, in start
    self.update()
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT4\sessions\Flappy_Bird_2.py", line 71, in update
    if self.pipes[0].is_off_screen():
IndexError: list index out of range

#### ChatGPT:
The `IndexError: list index out of range` error is still occurring because the code is trying to access an item at index 0 of `self.pipes` list when the list could be empty, which occurs when the bird passes the first pipe and the pipe is removed from the list.

To resolve this, we need to add a check to ensure that the list is not empty before attempting to access its elements.

Here's how to fix it:

```python
def update(self):
    self.bird.update()
    for pipe in self.pipes:
        pipe.update()
    if self.pipes and self.pipes[0].is_off_screen():  # check if self.pipes list is not empty
        self.pipes.pop(0)
        if self.pipes:  # Add this line
            self.pipes.append(Pipe(self.pipe_image, self.pipes[-1].x + 200))
    if self.bird.y <= 0 or self.bird.y + self.bird.image.get_height() >= WINDOW_HEIGHT:
        self.game_over()
    for pipe in self.pipes:
        if self.bird.x < pipe.x + pipe.image.get_width() and self.bird.x + self.bird.image.get_width() > pipe.x:
            if self.bird.y < pipe.top or self.bird.y + self.bird.image.get_height() > pipe.bottom:
                self.game_over()
```

With this code, the game will first check if there are any pipes in the `self.pipes` list before trying to access its first element. If there are no pipes, it will skip to the next line, avoiding the `IndexError`.


#### You:
I would like pipes to continue appearing after the first one.

#### ChatGPT:
My apologies for the confusion, the earlier solution did not correctly handle the spawning of new pipes once the first one was removed. Here is the corrected code:

```python
def update(self):
    self.bird.update()
    for pipe in self.pipes:
        pipe.update()
    if self.pipes[0].is_off_screen():
        self.pipes.pop(0)
    if not self.pipes or self.pipes[-1].x < WINDOW_WIDTH - 200: # spawns a new pipe when the last one is 200px from the right edge
        self.pipes.append(Pipe(self.pipe_image, WINDOW_WIDTH))
    if self.bird.y <= 0 or self.bird.y + self.bird.image.get_height() >= WINDOW_HEIGHT:
        self.game_over()
    for pipe in self.pipes:
        if self.bird.x < pipe.x + pipe.image.get_width() and self.bird.x + self.bird.image.get_width() > pipe.x:
            if self.bird.y < pipe.top or self.bird.y + self.bird.image.get_height() > pipe.bottom:
                self.game_over()
```

In this updated version, the `update` method checks whether the last pipe is 200px from the right edge of the screen, and if so, it spawns a new pipe at the right edge. This ensures that new pipes continue to appear as needed.


#### You:
Can you add a score (+1 each time the bird goes through a pair of pipes), and keep track of the highscore in a separate txt file ?

#### ChatGPT:
Sure, we can add scoring to the game. Each time the bird passes through a pair of pipes, we will increment the score by 1. We will also keep track of the high score by reading from and writing to a text file.

Here's how you can modify the `Game` class to add scoring and high score tracking:

```python
class Game:
    def __init__(self):
        # ...
        self.score = 0
        self.highscore = self.load_highscore()

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.highscore))

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
        if self.bird.x > self.pipes[0].x + self.pipe_image.get_width() and len(self.pipes) > 1 and self.bird.x < self.pipes[1].x:
            self.score += 1
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()

    def game_over(self):
        print(f"Game Over. Score: {self.score}. High Score: {self.highscore}")
        pygame.quit()
        sys.exit()
```

In this updated version of the code, the `load_highscore` method reads the high score from a file named "highscore.txt". If this file does not exist or contains invalid data, it defaults to a high score of 0. The `save_highscore` method writes the current high score to the file.

The `update` method has been updated to increase the score by 1 each time the bird passes a pair of pipes. If the new score is higher than the high score, the high score is updated and saved to the file.

The `game_over` method now also prints the final score and the high score when the game ends.


#### You:
I would like the score to be displayed on the screen while playing.

#### ChatGPT:
In order to display the score on the screen, we can use Pygame's font rendering capabilities. We'll create a `font` object and then render the score onto a surface that we can blit onto the screen.

Here's how you can modify the `Game` class to add score rendering:

```python
class Game:
    def __init__(self):
        # ...
        self.score = 0
        self.font = pygame.font.Font(None, 36)  # creates a default font of size 36

    def draw(self):
        # ...
        score_text = self.font.render(str(self.score), True, (255, 255, 255))  # creates a white text surface
        self.screen.blit(score_text, (WINDOW_WIDTH / 2, 10))  # draws the text at the top center of the screen
        pygame.display.update()
        self.clock.tick(60)
```

This modified version of the `Game` class creates a `font` object in the `__init__` method. The `draw` method then uses this `font` to render the current score into a white text surface. The text surface is then blitted onto the screen at the top center.

Note: Pygame's font module needs to be initialized separately with `pygame.font.init()`, but since we're already calling `pygame.init()` in the `Game` class's `__init__` method, the font module is already initialized. If you were to use the font module without calling `pygame.init()`, you would need to call `pygame.font.init()` before creating any `font` objects.


#### You:
The score goes up by 25 when passing pipes, change it to 1

#### ChatGPT:
The score seems to be increasing by more than expected because the score increment check is being performed in the `update` method, which is being called for every game loop iteration. Therefore, while the bird is between the two pipes, the score is incrementing.

To fix this, we can add a flag to each Pipe object indicating whether it has been passed by the bird, and only increase the score the first time the bird passes a pipe. Here's how you can do this:

```python
class Pipe:
    def __init__(self, pipe_image, x):
        # ...
        self.passed = False  # Add this line

class Game:
    # ...

    def update(self):
        # ...
        for pipe in self.pipes:
            if self.bird.x > pipe.x + self.pipe_image.get_width() and not pipe.passed:
                pipe.passed = True  # Mark the pipe as passed
                self.score += 1
                if self.score > self.highscore:
                    self.highscore = self.score
                    self.save_highscore()
```

In this updated version, each Pipe object keeps track of whether it has been passed by the bird. The score is only incremented the first time the bird passes a pipe. After the pipe has been passed, the `passed` flag is set to `True` to prevent the score from being incremented again for the same pipe.


#### You:
Can you add a start screen and a game over screen ?

#### ChatGPT:
Absolutely, here is how you can add a start screen and a game over screen:

```python
class Game:
    def __init__(self):
        # ...

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

    # ...
```

In this code, `start_screen` and `game_over_screen` are two new methods that display the start screen and game over screen respectively. They both enter a new game loop where they wait for a SPACE key press to continue, displaying the appropriate messages in the meantime.

In the `start` method, `self.start_screen()` is called before the main game loop, so the start screen is displayed before the game starts.

In the `game_over` method, `self.game_over_screen()` is called and then `self.start()` is called. This means that when the game ends, the game over screen is displayed, and then the game restarts (going back to the start screen).


#### You:
You just defined functions, but nothing really changed.

#### ChatGPT:
I apologize for the confusion. The functions `start_screen` and `game_over_screen` are indeed defined, but they need to be called at the appropriate places in the game loop for the changes to be visible.

Here's how you should modify the `start` and `game_over` methods to include these screens:

```python
class Game:
    # ...

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
```

With these modifications, the game will start with the start screen, and then transition to the game over screen when the game ends. After the game over screen, the game will return to the start screen, effectively restarting the game.
