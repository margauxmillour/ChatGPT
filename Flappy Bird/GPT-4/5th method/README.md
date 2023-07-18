PROMPT:

Write a code in python. There is a bird ('bird.png') centered on the left side of the screen. The bird moves downward due to gravity, and flaps its wings to rise a constant height when the spacebar is pressed. When making the bird flap its wings, don't forget to reset the bird's speed to 0. Use the pygame library. The window size should be 800x600. Don't forget to implement a clock. Make sure that all variables are declared.

Now, can you add animations and rotation to the bird? I have 3 frames : 'bird1.png', 'bird2.png' and 'bird3.png'. Don't make it too fast.

Now, I would like to add a blue background and a ground ('base.png'). The ground doesn't need to be moving.

Now, I would like to add pipes. For now, don't bother with collisions. Create a Pipe class, with the functions __init__(self,x,gap_y), move(self) and draw(self). Outside of this class, create a spawn_pipe() function. The pipes come by pair, one at the top ('pipe_top.png') and one at the bottom ('pipe_bottom.png'). They are separated by a gap which size is 5 times the bird's height. This gap is placed at a random height, between 100 and the height of the window minus the gap minus 100. The pipes appear on the right side of the screen, move from right to left, and disappear once they reach the left side. One pair of pipes appear every 2 seconds. 

Now can you add collisions? When the birds collides either with the ground or the pipes, the game ends.

Now can you add a score system? When the bird crosses the gap between a pair of pipes, the score should be incremented by one.

Now, can you add a start screen and a game over screen? The start screen should appear when the player opens the game, and it should be written on it 'Press space to start'. The game over screen should appear when the player loses, and it should be written on it the score and 'Press space to start'. Make sure that when restarting, the bird is at its initial position.

Finally, can you keep track of the highscore in a separate txt file? It should also be displayed on the game over screen.