import pygame
import math
import sys
import time
from ground_map import MAP
from random import uniform
import copy
pygame.init()

MAP_IN_GAME = copy.deepcopy(MAP)

WIDTH = 800
HEIGHT = 600
SIZE = HEIGHT / len(MAP_IN_GAME)
space = 0
angle_tir_player = 45
angle_tir_computer = 135
start_ai = time.time()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Wars")

# Game states
START_SCREEN = 0
GAME_SCREEN = 1
GAME_OVER_SCREEN = 2

game_state = START_SCREEN

ground_color = (100, 100, 100)  # RGB value for the ground color
ground_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

# Define the ground structure using the MAP_IN_GAME data
ground_width = len(MAP_IN_GAME[0])  # Each element represents a column of pixels
ground_height = 50
ground_depth = len(MAP_IN_GAME)

projectiles = []


class Tank:
    def __init__(self, x, y, image, health_image_full, health_image_mid, health_image_low, health_image_empty):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.angle = 0
        self.health = 3
        self.health_image_full = pygame.image.load(health_image_full)
        self.health_image_mid = pygame.image.load(health_image_mid)
        self.health_image_low = pygame.image.load(health_image_low)
        self.health_image_empty = pygame.image.load(health_image_empty)

    def draw(self):
        # Rotate the tank image based on the angle
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        if MAP_IN_GAME[int(self.y // SIZE) + 2][int(self.x // SIZE)] == 0 and MAP_IN_GAME[int(self.y // SIZE) + 2][int(self.x // SIZE) + 1] == 0:
            self.y += SIZE
        screen.blit(rotated_image, (self.x, self.y))

        # Draw tank's health
        health_images = [
            self.health_image_empty,
            self.health_image_low,
            self.health_image_mid,
            self.health_image_full
        ]
        health_image = health_images[min(self.health, 3)]
        screen.blit(health_image, (self.x, self.y - 20))

def draw_start_screen():
    screen.fill((0, 0, 0))
    # Draw start screen elements
    title = pygame.font.Font(None, 36).render("Tank Wars", True, (255, 255, 255))
    text = pygame.font.Font(None, 36).render("Press ENTER to start", True, (255, 255, 255))
    title_rect = title.get_rect()
    text_rect = text.get_rect()
    title_rect.center = (WIDTH/2, HEIGHT/2-40)
    text_rect.center = (WIDTH/2, HEIGHT/2+40)
    screen.blit(title, title_rect)
    screen.blit(text, text_rect)

def draw_game_over_screen():
    global player_tank, computer_tank
    # Draw game over screen elements
    if player_tank.health > computer_tank.health:
        text = pygame.font.Font(None, 36).render(f"Player wins!", True, (255, 255, 255))
    else:
        text = pygame.font.Font(None, 36).render(f"Computer wins!", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (WIDTH/2, HEIGHT/2)
    screen.blit(text, text_rect)
    text2 = pygame.font.Font(None, 36).render("Press ENTER to play again", True, (255, 255, 255))
    text2_rect = text2.get_rect()
    text2_rect.center = (WIDTH/2, HEIGHT-80)
    screen.blit(text2, text2_rect)

def draw_ground():
    for y in range(ground_depth):
        for x in range(ground_width):
            if MAP_IN_GAME[y][x] == 1:
                pygame.draw.rect(
                    screen,
                    ground_color,
                    (x * SIZE, y * SIZE, SIZE, SIZE)
                )

def handle_input(player_tank):
    global space, start, end, angle_tir_player, game_state

    keys = pygame.key.get_pressed()

    if keys[pygame.K_z] and angle_tir_player < 180:
        angle_tir_player += 1  # Rotate the tank counter-clockwise
    elif keys[pygame.K_s] and angle_tir_player > 0:
        angle_tir_player -= 1  # Rotate the tank clockwise

    if keys[pygame.K_d]:
        # Calculate the new position based on the tank's angle and movement direction
        new_x = player_tank.x + 3 * math.cos(math.radians(player_tank.angle))
        new_y = player_tank.y - 3 * math.sin(math.radians(player_tank.angle))

        # Check if the tank is within the screen boundaries
        if 0 <= new_x <= WIDTH - player_tank.image.get_width() and 0 <= new_y <= HEIGHT - player_tank.image.get_height():
            ground_x = int((new_x + 32) // 20)
            ground_y = int(new_y // 20)
            # Check if the tank is on the ground or can climb a one-block difference in height
            if MAP_IN_GAME[ground_y + 1][ground_x] == 0 and MAP_IN_GAME[ground_y][ground_x] == 0:
                player_tank.x = new_x
                player_tank.y = new_y

            elif MAP_IN_GAME[ground_y + 1][ground_x] == 1 and MAP_IN_GAME[ground_y][ground_x - 1] == 0 and MAP_IN_GAME[ground_y - 1][ground_x - 1] == 0:
                player_tank.x = new_x
                player_tank.y = new_y - SIZE

    if keys[pygame.K_q]:
        # Calculate the new position based on the tank's angle and movement direction
        new_x = player_tank.x - 3 * math.cos(math.radians(player_tank.angle))
        new_y = player_tank.y + 3 * math.sin(math.radians(player_tank.angle))

        # Check if the tank is within the screen boundaries
        if 0 <= new_x <= WIDTH - player_tank.image.get_width() and 0 <= new_y <= HEIGHT - player_tank.image.get_height():
            ground_x = int(new_x // 20)
            ground_y = int(new_y // 20)
            # Check if the tank is on the ground or can climb a one-block difference in height
            if MAP_IN_GAME[ground_y + 1][ground_x] == 0 and MAP_IN_GAME[ground_y][ground_x] == 0:
                player_tank.x = new_x
                player_tank.y = new_y
            elif MAP_IN_GAME[ground_y + 1][ground_x] == 1 and MAP_IN_GAME[ground_y][ground_x] == 0 and MAP_IN_GAME[ground_y - 1][ground_x - 1] == 0:
                player_tank.x = new_x
                player_tank.y = new_y - SIZE

    if space == 1:
        start = time.time()

    if keys[pygame.K_SPACE]:
        # Create a projectile and shoot it
        space += 1
    else:
        if space:
            space = 0
            end = time.time()
            velocity = (end - start) * 12 + 6
            shoot_projectile(player_tank, velocity, angle_tir_player)

def shoot_projectile(tank, velocity, angle):
    projectile = Projectile(tank.x + 18, tank.y + 3, velocity, angle)
    projectiles.append(projectile)

class Projectile:
    def __init__(self, x, y, velocity, angle):
        self.x = x
        self.y = y
        self.velocity = velocity  # Adjust the velocity as needed
        self.gravity = 0.5  # Adjust the gravity as needed
        self.time = 0
        self.angle = angle

    def update(self):
        global projectiles
        self.time += 1
        # Calculate the x and y components of the velocity
        velocity_x = self.velocity * math.cos(math.radians(self.angle))
        velocity_y = self.velocity * math.sin(math.radians(self.angle)) - self.gravity * self.time

        # Calculate the new position based on the velocity components
        self.x += velocity_x
        self.y -= velocity_y

        # Update the ground structure based on the projectile's impact
        ground_x = int(self.x // SIZE)
        ground_y = int(self.y // SIZE)
        if 0 <= ground_x < ground_width and 0 <= ground_y < ground_depth:
            if MAP_IN_GAME[ground_y][ground_x] == 1:
                compteur = ground_x + 1 - (ground_x - 2)
                for k in range(ground_y - 1, ground_y + 2):
                    for i in range(ground_x - compteur, ground_x + compteur + 1):
                        if 0 <= i < ground_width and 0 <= k < ground_depth-1:
                            MAP_IN_GAME[k][i] = 0
                    compteur -= 1
                projectiles.remove(self)

        # Check if the projectile hits the player tank
        if self.x > player_tank.x and self.x < player_tank.x + player_tank.image.get_width() and \
                self.y > player_tank.y and self.y < player_tank.y + player_tank.image.get_height():
            player_tank.health -= 1
            projectiles.remove(self)

        if self.x > computer_tank.x and self.x < computer_tank.x + computer_tank.image.get_width() and \
                self.y > computer_tank.y and self.y < computer_tank.y + computer_tank.image.get_height() and \
                self.time >= 10:
            computer_tank.health -= 1
            projectiles.remove(self)

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 5)

def handle_projectiles():
    for projectile in projectiles:
        projectile.update()
        projectile.draw()

def handle_ai(computer_tank):
    global angle_tir_computer, start_ai
    # Rotate the tank's turret to aim at the player tank
    dx = player_tank.x - (computer_tank.x+32)
    dy = computer_tank.y - (player_tank.y-29)
    angle_tir_computer = uniform(math.degrees(math.atan2(dy, dx))-10, math.degrees(math.atan2(dy, dx))+10)

    # Calculate the distance between the tanks
    distance = math.sqrt(dx**2 + dy**2)

    if distance < 300:
        if time.time()-start_ai >= 2:
            # Shoot the projectile if the tanks are close enough
            shoot_projectile(computer_tank, 15, angle_tir_computer)
            start_ai = time.time()

    else:
        # Calculate the new position based on the tank's angle and movement direction
        new_x = computer_tank.x - 3 * math.cos(math.radians(computer_tank.angle))
        new_y = computer_tank.y + 3 * math.sin(math.radians(computer_tank.angle))

        # Check if the tank is within the screen boundaries
        if 0 <= new_x <= WIDTH - computer_tank.image.get_width() and 0 <= new_y <= HEIGHT - computer_tank.image.get_height():
            ground_x = int(new_x // 20)
            ground_y = int(new_y // 20)
            # Check if the tank is on the ground or can climb a one-block difference in height
            if MAP_IN_GAME[ground_y + 1][ground_x] == 0 and MAP_IN_GAME[ground_y][ground_x] == 0:
                computer_tank.x = new_x
                computer_tank.y = new_y
            elif MAP_IN_GAME[ground_y + 1][ground_x] == 1 and MAP_IN_GAME[ground_y][ground_x] == 0 and MAP_IN_GAME[ground_y - 1][ground_x - 1] == 0:
                computer_tank.x = new_x
                computer_tank.y = new_y - SIZE

def check_game_over():
    global player_tank, computer_tank, game_state
    if player_tank.health <= 0 or computer_tank.health <= 0:
        game_state = GAME_OVER_SCREEN

clock = pygame.time.Clock()

player_tank = Tank(100, HEIGHT - 249, "assets/green_tank.png", "assets/green_heart_full.png",
                   "assets/green_heart_mid.png", "assets/green_heart_low.png", "assets/green_heart_empty.png")
computer_tank = Tank(WIDTH - 100, HEIGHT - 469, "assets/red_tank.png", "assets/red_heart_full.png",
                     "assets/red_heart_mid.png", "assets/red_heart_low.png", "assets/red_heart_empty.png")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if game_state == START_SCREEN:
        draw_start_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_state = GAME_SCREEN
    elif game_state == GAME_SCREEN:
        screen.fill((0, 0, 0))  # Clear the screen

        handle_input(player_tank)
        handle_ai(computer_tank)
        handle_projectiles()
        check_game_over()

        player_tank.draw()
        computer_tank.draw()
        draw_ground()

    elif game_state == GAME_OVER_SCREEN:
        player_tank.draw()
        computer_tank.draw()
        draw_ground()
        draw_game_over_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            space = 0
            angle_tir_player = 45
            angle_tir_computer = 135
            start_ai = time.time()
            projectiles = []
            MAP_IN_GAME = copy.deepcopy(MAP)
            player_tank = Tank(100, HEIGHT - 249, "assets/green_tank.png", "assets/green_heart_full.png",
                   "assets/green_heart_mid.png", "assets/green_heart_low.png", "assets/green_heart_empty.png")
            computer_tank = Tank(WIDTH - 100, HEIGHT - 469, "assets/red_tank.png", "assets/red_heart_full.png",
                     "assets/red_heart_mid.png", "assets/red_heart_low.png", "assets/red_heart_empty.png")
            game_state = GAME_SCREEN

    pygame.display.flip()  # Update the contents of the entire display
    clock.tick(60)  # Limit the frame rate to 60 FPS
