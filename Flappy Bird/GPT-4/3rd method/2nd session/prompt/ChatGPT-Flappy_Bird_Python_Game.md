# Flappy Bird Python Game

#### You:
Write a Flappy Bird game in python.

#### ChatGPT:
Creating a Flappy Bird game involves graphical rendering and user interaction, which is outside the scope of a text-based environment. However, I can provide you with a simple code snippet on how you can implement a Flappy Bird game using the Pygame module in Python.

```python
import pygame
import sys

class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 600))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("background.png").convert()
        self.birdSprites = [pygame.image.load("bird.png").convert_alpha(),
                            pygame.image.load("bird2.png").convert_alpha(),
                            pygame.image.load("bird3.png").convert_alpha()]
        self.wallUp = pygame.image.load("bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 200
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = 0

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = self.gap * random.uniform(-0.2, 0.2)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True
        if not 0 < self.bird[1] < 720:
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))
            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
```

This script creates a basic Flappy Bird game, where a bird moves through a scrolling environment and the player must avoid the walls by jumping. The bird jumps when a key is pressed and falls under gravity when no key is pressed. If the bird hits a wall or goes off the screen, the game resets.

Please note that you would need to replace the placeholder images ("background.png", "bird.png", "bird2.png", "bird3.png", "bottom.png", "top.png") with actual images to run this game.

Remember that running this code would require a local Python environment with the `pygame` library installed, as it cannot be run within this text-based environment.


#### You:
Can you add a start screen and a game over screen?

#### ChatGPT:
Sure, I can add a start screen and a game over screen. Here's how you can add these features to the Flappy Bird game:

```python
import pygame
import sys
import random

class FlappyBird:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        self.bird = pygame.Rect(65, 50, 50, 50)
        # You will need to have these images in the same directory as your Python script.
        self.background = pygame.image.load("background.png").convert()
        self.birdSprites = [pygame.image.load("bird1.png").convert_alpha(),
                            pygame.image.load("bird2.png").convert_alpha(),
                            pygame.image.load("bird3.png").convert_alpha()]
        self.wallUp = pygame.image.load("bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 200
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.running = True

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.offset = random.randint(-110, 110)

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
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and not self.dead and self.running:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp, (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown, (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter), -1, (255, 255, 255)), (200, 50))

            if self.dead:
                self.sprite = 2
                self.screen.blit(font.render("Game Over", -1, (255, 255, 255)), (70, 250))
                self.screen.blit(font.render("Press R to restart", -1, (255, 255, 255)), (50, 300))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.dead = False

            elif not self.running:
                self.screen.blit(font.render("Flappy Bird", -1, (255, 255, 255)), (70, 250))
                self.screen.blit(font.render("Press SPACE to start", -1, (255, 255, 255)), (35, 300))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.running = True

            else:
                if not self.dead:
                    self.sprite = 0
                self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))

            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
```

This script now features a start screen that displays the game title and prompts the player to press the spacebar to start the game. Additionally, it includes a game over screen that informs the player that the game has ended and prompts them to press 'R' to restart the game.

Please replace "bird1.png", "bird2.png", "bird3.png", "background.png", "bottom.png", "top.png" with the actual paths to your image files.

Again, remember that this code can't be run in this text-based environment. You need to run this on your local machine with Python and pygame installed.


#### You:
There's no start screen.

#### ChatGPT:
Apologies for the confusion earlier. Let's make a more explicit start and game over screen. The idea is to have a main game loop that shows a start screen until the user presses a key, then runs the game, then shows a game over screen until the user presses a key, and then loops back to the start screen.

Here's an updated version of the code:

```python
import pygame
import sys
import random

class FlappyBird:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        self.bird = pygame.Rect(65, 50, 50, 50)
        # You will need to have these images in the same directory as your Python script.
        self.background = pygame.image.load("background.png").convert()
        self.birdSprites = [pygame.image.load("bird1.png").convert_alpha(),
                            pygame.image.load("bird2.png").convert_alpha(),
                            pygame.image.load("bird3.png").convert_alpha()]
        self.wallUp = pygame.image.load("bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 200
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.running = False

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.offset = random.randint(-110, 110)

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
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and not self.dead:
                    if not self.running:
                        self.running = True
                    else:
                        self.jump = 17
                        self.gravity = 5
                        self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp, (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown, (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter), -1, (255, 255, 255)), (200, 50))

            if self.dead:
                self.sprite = 2
                self.running = False
                self.screen.blit(font.render("Game Over", -1, (255, 255, 255)), (70, 250))
                self.screen.blit(font.render("Press any key to play again", -1, (255, 255, 255)), (20, 300))
            elif not self.running:
                self.screen.blit(font.render("Flappy Bird", -1, (255, 255, 255)), (50, 250))
                self.screen.blit(font.render("Press any key to start", -1, (255, 255, 255)), (30, 300))
            else:
                if not self.dead:
                    self.sprite = 0
                self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))

            if self.running:
                self.updateWalls()
                self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
```

This version of the game will start with a start screen that displays "Flappy Bird" and "Press any key to start". When any key is pressed, the game will start. When the bird hits a wall or the ground, the game will end, and the game over screen will be displayed with "Game Over" and "Press any key to play again". When any key is pressed on the game over screen, the game will restart with the start screen.

Again, replace "bird1.png", "bird2.png", "bird3.png", "background.png", "bottom.png", "top.png" with the actual paths to your image files.

Please remember that this code can't be run in this text-based environment. You need to run this on your local machine with Python and pygame installed.


#### You:
The score system doesn't work anymore, and I can't play again.

#### ChatGPT:
My apologies for the oversight. Let's fix the issue with the score system and the ability to play again. The scoring system can be updated when the bird successfully passes through the walls. Also, we need to reset certain game variables when the game ends to ensure that the game can be played again.

Here's the updated code:

```python
import pygame
import sys
import random

class FlappyBird:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        self.bird = pygame.Rect(65, 50, 50, 50)
        # You will need to have these images in the same directory as your Python script.
        self.background = pygame.image.load("background.png").convert()
        self.birdSprites = [pygame.image.load("bird1.png").convert_alpha(),
                            pygame.image.load("bird2.png").convert_alpha(),
                            pygame.image.load("bird3.png").convert_alpha()]
        self.wallUp = pygame.image.load("bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 200
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.running = False

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
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.gravity = 5

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
                    if not self.running:
                        self.running = True
                    elif not self.dead:
                        self.jump = 17
                        self.gravity = 5
                        self.jumpSpeed = 10
                    elif self.dead:
                        self.dead = False
                        self.birdY = 200
                        self.wallx = 400
                        self.counter = 0
                        self.bird[1] = self.birdY

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp, (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown, (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter), -1, (255, 255, 255)), (200, 50))

            if self.dead:
                self.sprite = 2
                self.running = False
                self.screen.blit(font.render("Game Over", -1, (255, 255, 255)), (70, 250))
                self.screen.blit(font.render("Press any key to play again", -1, (255, 255, 255)), (20, 300))
            elif not self.running:
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
```

In this version of the game, the score increases by 1 each time the bird successfully passes through a set of walls. When the bird hits a wall or the ground, the game ends, and the score is reset to 0. The game over screen is displayed with "Game Over" and "Press any key to play again". When any key is pressed on the game over screen, the game restarts from the start screen.

Again, replace "bird1.png", "bird2.png", "bird3.png", "background.png", "bottom.png", "top.png" with the actual paths to your image files.

Please remember that this code can't be run in this text-based environment. You need to run this on your local machine with Python and pygame installed.


#### You:
I still can't play again, when I press a key, nothing happens.

#### ChatGPT:
Apologies for the oversight. The issue is that the event loop was not correctly capturing the keyboard event after the game over screen. Here's the corrected code:

```python
import pygame
import sys
import random

class FlappyBird:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("background.png").convert()
        self.birdSprites = [pygame.image.load("bird1.png").convert_alpha(),
                            pygame.image.load("bird2.png").convert_alpha(),
                            pygame.image.load("bird3.png").convert_alpha()]
        self.wallUp = pygame.image.load("bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 200
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.running = False

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
                        self.birdY = 200
                        self.bird[1] = self.birdY
                        self.wallx = 400
                        self.counter = 0
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
                self.screen.blit(font.render("Press any key to play again", -1, (255, 255, 255)), (20, 300))
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
```

This updated version of the code should fix the issues with the scoring system and the ability to replay the game. When the bird hits a wall or the ground, the game ends, and the score is reset to 0. The game over screen is displayed with "Game Over" and "Press any key to play again". When any key is pressed on the game over screen, the game restarts from the start screen.

Again, replace "bird1.png", "bird2.png", "bird3.png", "background.png", "bottom.png", "top.png" with the actual paths to your image files.

Please remember that this code can't be run in this text-based environment. You need to run this on your local machine with Python and pygame installed.


#### You:
Can you keep track of the highscore in a separate txt file?

#### ChatGPT:
Sure, we can modify the script to read and write the high score to a text file. To read the high score, we open the file in read mode at the beginning of the game. To write a new high score, we open the file in write mode when the game ends and the current score is higher than the high score.

Here is the updated code:

```python
import pygame
import sys
import random

class FlappyBird:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("background.png").convert()
        self.birdSprites = [pygame.image.load("bird1.png").convert_alpha(),
                            pygame.image.load("bird2.png").convert_alpha(),
                            pygame.image.load("bird3.png").convert_alpha()]
        self.wallUp = pygame.image.load("bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 200
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.running = False

        # Load the high score
        with open('highscore.txt', 'r') as f:
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
                            with open('highscore.txt', 'w') as f:
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
```

In this version of the game, the high score is loaded from a file named 'highscore.txt' at the start of the game. If the current score is higher than the high score at the end of the game, the high score is updated and saved back to the file. The game over screen now also displays the high score.

Again, replace "bird1.png", "bird2.png", "bird3.png", "background.png", "bottom.png", "top.png" with the actual paths to your image files.

Please remember that this code can't be run in this text-based environment. You need to run this on your local machine with Python and pygame installed.
