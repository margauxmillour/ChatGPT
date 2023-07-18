# Flappy Bird Game Script

#### You:
Could you help me write a Python script using the Pygame library to create a simple Flappy Bird game? I would like the game to have these features:

    A game window with a size of 288x512.
    Use images for the background, base, bird, and pipes. The images are located in a folder named 'assets'.
    The bird should fall down due to gravity and be able to jump up when a key is pressed.
    The pipes should move from right to left and spawn every 1.5 seconds. The gap between the top and bottom pipes should be 150 pixels.
    Keep track of the score, incrementing it by 1 every time the bird successfully passes through a pair of pipes.
    The game should be able to end if the bird hits a pipe or goes off the top or bottom of the screen.
    Display a 'Game Over' message and the final score when the game ends.
    The game should be restartable by pressing a key.
    Store the high score in a text file and display it on the game over screen. If the current game's score is higher than the high score, update the high score.
    The speed of the pipes and the frequency at which they spawn should increase as the score increases, up to a certain limit.

#### ChatGPT:
Sure, I can help you write the Python script using Pygame to create a simple Flappy Bird game. However, there are a few considerations I want to outline:

1. This is a non-trivial project and will involve a substantial amount of code. We'll need to break it down into manageable components and tackle each one separately.
2. As I can't access your local file system, I can't directly test the script. Therefore, I recommend testing the code on your local machine after we write each component to ensure it works as expected. I'll guide you on how to do that.
3. The images for the bird, background, base, and pipes should be in PNG format and located in a folder named 'assets' in the same directory as the Python script.
4. We'll use a text file to store the high score. This file will be created in the same directory as the Python script.

Let's start with the basic setup of Pygame and creating a window for the game.

```python
import pygame
import sys
import random

# Game Variables
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
GRAVITY = 1
BIRD_JUMP = 8
GAME_SPEED = 2
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # Milliseconds
HIGH_SCORE_FILE = "high_score.txt"

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

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_background()
        draw_base()
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
```

This script initializes the Pygame library, sets up the game window, and loads the assets. In the main loop, it listens for the QUIT event (which occurs when you close the game window) and then draws the background and base on each frame.

Please try running this script on your local machine and let me know if it works as expected. Make sure your Python environment has the `pygame` package installed and the 'assets' folder is in the same directory as your script.

In the next steps, we can add the bird, gravity, and the ability for the bird to jump.


#### You:
Can you continue with the next steps?

#### ChatGPT:
Absolutely! Now we'll add the bird to our game, apply gravity, and add the functionality for the bird to jump.

To accomplish this, we'll need to:

1. Define a `Bird` class that represents our bird. This class will contain methods to draw the bird, make it jump, and update its position according to gravity.
2. In the main game loop, listen for a KEYDOWN event which will occur when the player presses a key. If a key is pressed, make the bird jump.
3. Continually update the bird's position and redraw it on the screen.

Let's add these parts to the code:

```python
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

def main():
    bird_instance = Bird()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                bird_instance.jump()

        bird_instance.update()
        draw_background()
        bird_instance.draw(screen)
        draw_base()
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
```

In the `main` function, we first create an instance of the `Bird` class. Then, within the main game loop, we check if any key has been pressed. If it has, we call the `jump` method of the `Bird` class which causes the bird to move upwards. We call the `update` method of the `Bird` class on each frame to update the bird's position. Finally, we draw the bird on the screen at its updated position.

Please add these changes to the script and run it on your local machine. You should now see a bird that falls due to gravity and jumps up when you press any key. Let me know if it works as expected and if you encounter any issues. In the next steps, we can add the pipes and the collision logic.


#### You:
Can you continue with the next steps?

#### ChatGPT:
Sure! Now let's add the pipes to our game and implement the collision logic.

To achieve this, we'll need to:

1. Define a `Pipe` class that represents a pair of pipes. This class will contain methods to draw the pipes, update their position, and check if the bird has collided with the pipes.
2. Create a Pygame `USEREVENT` that spawns a new pair of pipes every 1.5 seconds.
3. In the main game loop, listen for this event and create a new `Pipe` object whenever it occurs.
4. Continually update the pipes' positions and redraw them on the screen.
5. Check if the bird has collided with any of the pipes. If a collision has occurred, end the game.

Here is how you can do it:

```python
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.gap_y = random.randint(80, SCREEN_HEIGHT - 80 - PIPE_GAP)
        self.passed = False

    def draw(self, screen):
        screen.blit(pipe, (self.x, SCREEN_HEIGHT - self.gap_y))
        screen.blit(pygame.transform.flip(pipe, False, True), (self.x, self.gap_y - PIPE_GAP - pipe.get_height()))

    def update(self):
        self.x -= GAME_SPEED

    def collide(self, bird):
        return pygame.Rect(self.x, 0, pipe.get_width(), self.gap_y).colliderect(pygame.Rect(bird.x, bird.y, bird.get_width(), bird.get_height())) or pygame.Rect(self.x, self.gap_y + PIPE_GAP, pipe.get_width(), SCREEN_HEIGHT - self.gap_y - PIPE_GAP).colliderect(pygame.Rect(bird.x, bird.y, bird.get_width(), bird.get_height()))

def main():
    bird_instance = Bird()
    pipes = []
    pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)

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
            if pipe.collide(bird_instance):
                # Game Over
                return
        draw_background()
        for pipe in pipes:
            pipe.draw(screen)
        bird_instance.draw(screen)
        draw_base()
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
```

In the `main` function, we first create an empty list to store our `Pipe` objects. We then create a new `USEREVENT` that triggers every 1.5 seconds. In the main game loop, we check if this event has occurred, and if it has, we create a new `Pipe` object and add it to our list. We then update each pipe's position, check if the bird has collided with the pipe, and draw the pipe on the screen.

Please add these changes to the script and run it on your local machine. You should now see pipes appearing from the right side of the screen and moving towards the left. If the bird collides with a pipe, the game will end. Let me know if it works as expected and if you encounter any issues. In the next steps, we can add the score and high score functionality.


#### You:
Traceback (most recent call last):
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT-4\1st method\prompt 4\1st session\code\Flappy_Bird.py", line 101, in <module>
    main()
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT-4\1st method\prompt 4\1st session\code\Flappy_Bird.py", line 89, in main
    if pipe.collide(bird_instance):
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT-4\1st method\prompt 4\1st session\code\Flappy_Bird.py", line 69, in collide
    return pygame.Rect(self.x, 0, pipe.get_width(), self.gap_y).colliderect(pygame.Rect(bird.x, bird.y, bird.get_width(), bird.get_height())) or pygame.Rect(self.x, self.gap_y + PIPE_GAP, pipe.get_width(), SCREEN_HEIGHT - self.gap_y - PIPE_GAP).colliderect(pygame.Rect(bird.x, bird.y, bird.get_width(), bird.get_height()))
AttributeError: 'Bird' object has no attribute 'get_width'

#### ChatGPT:
I apologize for the confusion. The `Bird` object is a custom object and doesn't have the `get_width` or `get_height` methods like a Pygame Surface does. We should be using the width and height of the `bird` image, not the `Bird` object. Here's how to fix this:

In the `collide` method of the `Pipe` class, replace the calls to `bird.get_width()` and `bird.get_height()` with `bird.get_width()` and `bird.get_height()`, respectively. The corrected `collide` method should look like this:

```python
def collide(self, bird):
    bird_rect = pygame.Rect(bird.x, bird.y, bird.get_width(), bird.get_height())
    upper_pipe_rect = pygame.Rect(self.x, 0, pipe.get_width(), self.gap_y)
    lower_pipe_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP, pipe.get_width(), SCREEN_HEIGHT - self.gap_y - PIPE_GAP)
    return upper_pipe_rect.colliderect(bird_rect) or lower_pipe_rect.colliderect(bird_rect)
```

And in the `Bird` class, add two methods to return the width and height of the bird image:

```python
def get_width(self):
    return bird.get_width()

def get_height(self):
    return bird.get_height()
```

Please make these changes and run the script again. Let me know if you still encounter any issues.


#### You:
There is a problem with the collisions, the game ends even though I'm not touching the pipes

#### ChatGPT:
The collision issue might be due to the fact that the bird and pipe images possibly have transparent areas. The collision detection might be considering the full rectangle of the image including the transparent areas, which can lead to the appearance of a collision even though the bird does not visually appear to be touching the pipe.

To solve this, we could adjust the rectangles used for collision detection to better fit the visible parts of the bird and pipe images. However, this would require knowing the exact dimensions and positions of the visible parts, which can be difficult to determine without seeing the images.

As a simpler solution, we can add a buffer around the bird's collision rectangle to reduce the likelihood of a collision being detected when the bird is near, but not touching, a pipe. Here's how you can modify the `collide` method in the `Pipe` class:

```python
def collide(self, bird):
    bird_rect = pygame.Rect(bird.x + 5, bird.y + 5, bird.get_width() - 10, bird.get_height() - 10)
    upper_pipe_rect = pygame.Rect(self.x, 0, pipe.get_width(), self.gap_y)
    lower_pipe_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP, pipe.get_width(), SCREEN_HEIGHT - self.gap_y - PIPE_GAP)
    return upper_pipe_rect.colliderect(bird_rect) or lower_pipe_rect.colliderect(bird_rect)
```

In this version, I've added a buffer of 5 pixels on all sides of the bird's collision rectangle by adding 5 to the x and y coordinates and subtracting 10 from the width and height. You can adjust these values as needed to best fit your specific bird and pipe images.

Please try making these changes and let me know if it improves the collision detection.


#### You:
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
HIGH_SCORE_FILE = "high_score.txt"

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

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x + 5, bird.y + 5, bird.get_width() - 10, bird.get_height() - 10)
        upper_pipe_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.gap_y - PIPE_GAP - pipe.get_height(), pipe.get_width(), pipe.get_height())
        lower_pipe_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.gap_y, pipe.get_width(), SCREEN_HEIGHT - self.gap_y - PIPE_GAP)
        return upper_pipe_rect.colliderect(bird_rect) or lower_pipe_rect.colliderect(bird_rect)

def main():
    bird_instance = Bird()
    pipes = []
    pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)

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
            if pipe.collide(bird_instance):
                # Game Over
                return
        draw_background()
        for pipe in pipes:
            pipe.draw(screen)
        bird_instance.draw(screen)
        draw_base()
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()


Can you add a start screen and a game over screen?

#### ChatGPT:
Sure, we can add a start screen and a game over screen.

Let's begin by creating two new functions: `start_screen()` and `game_over_screen()`. We'll call `start_screen()` before the game loop starts, and `game_over_screen()` when the game ends.

```python
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

def game_over_screen():
    screen.blit(font.render('Game Over', True, (255, 255, 255)), (50, SCREEN_HEIGHT // 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
```

In `start_screen()`, we display the text 'Press Any Key to Start' and wait for the player to press any key. Once a key is pressed, we return from the function and the game starts.

In `game_over_screen()`, we display the text 'Game Over' and wait for the player to press any key. Once a key is pressed, we return from the function and the game can be restarted.

Now, we can modify our `main()` function to call `start_screen()` at the beginning and `game_over_screen()` when the game ends:

```python
def main():
    start_screen()
    bird_instance = Bird()
    pipes = []
    pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)

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
            if pipe.collide(bird_instance):
                game_over_screen()
                return
        draw_background()
        for pipe in pipes:
            pipe.draw(screen)
        bird_instance.draw(screen)
        draw_base()
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    while True:
        main()
```

Now when you run the game, you should see a start screen before the game begins and a game over screen when the game ends. After the game over screen, the game will restart. Please let me know if this works for you or if you need further assistance.


#### You:
Can you add a score and keep track of the highscore in a separate txt file?

#### ChatGPT:
Sure, we can add scoring to the game and keep track of the high score in a separate text file.

Here's how we can do it:

1. Add a `score` variable in the `main()` function to keep track of the current score.
2. When a pipe moves past the bird (i.e., when the x-coordinate of the pipe is less than that of the bird), increment the score by 1.
3. Display the current score on the screen during the game.
4. When the game ends, compare the current score with the high score (stored in a text file). If the current score is higher, update the high score in the file.
5. Display the high score on the game over screen.

Here's how we can modify the code to add these features:

```python
def get_high_score():
    with open(HIGH_SCORE_FILE, "r") as f:
        return int(f.read().strip())

def set_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

class Pipe:
    ...
    def update(self):
        self.x -= GAME_SPEED
        if self.x + pipe.get_width() < 0:
            self.passed = True
    ...

def main():
    start_screen()
    bird_instance = Bird()
    pipes = []
    pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)
    score = 0

    while True:
        for event in pygame.event.get():
            ...
            if event.type == pygame.USEREVENT:
                pipes.append(Pipe())

        bird_instance.update()
        for pipe in pipes:
            pipe.update()
            if not pipe.passed and pipe.x + pipe.get_width() < bird_instance.x:
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

if __name__ == "__main__":
    with open(HIGH_SCORE_FILE, "a+") as f:  # Create the high score file if it doesn't exist
        pass
    while True:
        main()
```

In this code, we first add a `score` variable in the `main()` function. We increment `score` by 1 whenever a pipe moves past the bird. We then display the current score on the screen during the game. When the game ends, we compare the current score with the high score (stored in a text file). If the current score is higher, we update the high score in the file. We then display the high score on the game over screen.

Make sure to replace the ellipsis (...) with the existing code. Please try this out and let me know if it works for you or if you need further assistance.


#### You:
Traceback (most recent call last):
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT-4\1st method\prompt 4\1st session\code\Flappy_Bird.py", line 158, in <module>
    main()
  File "c:\Users\marga\Desktop\ChatGPT\Flappy Bird\GPT-4\1st method\prompt 4\1st session\code\Flappy_Bird.py", line 136, in main
    if not pipe.passed and pipe.x + pipe.get_width() < bird_instance.x:
AttributeError: 'Pipe' object has no attribute 'get_width'

#### ChatGPT:
I apologize for the oversight. Like before, the `Pipe` object doesn't have a `get_width` method, so we should use the width of the `pipe` image instead. Here's the corrected line:

```python
if not pipe.passed and pipe.x + pipe.get_width() < bird_instance.x:
```

should be replaced with:

```python
if not pipe.passed and pipe.x + pipe.get_width() < bird_instance.x:
```

In addition, I notice another potential issue. The `pipe.x` value in the `collide` method of the `Pipe` class should represent the left edge of the pipe. Hence, the collision with the upper pipe is not correctly calculated.

Please replace the following line in the `collide` method:

```python
upper_pipe_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.gap_y - PIPE_GAP - pipe.get_height(), pipe.get_width(), pipe.get_height())
```

with:

```python
upper_pipe_rect = pygame.Rect(self.x, 0, pipe.get_width(), self.gap_y)
```

Please make these changes and try running the script again. Let me know if you still encounter any issues.
