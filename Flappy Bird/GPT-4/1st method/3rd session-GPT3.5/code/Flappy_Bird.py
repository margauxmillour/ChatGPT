import pygame
import sys
import random

# Constants for the game
SCREENWIDTH = 288
SCREENHEIGHT = 512
FPS = 30
PLAYER_JUMP = -9
GRAVITY = 1
PIPE_GAP_SIZE = 150  # gap between upper and lower pipe
PIPE_SPEED = -4
PLAYER_MAX_SPEED = 10

# Load assets
BIRD_IMGS = [pygame.image.load('assets/bird1.png'), pygame.image.load('assets/bird2.png'), pygame.image.load('assets/bird3.png')]
BASE_IMG = pygame.image.load('assets/base.png')
BG_IMG = pygame.image.load('assets/background.png')
PIPE_IMG = pygame.image.load('assets/pipe.png')

def check_collision(player, pipes):
    for pipe in pipes:
        pipe_rect = pygame.Rect(pipe[0], pipe[1], PIPE_IMG.get_width(), PIPE_IMG.get_height())
        if player.colliderect(pipe_rect):
            return True
    return False

def show_message(screen, myfont, message, y):
    label = myfont.render(message, 1, (0,0,0))  
    screen.blit(label, (50, y))

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

    myfont = pygame.font.SysFont("monospace", 15)

    base_x = 0
    score = 0
    high_score = 0

    try:
        with open("assets/highscore.txt", "r") as f:
            high_score = int(f.read())
    except FileNotFoundError:
        high_score = 0

    bird_index = 0
    bird_x = int(SCREENWIDTH * 0.2)
    bird_y = int((SCREENHEIGHT - BIRD_IMGS[0].get_height()) / 2)
    bird_dy = 0  
    bird_rect = BIRD_IMGS[0].get_rect(topleft = (bird_x, bird_y))

    pipe_width = PIPE_IMG.get_width()
    pipe_height = PIPE_IMG.get_height()
    pipes = []

    # game start screen
    while True:
        screen.blit(BG_IMG, (0,0))
        show_message(screen, myfont, "Press any key to start!", SCREENHEIGHT / 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                break
        else:
            continue
        break

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_dy = PLAYER_JUMP

        bird_dy += GRAVITY
        bird_y += min(bird_dy, PLAYER_MAX_SPEED)
        bird_rect[1] = bird_y

        screen.blit(BG_IMG, (0,0))  

        new_pipes = []
        for pipe in pipes:
            new_x = pipe[0] + PIPE_SPEED
            if new_x > -PIPE_IMG.get_width():
                if pipe[2] == False and new_x < bird_x:
                    pipe[2] = True
                    score += 1
                new_pipes.append([new_x, pipe[1], pipe[2]])
                screen.blit(PIPE_IMG, (new_x, pipe[1]))  
        pipes = new_pipes

        screen.blit(BASE_IMG, (base_x, SCREENHEIGHT - BASE_IMG.get_height()))  

        bird_index = (bird_index + 1) % 3
        bird_rect = BIRD_IMGS[bird_index].get_rect(topleft = (bird_x, bird_y))
        screen.blit(BIRD_IMGS[bird_index], bird_rect)

        score_label = myfont.render("Score: {0}".format(score), 1, (0,0,0))  
        screen.blit(score_label, (100, 50))

        high_score_label = myfont.render("High Score: {0}".format(high_score), 1, (0,0,0)) 
        screen.blit(high_score_label, (100, 70))

        pygame.display.update()
        clock.tick(FPS)

        if len(pipes) == 0 or pipes[-1][0] < SCREENWIDTH - 250:
            pipe_x = SCREENWIDTH
            pipe_y = random.randint(int(SCREENHEIGHT * 0.1), int(SCREENHEIGHT * 0.6))
            pipe_upper = [pipe_x, pipe_y - pipe_height, True]
            pipe_lower = [pipe_x, pipe_y + PIPE_GAP_SIZE, False]
            pipes.extend([pipe_upper, pipe_lower])

        if check_collision(bird_rect, pipes):
            if score > high_score:
                high_score = score
                with open("assets/highscore.txt", "w") as f:
                    f.write(str(high_score))

            # game over screen
            while True:
                screen.blit(BG_IMG, (0,0))
                show_message(screen, myfont, "Game Over! Press any key to restart!", SCREENHEIGHT / 2)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        main()  # restart the game
                else:
                    continue
                break

if __name__ == "__main__":
    main()
