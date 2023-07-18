# Flappy Bird Game

#### You:
Write a code in python. There is a bird ('bird.png') centered on the left side of the screen. The bird falls slowly due to gravity, but can flap its wings and rise a determined height when the spacebar is pressed. Use the pygame library. The window size should be 800x600. Don't forget to implement a clock.

#### ChatGPT:
Sure! Here's an example code that implements the described functionality using the Pygame library:

```python
import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load bird image
bird_image = pygame.image.load("bird.png")

# Set bird initial position
bird_x = window_width // 4  # Centered on the left side
bird_y = window_height // 2

# Set bird motion variables
bird_y_velocity = 0
gravity = 0.25
flap_height = -5

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_velocity = flap_height

    # Update bird position
    bird_y_velocity += gravity
    bird_y += bird_y_velocity

    # Clear the window
    window.fill((255, 255, 255))

    # Draw bird
    window.blit(bird_image, (bird_x, bird_y))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
```

Make sure you have the Pygame library installed and have the `bird.png` image file in the same directory as the Python script. You can adjust the window size, bird motion variables, and other parameters as needed.


#### You:
Now, can you add animations and rotation to the bird? I have 3 frames : 'bird1.png', 'bird2.png' and 'bird3.png'. Don't make it too fast.

#### ChatGPT:
Certainly! Here's an updated version of the code that includes animations and rotation for the bird:

```python
import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load bird images
bird_frames = [
    pygame.image.load("bird1.png"),
    pygame.image.load("bird2.png"),
    pygame.image.load("bird3.png")
]

# Set bird initial position
bird_x = window_width // 4  # Centered on the left side
bird_y = window_height // 2

# Set bird motion variables
bird_y_velocity = 0
gravity = 0.25
flap_height = -5

# Animation variables
animation_frame = 0
animation_speed = 0.15  # Delay between animation frames

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_velocity = flap_height

    # Update bird position
    bird_y_velocity += gravity
    bird_y += bird_y_velocity

    # Animation logic
    animation_frame += animation_speed
    if animation_frame >= len(bird_frames):
        animation_frame = 0

    # Rotate bird image based on velocity
    bird_image = pygame.transform.rotate(bird_frames[int(animation_frame)], bird_y_velocity * -3)

    # Clear the window
    window.fill((255, 255, 255))

    # Draw bird
    window.blit(bird_image, (bird_x, bird_y))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
```

This version of the code loads the bird frames as a list of images. The animation logic iterates through the frames based on the `animation_frame` variable, and the bird image is rotated based on the bird's vertical velocity. You can adjust the animation speed and rotation factor to achieve the desired visual effect.


#### You:
Now, I would like to add pipes. For now, don't bother with collisions. They come by pair, one at the top ('pipe_top.png') and one at the bottom ('pipe_bottom.png'). They are separated by a gap which size is 5 times the bird's height. This gap is placed at a random height. The pipes appear on the right side of the screen, move from right to left, and disappear once they reach the left side. One pair of pipes appear every 2 seconds. Be careful with the randint function, the first argument must be less than the second.

#### ChatGPT:
Sure! Let's add the pipes to the game. We'll create a class for the pipes, and every 2 seconds, a new pair of pipes will be generated at a random height. The pipes will then move from right to left across the screen, and once they reach the left side, they will be removed.

Here's the updated code:

```python
import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load bird images
bird_frames = [
    pygame.image.load("bird1.png"),
    pygame.image.load("bird2.png"),
    pygame.image.load("bird3.png")
]

# Load pipe images
pipe_top_image = pygame.image.load("pipe_top.png")
pipe_bottom_image = pygame.image.load("pipe_bottom.png")

# Set bird initial position
bird_x = window_width // 4  # Centered on the left side
bird_y = window_height // 2

# Set bird motion variables
bird_y_velocity = 0
gravity = 0.25
flap_height = -5

# Animation variables
animation_frame = 0
animation_speed = 0.15  # Delay between animation frames

# Pipe variables
pipe_width = 100
pipe_gap = 5 * bird_frames[0].get_height()  # Gap size is 5 times the bird's height
pipe_spawn_timer = 0
pipes = []

class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y

    def move(self):
        self.x -= 2  # Move the pipe from right to left

    def draw(self):
        # Draw top pipe
        window.blit(pipe_top_image, (self.x, self.gap_y - pipe_top_image.get_height()))

        # Draw bottom pipe
        bottom_pipe_y = self.gap_y + pipe_gap
        window.blit(pipe_bottom_image, (self.x, bottom_pipe_y))

def spawn_pipe():
    gap_y = random.randint(100, window_height - pipe_gap - 100)  # Random height for the gap
    new_pipe = Pipe(window_width, gap_y)
    pipes.append(new_pipe)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_velocity = flap_height

    # Update bird position
    bird_y_velocity += gravity
    bird_y += bird_y_velocity

    # Animation logic
    animation_frame += animation_speed
    if animation_frame >= len(bird_frames):
        animation_frame = 0

    # Rotate bird image based on velocity
    bird_image = pygame.transform.rotate(bird_frames[int(animation_frame)], bird_y_velocity * -3)

    # Clear the window
    window.fill((255, 255, 255))

    # Draw pipes
    for pipe in pipes:
        pipe.move()
        pipe.draw()

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe.x > -pipe_width]

    # Spawn new pipes every 2 seconds
    pipe_spawn_timer += 1
    if pipe_spawn_timer >= 120:
        spawn_pipe()
        pipe_spawn_timer = 0

    # Draw bird
    window.blit(bird_image, (bird_x, bird_y))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
```

In this code, we added a `Pipe` class to represent each pipe. The class has methods to move and draw the pipe on the screen. The `spawn_pipe()` function generates a new pipe pair at a random height.

The pipes are stored in a list called `pipes`. In each iteration of the game loop, we move and draw each pipe, and then remove any pipes that have moved off the screen. We also have a `pipe_spawn_timer` variable that counts the number of iterations, and when it reaches 120 (corresponding to 2 seconds at 60 frames per second), a new pipe pair is spawned.

Note that we're not handling collisions in this version of the code. Let me know if you would like to add collision detection as well.


#### You:
Now can you add collisions? When the birds collides either with the ground or the pipes, the game ends.

#### ChatGPT:
Certainly! Let's add collision detection to the game. We'll check for collisions between the bird and the pipes as well as between the bird and the ground. If a collision occurs, the game will end.

Here's the updated code:

```python
import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load bird images
bird_frames = [
    pygame.image.load("bird1.png"),
    pygame.image.load("bird2.png"),
    pygame.image.load("bird3.png")
]

# Load pipe images
pipe_top_image = pygame.image.load("pipe_top.png")
pipe_bottom_image = pygame.image.load("pipe_bottom.png")

# Set bird initial position
bird_x = window_width // 4  # Centered on the left side
bird_y = window_height // 2

# Set bird motion variables
bird_y_velocity = 0
gravity = 0.25
flap_height = -5

# Animation variables
animation_frame = 0
animation_speed = 0.15  # Delay between animation frames

# Pipe variables
pipe_width = 100
pipe_gap = 5 * bird_frames[0].get_height()  # Gap size is 5 times the bird's height
pipe_spawn_timer = 0
pipes = []

class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y

    def move(self):
        self.x -= 2  # Move the pipe from right to left

    def draw(self):
        # Draw top pipe
        window.blit(pipe_top_image, (self.x, self.gap_y - pipe_top_image.get_height()))

        # Draw bottom pipe
        bottom_pipe_y = self.gap_y + pipe_gap
        window.blit(pipe_bottom_image, (self.x, bottom_pipe_y))

def spawn_pipe():
    gap_y = random.randint(100, window_height - pipe_gap - 100)  # Random height for the gap
    new_pipe = Pipe(window_width, gap_y)
    pipes.append(new_pipe)

# Ground variables
ground_height = 50

# Game over flag
game_over = False

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_y_velocity = flap_height

    # Update bird position
    if not game_over:
        bird_y_velocity += gravity
        bird_y += bird_y_velocity

    # Animation logic
    animation_frame += animation_speed
    if animation_frame >= len(bird_frames):
        animation_frame = 0

    # Rotate bird image based on velocity
    bird_image = pygame.transform.rotate(bird_frames[int(animation_frame)], bird_y_velocity * -3)

    # Clear the window
    window.fill((255, 255, 255))

    # Draw pipes
    for pipe in pipes:
        pipe.move()
        pipe.draw()

        # Check for collision with pipes
        if pipe.x < bird_x + bird_image.get_width() and bird_x < pipe.x + pipe_width:
            if bird_y < pipe.gap_y or bird_y + bird_image.get_height() > pipe.gap_y + pipe_gap:
                game_over = True

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe.x > -pipe_width]

    # Spawn new pipes every 2 seconds
    if not game_over:
        pipe_spawn_timer += 1
        if pipe_spawn_timer >= 120:
            spawn_pipe()
            pipe_spawn_timer = 0

    # Check for collision with ground
    if bird_y + bird_image.get_height() > window_height - ground_height:
        game_over = True

    # Draw bird
    window.blit(bird_image, (bird_x, bird_y))

    # Draw ground
    pygame.draw.rect(window, (0, 255, 0), (0, window_height - ground_height, window_width, ground_height))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
```

In this version, we added a `game_over` flag to track whether the game has ended or not. If `game_over` is `True`, the bird will stop moving, and collision detection will no longer be performed.

We added collision detection logic within the pipe loop to check if the bird collides with any of the pipes. If a collision is detected, the `game_over` flag is set to `True`. We also added a collision check with the ground by comparing the bird's position with the ground's position. If the bird touches the ground, the `game_over` flag is set to `True`.

After updating the display, we continue to check if the game is over before spawning new pipes or updating the bird's position.

I hope this helps! Let me know if you have any further questions.


#### You:
I have 'base.png' for the ground, replace it.

#### ChatGPT:
Certainly! To replace the ground with the 'base.png' image, you can modify the code as follows:

```python
import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load bird images
bird_frames = [
    pygame.image.load("bird1.png"),
    pygame.image.load("bird2.png"),
    pygame.image.load("bird3.png")
]

# Load pipe images
pipe_top_image = pygame.image.load("pipe_top.png")
pipe_bottom_image = pygame.image.load("pipe_bottom.png")

# Load base image
base_image = pygame.image.load("base.png")

# Set bird initial position
bird_x = window_width // 4  # Centered on the left side
bird_y = window_height // 2

# Set bird motion variables
bird_y_velocity = 0
gravity = 0.25
flap_height = -5

# Animation variables
animation_frame = 0
animation_speed = 0.15  # Delay between animation frames

# Pipe variables
pipe_width = 100
pipe_gap = 5 * bird_frames[0].get_height()  # Gap size is 5 times the bird's height
pipe_spawn_timer = 0
pipes = []

class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y

    def move(self):
        self.x -= 2  # Move the pipe from right to left

    def draw(self):
        # Draw top pipe
        window.blit(pipe_top_image, (self.x, self.gap_y - pipe_top_image.get_height()))

        # Draw bottom pipe
        bottom_pipe_y = self.gap_y + pipe_gap
        window.blit(pipe_bottom_image, (self.x, bottom_pipe_y))

def spawn_pipe():
    gap_y = random.randint(100, window_height - pipe_gap - 100)  # Random height for the gap
    new_pipe = Pipe(window_width, gap_y)
    pipes.append(new_pipe)

# Game over flag
game_over = False

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_y_velocity = flap_height

    # Update bird position
    if not game_over:
        bird_y_velocity += gravity
        bird_y += bird_y_velocity

    # Animation logic
    animation_frame += animation_speed
    if animation_frame >= len(bird_frames):
        animation_frame = 0

    # Rotate bird image based on velocity
    bird_image = pygame.transform.rotate(bird_frames[int(animation_frame)], bird_y_velocity * -3)

    # Clear the window
    window.fill((255, 255, 255))

    # Draw pipes
    for pipe in pipes:
        pipe.move()
        pipe.draw()

        # Check for collision with pipes
        if pipe.x < bird_x + bird_image.get_width() and bird_x < pipe.x + pipe_width:
            if bird_y < pipe.gap_y or bird_y + bird_image.get_height() > pipe.gap_y + pipe_gap:
                game_over = True

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe.x > -pipe_width]

    # Spawn new pipes every 2 seconds
    if not game_over:
        pipe_spawn_timer += 1
        if pipe_spawn_timer >= 120:
            spawn_pipe()
            pipe_spawn_timer = 0

    # Check for collision with ground
    if bird_y + bird_image.get_height() > window_height - base_image.get_height():
        game_over = True

    # Draw base (ground)
    base_x = 0
    base_y = window_height - base_image.get_height()
    window.blit(base_image, (base_x, base_y))

    # Draw bird
    window.blit(bird_image, (bird_x, bird_y))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
```

In this code, I added the `base_image` variable and loaded the 'base.png' image using `pygame.image.load()`. The base image is then blitted at the bottom of the screen within the game loop.

Now, the 'base.png' image will be displayed as the ground in the game.

Let me know if you have any more questions!


#### You:
Can you add a score system? When the bird crosses the gap between a pair of pipes, the score should be incremented by one.

#### ChatGPT:
Certainly! Let's add a score system to keep track of the player's score. The score will be incremented each time the bird successfully crosses a pair of pipes.

Here's the updated code with the score system:

```python
import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load bird images
bird_frames = [
    pygame.image.load("bird1.png"),
    pygame.image.load("bird2.png"),
    pygame.image.load("bird3.png")
]

# Load pipe images
pipe_top_image = pygame.image.load("pipe_top.png")
pipe_bottom_image = pygame.image.load("pipe_bottom.png")

# Load base image
base_image = pygame.image.load("base.png")

# Set bird initial position
bird_x = window_width // 4  # Centered on the left side
bird_y = window_height // 2

# Set bird motion variables
bird_y_velocity = 0
gravity = 0.25
flap_height = -5

# Animation variables
animation_frame = 0
animation_speed = 0.15  # Delay between animation frames

# Pipe variables
pipe_width = 100
pipe_gap = 5 * bird_frames[0].get_height()  # Gap size is 5 times the bird's height
pipe_spawn_timer = 0
pipes = []

# Score variables
score = 0
score_font = pygame.font.Font(None, 36)

class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y

    def move(self):
        self.x -= 2  # Move the pipe from right to left

    def draw(self):
        # Draw top pipe
        window.blit(pipe_top_image, (self.x, self.gap_y - pipe_top_image.get_height()))

        # Draw bottom pipe
        bottom_pipe_y = self.gap_y + pipe_gap
        window.blit(pipe_bottom_image, (self.x, bottom_pipe_y))

def spawn_pipe():
    gap_y = random.randint(100, window_height - pipe_gap - 100)  # Random height for the gap
    new_pipe = Pipe(window_width, gap_y)
    pipes.append(new_pipe)

# Game over flag
game_over = False

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_y_velocity = flap_height

    # Update bird position
    if not game_over:
        bird_y_velocity += gravity
        bird_y += bird_y_velocity

    # Animation logic
    animation_frame += animation_speed
    if animation_frame >= len(bird_frames):
        animation_frame = 0

    # Rotate bird image based on velocity
    bird_image = pygame.transform.rotate(bird_frames[int(animation_frame)], bird_y_velocity * -3)

    # Clear the window
    window.fill((255, 255, 255))

    # Draw pipes
    for pipe in pipes:
        pipe.move()
        pipe.draw()

        # Check for collision with pipes
        if pipe.x < bird_x + bird_image.get_width() and bird_x < pipe.x + pipe_width:
            if bird_y < pipe.gap_y or bird_y + bird_image.get_height() > pipe.gap_y + pipe_gap:
                game_over = True

        # Check if bird passed the pipe
        if not game_over and bird_x == pipe.x + pipe_width:
            score += 1

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe.x > -pipe_width]

    # Spawn new pipes every 2 seconds
    if not game_over:
        pipe_spawn_timer += 1
        if pipe_spawn_timer >= 120:
            spawn_pipe()
            pipe_spawn_timer = 0

    # Check for collision with ground
    if bird_y + bird_image.get_height() > window_height - base_image.get_height():
        game_over = True

    # Draw base (ground)
    base_x = 0
    base_y = window_height - base_image.get_height()
    window.blit(base_image, (base_x, base_y))

    # Draw bird
    window.blit(bird_image, (bird_x, bird_y))

    # Draw score
    score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
```

In this code, we added a `score` variable to keep track of the player's score. Each time the bird passes through a pair of pipes, the score is incremented by one.

Within the pipe loop, after checking for a collision with the pipes, we added a condition to check if the bird's `bird_x` position is equal to the `pipe.x` position plus the width of the pipe. If it is, it means the bird has successfully passed the pipe, and we increment the score.

Lastly, we added the rendering of the score using a font object (`score_font`) and blit it onto the window surface at coordinates (10, 10).

Now, the score will be displayed on the screen, and it will increment each time the bird successfully crosses a pair of pipes.

Let me know if you have any more questions!


#### You:
Can you add a start screen and a game over screen? The start screen should appear when the player opens the game, and it should be written on it 'Press space to start'. The game over screen should appear when the player loses, and it should be written on it the score and 'Press space to start'.

#### ChatGPT:
Certainly! Let's add a start screen and a game over screen to enhance the user experience.

Here's the updated code with the start screen and game over screen:

```python
import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird")

# Load bird images
bird_frames = [
    pygame.image.load("bird1.png"),
    pygame.image.load("bird2.png"),
    pygame.image.load("bird3.png")
]

# Load pipe images
pipe_top_image = pygame.image.load("pipe_top.png")
pipe_bottom_image = pygame.image.load("pipe_bottom.png")

# Load base image
base_image = pygame.image.load("base.png")

# Set bird initial position
bird_x = window_width // 4  # Centered on the left side
bird_y = window_height // 2

# Set bird motion variables
bird_y_velocity = 0
gravity = 0.25
flap_height = -5

# Animation variables
animation_frame = 0
animation_speed = 0.15  # Delay between animation frames

# Pipe variables
pipe_width = 100
pipe_gap = 5 * bird_frames[0].get_height()  # Gap size is 5 times the bird's height
pipe_spawn_timer = 0
pipes = []

# Score variables
score = 0
score_font = pygame.font.Font(None, 36)

# Game over flag
game_over = False

# Start screen flag
start_screen = True

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start_screen or game_over:
                    # Reset game state
                    start_screen = False
                    game_over = False
                    bird_y = window_height // 2
                    bird_y_velocity = 0
                    score = 0
                    pipes.clear()
                else:
                    bird_y_velocity = flap_height

    # Update bird position
    if not start_screen and not game_over:
        bird_y_velocity += gravity
        bird_y += bird_y_velocity

    # Animation logic
    animation_frame += animation_speed
    if animation_frame >= len(bird_frames):
        animation_frame = 0

    # Rotate bird image based on velocity
    bird_image = pygame.transform.rotate(bird_frames[int(animation_frame)], bird_y_velocity * -3)

    # Clear the window
    window.fill((255, 255, 255))

    if start_screen:
        # Draw start screen text
        start_text = score_font.render("Press SPACE to start", True, (0, 0, 0))
        text_width = start_text.get_width()
        text_height = start_text.get_height()
        window.blit(start_text, (window_width // 2 - text_width // 2, window_height // 2 - text_height // 2))
    elif game_over:
        # Draw game over screen text
        game_over_text = score_font.render("Game Over", True, (0, 0, 0))
        score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))
        text_width = game_over_text.get_width()
        text_height = game_over_text.get_height()
        score_width = score_text.get_width()
        score_height = score_text.get_height()
        window.blit(game_over_text, (window_width // 2 - text_width // 2, window_height // 2 - text_height))
        window.blit(score_text, (window_width // 2 - score_width // 2, window_height // 2 + text_height))

    else:
        # Draw pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()

            # Check for collision with pipes
            if pipe.x < bird_x + bird_image.get_width() and bird_x < pipe.x + pipe_width:
                if bird_y < pipe.gap_y or bird_y + bird_image.get_height() > pipe.gap_y + pipe_gap:
                    game_over = True

            # Check if bird passed the pipe
            if bird_x == pipe.x + pipe_width:
                score += 1

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x > -pipe_width]

        # Spawn new pipes every 2 seconds
        pipe_spawn_timer += 1
        if pipe_spawn_timer >= 120:
            spawn_pipe()
            pipe_spawn_timer = 0

        # Check for collision with ground
        if bird_y + bird_image.get_height() > window_height - base_image.get_height():
            game_over = True

        # Draw base (ground)
        base_x = 0
        base_y = window_height - base_image.get_height()
        window.blit(base_image, (base_x, base_y))

        # Draw bird
        window.blit(bird_image, (bird_x, bird_y))

        # Draw score
        score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))
        window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
```

In this code, I added a `start_screen` flag to control the visibility of the start screen. When the player starts the game or when the game is over, pressing the spacebar will reset the game state and clear the pipes. The `bird_y` position and `bird_y_velocity` are reset to their initial values. The `score` variable is also reset to 0.

Within the game loop, if `start_screen` is `True`, the start screen text is rendered and displayed on the screen. If `game_over` is `True`, the game over screen text along with the score is rendered and displayed.

If neither `start_screen` nor `game_over` is `True`, the regular gameplay continues, with the pipes moving, collision detection being performed, and the score being updated and displayed.

Let me know if you have any more questions!
