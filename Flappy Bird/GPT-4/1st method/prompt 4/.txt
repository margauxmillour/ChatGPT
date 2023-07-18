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