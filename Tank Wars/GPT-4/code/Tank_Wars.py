import pygame
import sys
import random
import math

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAVITY = 0.1

class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.lives = 3

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, 50, 50))

    def hit(self):
        self.lives -= 1
        print(f"{self.color} tank was hit! Lives remaining: {self.lives}")

    def move(self, dx):
        self.x += dx
        self.x = max(0, min(WIDTH-50, self.x))  # keep tank within screen

class Projectile:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY  # simulate gravity

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 5)

    def check_collision(self, tank):
        if self.x >= tank.x and self.x <= tank.x + 50 and self.y >= tank.y and self.y <= tank.y + 50:
            return True
        return False

    def out_of_bounds(self):
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            return True
        return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = Tank(100, HEIGHT-50, GREEN)
computer = Tank(WIDTH-150, HEIGHT-50, RED)
projectiles = []
computer_timer = 0

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_down_time = pygame.time.get_ticks()  # record the time when space is first pressed
            elif event.key == pygame.K_LEFT:
                player.move(-10)
            elif event.key == pygame.K_RIGHT:
                player.move(10)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_up_time = pygame.time.get_ticks()  # record the time when space is released
                dt = max(1, space_up_time - space_down_time)  # compute the time difference
                power = dt / 200.0  # scale the time difference to get a reasonable power value
                projectiles.append(Projectile(player.x, player.y, 2*power, -2*power))

    # Computer behavior
    computer_timer += 1
    if computer_timer > 200:
        projectiles.append(Projectile(computer.x, computer.y, -2, -2))
        computer_timer = 0

    # Game state updates
    for p in projectiles[:]:  # iterate over a copy of the list
        p.move()
        if p.check_collision(player):
            player.hit()
            projectiles.remove(p)
        elif p.check_collision(computer):
            computer.hit()
            projectiles.remove(p)
        elif p.out_of_bounds():
            projectiles.remove(p)


    # Check for game over
    if not player.lives:
        print("Computer wins!")
        break
    if not computer.lives:
        print("Player wins!")
        break

    # Drawing
    screen.fill(BLACK)
    player.draw(screen)
    computer.draw(screen)
    for p in projectiles:
        p.draw(screen)

    pygame.display.flip()
