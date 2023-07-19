# Flappy Bird Pygame Game

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
Below is an example of a simple implementation for your requirements using Pygame.

In this code, I assume that you have the following image assets in a "assets" directory:

- bird.png
- background.png
- base.png
- pipe.png

```python
import pygame
import sys
from pygame.locals import *

pygame.init()

FPS = 60
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((288, 512))
FONT = pygame.font.Font('freesansbold.ttf', 32)

# Load the images
BIRD_IMG = pygame.image.load('assets/bird.png')
BACKGROUND_IMG = pygame.image.load('assets/background.png')
BASE_IMG = pygame.image.load('assets/base.png')
PIPE_IMG = pygame.image.load('assets/pipe.png')

# Game parameters
GRAVITY = 1
FLAP_POWER = 9
FLAP_DELAY = 300
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)
BIRD_HEIGHT = BIRD_IMG.get_height()
PIPE_HEIGHT = PIPE_IMG.get_height()
PIPE_WIDTH = PIPE_IMG.get_width()

def draw_base(base_shift):
    SCREEN.blit(BASE_IMG, (base_shift, 450))
    SCREEN.blit(BASE_IMG, (base_shift + 288, 450))

def create_pipe():
    return {'x': 300, 'y': 200}

def move_pipes(pipes):
    for pipe in pipes:
        pipe['x'] -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        SCREEN.blit(PIPE_IMG, (pipe['x'], pipe['y']))
        SCREEN.blit(pygame.transform.flip(PIPE_IMG, False, True), (pipe['x'], pipe['y'] - PIPE_HEIGHT - 200))

def detect_collision(playerY, pipes):
    for pipe in pipes:
        if BIRD_HEIGHT + playerY > 450 or playerY < 0:
            return True
        bird_rect = pygame.Rect(50, playerY, BIRD_IMG.get_width(), BIRD_IMG.get_height())
        pipe_rect = pygame.Rect(pipe['x'], pipe['y'], PIPE_IMG.get_width(), PIPE_IMG.get_height())
        pipe_rect_flipped = pygame.Rect(pipe['x'], pipe['y'] - PIPE_HEIGHT - 200, PIPE_IMG.get_width(), PIPE_IMG.get_height())
        if bird_rect.colliderect(pipe_rect) or bird_rect.colliderect(pipe_rect_flipped):
            return True
    return False

def game_loop():
    score = 0
    high_score = 0
    base_shift = 0
    birdY = 256
    birdY_change = 0
    flap_time = 0
    pipes = [create_pipe()]

    game_active = True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if game_active:
                if event.type == KEYDOWN and event.key == K_SPACE and pygame.time.get_ticks() - flap_time > FLAP_DELAY:
                    birdY_change = 0
                    birdY_change -= FLAP_POWER
                    flap_time = pygame.time.get_ticks()

                if event.type == SPAWN_PIPE:
                    pipes.append(create_pipe())
            else:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    game_active = True
                    pipes.clear()
                    birdY = 256
                    birdY_change = 0
                    pipes = [create_pipe()]

        if game_active:
            # Bird
            birdY_change += GRAVITY
            birdY += birdY_change
            SCREEN.blit(BACKGROUND_IMG, (0,0))
            SCREEN.blit(BIRD_IMG, (50, birdY))

            # Pipes
            pipes = move_pipes(pipes)
            draw_pipes(pipes)

            # Base
            base_shift -= 1
            if base_shift <= -288:
                base_shift = 0
            draw_base(base_shift)

            # Score
            score += 1
            score_display = FONT.render('Score: ' + str(score), True, (255, 255, 255))
            SCREEN.blit(score_display, (10, 10))

            game_active = not detect_collision(birdY, pipes)
        else:
            high_score = max(high_score, score)
            score = 0
            high_score_display = FONT.render('High score: ' + str(high_score), True, (255, 255, 255))
            SCREEN.blit(high_score_display, (10, 10))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    game_loop()
```

Note: The gameplay parameters like the bird's jump power, gravity, and the pipe's spawn interval might need adjustments to make the game playable. Also, the collision detection with pipes could be improved with more advanced techniques than simple rectangle collision.


#### You:
Can you add a score and keep track of the highscore in a separate txt file?

#### ChatGPT:
Sure, here is how you can modify the code to store the high score in a separate text file.

I have created two new functions: `get_high_score()` to read the high score from the file and `update_high_score()` to write a new high score to the file. I've also updated the game loop to use these functions.

Please ensure you have the necessary permissions to read and write files in the directory where you're running this script.

```python
#...
# Here are the new functions
def get_high_score():
    try:
        with open("highscore.txt", 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def update_high_score(new_high_score):
    with open("highscore.txt", 'w') as f:
        f.write(str(new_high_score))

def game_loop():
    score = 0
    high_score = get_high_score() # updated to use get_high_score()
    base_shift = 0
    birdY = 256
    birdY_change = 0
    flap_time = 0
    pipes = [create_pipe()]

    game_active = True

    while True:
        #...
        
        if game_active:
            #...
        else:
            if score > high_score: # new condition to update high score
                high_score = score
                update_high_score(high_score)
            score = 0
            high_score_display = FONT.render('High score: ' + str(high_score), True, (255, 255, 255))
            SCREEN.blit(high_score_display, (10, 10))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    game_loop()
```

Note: This code will create a new file named `highscore.txt` in the same directory where you're running the script if it doesn't already exist. If the file already exists, it will read the high score from it and update it if you beat it. Make sure the file contains only a single integer value, otherwise, an error will occur. If the file does not exist or cannot be opened, the high score will be set to 0.


#### You:
The pipes should come by pair, one below and one on top. They should be separated by a gap to let the bird go through.

#### ChatGPT:
My apologies for the oversight. In the original code, the pipes are single and placed in the middle of the screen. Let's fix that by creating a pair of pipes for each spawn event: one at the top and one at the bottom with a gap between them.

Here's the updated code:

```python
# ...

# New constant for the gap size
PIPE_GAP_SIZE = 100

def create_pipe():
    gap_y = random.randint(100, 400)
    return [
        {'x': 300, 'y': gap_y - PIPE_HEIGHT},  # Upper pipe
        {'x': 300, 'y': gap_y + PIPE_GAP_SIZE}  # Lower pipe
    ]

def draw_pipes(pipes):
    for pair in pipes:
        for pipe in pair:
            if pipe['y'] <= 200:  # This is the upper pipe
                SCREEN.blit(pygame.transform.flip(PIPE_IMG, False, True), (pipe['x'], pipe['y']))
            else:  # This is the lower pipe
                SCREEN.blit(PIPE_IMG, (pipe['x'], pipe['y']))

def detect_collision(playerY, pipes):
    for pair in pipes:
        for pipe in pair:
            if BIRD_HEIGHT + playerY > 450 or playerY < 0:
                return True
            bird_rect = pygame.Rect(50, playerY, BIRD_IMG.get_width(), BIRD_IMG.get_height())
            pipe_rect = pygame.Rect(pipe['x'], pipe['y'], PIPE_IMG.get_width(), PIPE_IMG.get_height())
            if bird_rect.colliderect(pipe_rect):
                return True
    return False

# ...
```

Now, each time a pair of pipes is created, they are placed at a random height on the screen, and a gap of `PIPE_GAP_SIZE` pixels is created between them. The collision detection and pipe drawing functions have been updated to handle pipe pairs.


#### You:
import pygame
import sys
from pygame.locals import *
import random

pygame.init()

FPS = 60
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((288, 512))
FONT = pygame.font.Font('freesansbold.ttf', 32)

# Load the images
BIRD_IMG = pygame.image.load('assets/bird.png')
BACKGROUND_IMG = pygame.image.load('assets/background.png')
BASE_IMG = pygame.image.load('assets/base.png')
PIPE_IMG = pygame.image.load('assets/pipe.png')

# Game parameters
GRAVITY = 0.5
FLAP_POWER = 9
FLAP_DELAY = 0
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)
BIRD_HEIGHT = BIRD_IMG.get_height()
PIPE_HEIGHT = PIPE_IMG.get_height()
PIPE_WIDTH = PIPE_IMG.get_width()

def draw_base(base_shift):
    SCREEN.blit(BASE_IMG, (base_shift, 450))
    SCREEN.blit(BASE_IMG, (base_shift + 288, 450))

# New constant for the gap size
PIPE_GAP_SIZE = 150

def create_pipe():
    gap_y = random.randint(100, 350)
    return [
        {'x': 300, 'y': gap_y - PIPE_HEIGHT},  # Upper pipe
        {'x': 300, 'y': gap_y + PIPE_GAP_SIZE}  # Lower pipe
    ]

def draw_pipes(pipes):
    for pair in pipes:
        for pipe in pair:
            if pipe['y'] <= 200:  # This is the upper pipe
                SCREEN.blit(pygame.transform.flip(PIPE_IMG, False, True), (pipe['x'], pipe['y']))
            else:  # This is the lower pipe
                SCREEN.blit(PIPE_IMG, (pipe['x'], pipe['y']))

def detect_collision(playerY, pipes):
    for pair in pipes:
        for pipe in pair:
            if BIRD_HEIGHT + playerY > 450 or playerY < 0:
                return True
            bird_rect = pygame.Rect(50, playerY, BIRD_IMG.get_width(), BIRD_IMG.get_height())
            pipe_rect = pygame.Rect(pipe['x'], pipe['y'], PIPE_IMG.get_width(), PIPE_IMG.get_height())
            if bird_rect.colliderect(pipe_rect):
                return True
    return False

def move_pipes(pipes):
    for pipe in pipes:
        pipe[0]['x'] -= 3
        pipe[1]['x'] -= 3
    return pipes

def get_high_score():
    try:
        with open("highscore.txt", 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def update_high_score(new_high_score):
    with open("highscore.txt", 'w') as f:
        f.write(str(new_high_score))

def game_loop():
    score = 0
    high_score = get_high_score() # updated to use get_high_score()
    base_shift = 0
    birdY = 256
    birdY_change = 0
    flap_time = 0
    pipes = []

    game_active = True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if game_active:
                if event.type == KEYDOWN and event.key == K_SPACE and pygame.time.get_ticks() - flap_time > FLAP_DELAY:
                    birdY_change = 0
                    birdY_change -= FLAP_POWER
                    flap_time = pygame.time.get_ticks()

                if event.type == SPAWN_PIPE:
                    pipes.append(create_pipe())
            else:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    game_active = True
                    pipes.clear()
                    birdY = 256
                    birdY_change = 0
                    pipes = []

        if game_active:
            # Bird
            birdY_change += GRAVITY
            birdY += birdY_change
            SCREEN.blit(BACKGROUND_IMG, (0,0))
            SCREEN.blit(BIRD_IMG, (50, birdY))

            # Pipes
            pipes = move_pipes(pipes)
            draw_pipes(pipes)

            # Base
            base_shift -= 1
            if base_shift <= -288:
                base_shift = 0
            draw_base(base_shift)

            # Score
            score += 1
            score_display = FONT.render('Score: ' + str(score), True, (255, 255, 255))
            SCREEN.blit(score_display, (10, 10))

            game_active = not detect_collision(birdY, pipes)
        
        else:
            if score > high_score: # new condition to update high score
                high_score = score
                update_high_score(high_score)
            score = 0
            high_score_display = FONT.render('High score: ' + str(high_score), True, (255, 255, 255))
            SCREEN.blit(high_score_display, (10, 50))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    game_loop()


I would like the score to go up by one when the bird passed through a pair of pipes.

#### ChatGPT:
To increase the score when the bird successfully passes through a pair of pipes, you can add a boolean variable to each pair of pipes to keep track of whether the bird has passed through them or not. This boolean variable can be used to decide whether to increment the score or not.

Here's an example of how you can do this:

```python
# ...
def create_pipe():
    gap_y = random.randint(100, 350)
    return [
        {'x': 300, 'y': gap_y - PIPE_HEIGHT, 'passed': False},  # Upper pipe
        {'x': 300, 'y': gap_y + PIPE_GAP_SIZE, 'passed': False}  # Lower pipe
    ]
# ...

def move_pipes(pipes, birdX):
    for pipe in pipes:
        pipe[0]['x'] -= 3
        pipe[1]['x'] -= 3
        if birdX > pipe[0]['x'] + PIPE_WIDTH and not pipe[0]['passed']:
            pipe[0]['passed'] = True
            return True
    return False
# ...

def game_loop():
    score = 0
    high_score = get_high_score()  # updated to use get_high_score()
    base_shift = 0
    birdY = 256
    birdY_change = 0
    flap_time = 0
    pipes = []

    game_active = True

    while True:
        # ...

        if game_active:
            # Bird
            birdY_change += GRAVITY
            birdY += birdY_change
            SCREEN.blit(BACKGROUND_IMG, (0, 0))
            SCREEN.blit(BIRD_IMG, (50, birdY))

            # Pipes
            if move_pipes(pipes, 50):  # check if bird passed a pipe
                score += 1
            draw_pipes(pipes)

            # Base
            base_shift -= 1
            if base_shift <= -288:
                base_shift = 0
            draw_base(base_shift)

            # Score
            score_display = FONT.render('Score: ' + str(score), True, (255, 255, 255))
            SCREEN.blit(score_display, (10, 10))

            game_active = not detect_collision(birdY, pipes)

        else:
            if score > high_score:  # new condition to update high score
                high_score = score
                update_high_score(high_score)
            score = 0
            high_score_display = FONT.render('High score: ' + str(high_score), True, (255, 255, 255))
            SCREEN.blit(high_score_display, (10, 50))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
# ...
```

In the code above, we first add a 'passed' key to the pipe dictionaries when creating new pipes and initialize it to `False`. Then, in the `move_pipes` function, we check if the bird has moved beyond a pipe pair without hitting them (i.e., has passed through the pipe pair). If it has, we set the 'passed' key to `True` for that pair of pipes and return `True`. If the `move_pipes` function returns `True`, the score is incremented.


#### You:
Can you add a start screen and a game over screen?

#### ChatGPT:
Sure, to add start and game over screens, you'll need to add functions for displaying these screens. You can add text and instructions for starting/restarting the game. You'll also want to add a game state variable to track whether the game is in the start screen, main game, or game over screen state.

Here's an example of how you might do this:

```python
# ...

def draw_start_screen():
    start_screen_text = FONT.render('Press SPACE to start', True, (255, 255, 255))
    SCREEN.blit(start_screen_text, (10, 256))

def draw_game_over_screen(score, high_score):
    game_over_text = FONT.render('GAME OVER', True, (255, 255, 255))
    SCREEN.blit(game_over_text, (10, 256))
    score_display = FONT.render('Score: ' + str(score), True, (255, 255, 255))
    SCREEN.blit(score_display, (10, 300))
    high_score_display = FONT.render('High score: ' + str(high_score), True, (255, 255, 255))
    SCREEN.blit(high_score_display, (10, 350))

def game_loop():
    game_state = 'start_screen'  # can be 'start_screen', 'main_game', 'game_over_screen'
    score = 0
    high_score = get_high_score()
    base_shift = 0
    birdY = 256
    birdY_change = 0
    flap_time = 0
    pipes = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:
                if game_state == 'start_screen':
                    game_state = 'main_game'
                elif game_state == 'main_game':
                    birdY_change = 0
                    birdY_change -= FLAP_POWER
                    flap_time = pygame.time.get_ticks()
                elif game_state == 'game_over_screen':
                    game_state = 'start_screen'
                    score = 0
                    pipes = []

            if game_state == 'main_game' and event.type == SPAWN_PIPE:
                pipes.append(create_pipe())

        if game_state == 'start_screen':
            SCREEN.blit(BACKGROUND_IMG, (0, 0))
            draw_start_screen()

        elif game_state == 'main_game':
            # ... (main game code here)

        elif game_state == 'game_over_screen':
            SCREEN.blit(BACKGROUND_IMG, (0, 0))
            draw_game_over_screen(score, high_score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    game_loop()
```

In this code, we add `draw_start_screen` and `draw_game_over_screen` functions to display the start and game over screens, respectively. The `game_state` variable keeps track of the current game state, and the game logic adjusts based on this state. For example, the SPACE key now has different behaviors depending on the game state: it starts the main game from the start screen, makes the bird jump in the main game, and restarts the game from the game over screen.
