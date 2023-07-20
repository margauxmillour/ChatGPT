# End-user Programming with LLM (and ChatGPT) 

Is it possible to program non-trivial applications and customize code without knowing much about programming? 
Impressive [showcases](https://youtu.be/qbIk7-JPB2c?t=1865) of [ChatGPT](https://twitter.com/acherm/status/1636035908137893896) suggest a positive answer. 
Some people have even claimed that [programmers will be replaced or disappear](https://cacm.acm.org/magazines/2023/1/267976-the-end-of-programming/fulltext). 
So, can end-users create working and non-trivial applications, like games, just using instructions in natural language with ChatGPT? 
Enter the git! 
So far, we have mainly considered the game Flappy bird, using Python.  
We are sharing 35 sessions, with prompts, code, observations, and results (videos) with ChatGPT-3.5 and ChatGPT-4. 

We plan to collect other experiences and consider other applications and games in near future, **please contribute and/or stay tuned!**

## Method, prompts, code, observations, and results 

Specifically, our material is available in folder `Flappy Bird`. 
There are two folders `GPT-4` and `GPT-3.5`.

In each folder, there are different methods and strategies that we have used. For each method, several sessions with ChatGPT have been made: the prompts and interactions are available as Markdown files in `prompt`. There is also the code in `code` -- usually resulting from the last interaction with ChatGPT. 
There is also a `video.mp4` that shows the game in action! Finally, there is also `observations.txt` that reviews the session, reporting some lessons learned or some indicators (e.g., number of iterations.)
 



Five methods:
 * __1st method__: _Giving ChatGPT an example of finished code doing what we want (in our case a complete Flappy Bird game written in Python), and asking it to return a prompt_.
The prompt returned was never the same (probably because of the temperature parameter), but was usually in the form of a list of characteristics.
For instance: 
    >* Create a Flappy Bird game using Pygame. The game should have the following features:
    >* The game window should be 288x512 pixels in size.
    >* The background, bird, base, and pipe assets should be loaded and displayed on the screen.
    >* The bird should be able to jump when the spacebar is pressed.
    >* Pipes should spawn at regular intervals and move from right to left.
    >* The bird should be able to collide with the pipes, the top/bottom of the screen, or the base.
    >* The score should increase when the bird successfully passes a pair of pipes.
    >* The game should end when the bird collides with an obstacle.
    >* The highest score achieved should be displayed on the screen, along with the option to restart the game.
    > Please provide the necessary code to implement the above features using the Pygame library.

 * __2nd method__: _Providing a list of characteristics (this time written by a human)_.
The user will come with a list of functions and/or characteristics that describe the game. The list is given all at once to ChatGPT and is used as the prompt.
For instance:
    >* Write a Flappy Bird game in Python.
    >* There is a start screen where you can see the highscore, and start playing by pressing the spacebar.
    >* The highscore is stocked in a txt file.
    >* I have an image for the pipes, the background, the clouds, and a frame sheet for the bird.
    >* The bird is animated and has 3 frames
    >* There are 2 types of clouds moving in the background.
    >* The player navigates the bird through pairs of pipes that have equally sized gaps placed at random heights.
    >* The difficulty gradually increases.
    >* The bird automatically descends and ascends when the player presses the spacebar.
    >* Each successful pass through a pair of pipes awards the player one point.
    >* Colliding with a pipe or the ground ends the gameplay.
    >* There is a game over screen where you can see your score, the highscore, and play again by pressing the spacebar.


 * __3rd method__: _A short prompt_.
 The prompt is given as a simple sentence that provides the overall (general) goal of the task.
 No specific information nor detailed functionalities are given. At lot have to be infered by the LLM at generation time.
 For instance:
     >Write a Flappy Bird game in Python.
 
 * __4th method__: _A short description of the main features_.
 This can be seen as a mix of methods 2 and 3 as the prompt is written in natural written language and not as a list of functionalities or characteristics. Yet, the text gives more information than the prompt proposed in the third method.
 For instance:
    >Write the code for a Flappy Bird game in python. I have a folder "assets" with "background.png", "pipe.png" and "bird.png". I would like to know my score and keep track of my highcore in a separate file. I would like to have a start screen when I first open the game, where I can see my highscore, and a game over screen where I can see my score, highscore and play again.
 
 * __5th method__: _A list of prompts (without having to look at the code in between the requests)_.
 This last method would mimic the behavior of an end-user that carefully thought about what they need. They do not really interact with the LLM and only give the instruction one after an other without caring for the provided output.
 Only the final output is used and potentially asked to be improved, anything before that is only the user trying to build little by little what would be its codebase.
 For instance (note that every bullet here is a prompt that follows the previous one):
 
    >* Write a code in python. There is a bird ('bird.png') centered on the left side of the screen. The bird moves downward due to gravity, and flaps its wings to rise a constant height when the spacebar is pressed. When making the bird flap its wings, don't forget to reset the bird's speed to 0. Use the pygame library. The window size should be 800x600. Don't forget to implement a clock. Make sure that all variables are declared.
    >* Now, can you add animations and rotation to the bird? I have 3 frames: "bird1.png", "bird2.png" and "bird3.png". Don't make it too fast.
    >* Now, I would like to add a blue background and a ground ("base.png"). The ground doesn't need to be moving.
    >* Now, I would like to add pipes. For now, don't bother with collisions. Create a Pipe class, with the functions __init__(self,x,gap_y), move(self) and draw(self). Outside of this class, create a spawn_pipe() function. The pipes come by pair, one at the top ('pipe_top.png') and one at the bottom ('pipe_bottom.png'). They are separated by a gap which size is 5 times the bird's height. This gap is placed at a random height, between 100 and the height of the window minus the gap minus 100. The pipes appear on the right side of the screen, move from right to left, and disappear once they reach the left side. One pair of pipes appear every 2 seconds.
    >* Now can you add collisions? When the birds collides either with the ground or the pipes, the game ends.
    >* Now can you add a score system? When the bird crosses the gap between a pair of pipes, the score should be incremented by one.*
    >* Now, can you add a start screen and a game over screen? The start screen should appear when the player opens the game, and it should be written on it 'Press space to start'. The game over screen should appear when the player loses, and it should be written on it the score and 'Press space to start'. Make sure that when restarting, the bird is at its initial position.*
    >* Finally, can you keep track of the highscore in a separate txt file? It should also be displayed on the game over screen.*

## Observation and synthesis
 
### Do claims generalize? (Use the prompt and you'll get a game)  

No, we did not find a method (or a magic prompt) that **systematically** works and would generate a feature-rich game.
Though we have been able to generate interesting and playable games without technical intervention, there are also several cases and sessions that lead to a dead-end situation, far from the ideal scenario usually promised. 

First, it happens that we reach a dead "end-state" with a non-working or unusable game (mainly due to inability to fix an issue), see for instance:
 * 2nd method, 2nd session (it is possible to continue, but just requiring skills to debug code "("Pipes only came 1 by 1 and not by pair. Trying to implement that only led to more problems that ChatGPT couldn't solve.")")
 * 2nd method, 4th session (10 interactions, Too many problems (no top pipes, always at the same height, wrong collision detection...))

Second, despite the same original prompt (and the same "method"), we can have very different generated code. 
This difference is in terms of: 
 * issues in the code, requiring more or less fixing and debugging effort
 * features supported: ChatGPT takes the liberty to implement (or not) some functionalities, and the resulting game might be very different... It forces again to interact with ChatGPT, specifically with regards to what has been generated.

The consequence is that several specific interactions are needed, some leading to the worst situation (no working game), far from the ideal scenario. 



### Is it possible to program without expertise? 

Yes, but again, it is not systematic.

Direct interventions in the code are sometimes needed (to fix issues!). 
For example, we had to `[...] change the values of the gravity, bird_movemement and pipe_gap to make it easier and more controllable.`
ChatGPT does not seem to find how to fix the code by itself (when we just point out the problems).
Besides, it is more challenging to interact as end-user when the game was from the start in a very bad shape, and basically unplayable or missing critical features. In this case, it is not possible to get a visual observation that would help formulating a proper feedback. 


The *style* of ChatGPT is sometimes to decompose the problem and put placeholders in the code... but without the implementation!
From a developer perspective, it is an interesting style that forces to consider a step-by-step implementation. 
However, from a end-user perspective, the game is in an incomplete shape. 

There are sometimes ChatGPT explanations related to a "feature" that does not exist, leading to time consuming effort. 
For example, `Implement a feature that has no meaning "There was a 'FLAP' event that made the bird jump every 200ms. That's not part of the game!"`

Some examples of issues that needed to be fixed:
 * clock (pygame specifics?) => bird crashes immediately 
 * gap placement between the pipes
 * collision detection
 * breaking of older functionality 
 * missing a bit of diversity

Both fixes are time-consuming. It is possible to help thanks to end-user, visual observations about the game. 
Sometimes, there is the need to orient discussions and interactions towards code. 


### How are games different? What are the features? 

see videos and sheet with features per game and method. 
You can get well a feature-rich Flappy bird, but also a game with closed pipes that make the progression of the game limited.  

### How do resulting codes differ?

see notebook
 
 
### What are the positive aspects of using ChatGPT? 

There are several positive aspects:
 * inspiration, funny variants 
 * discovering new features
 * good starting point for developers 
 * sometimes it can work and end-users can create interesting games


## Conclusion and perspectives 

Formulating a prompt and systematically getting a comprehensive and playable game is not yet a reality. 
ChatGPT can provide impressive results, but not all times. A magic prompt is missing to make ChatGPT reliable. 
Many interactions are rather needed to fix issues or expand the features, sometimes in non-technical terms and with instructions out of observations of the current game. But the control of the code is not that far and seems inevitable. 

There are several interesting directions to consider:
 * change the targeted programming language and/or the framework: instead of Python and pygame, it's possible to use JavaScript and p5 for instance... An hypothesis is that the targeted technological space can help ChatGPT filling the gap between the prompts and the intentions. 
 * find a super prompt or a language (who says a domain-specific language?) that leads to more determinism and control of ChatGPT
 * improve the usability and the integration of ChatGPT ouputs into development environment. The back and forth between the IDE and ChatGPT is time-consuming. Moreover, some (informal) instructions of ChatGPT can be automatically applied onto the code base, limiting the user effort or the technical expertise required. The hope is to have a better feedback-loop! 





## Future 


### 3D game HTML/JS

Sparks of Artificial General Intelligence: Early experiments with GPT-4 https://arxiv.org/abs/2303.12712 
Section 3.1.2

"Coding challenges can evaluate the skills in algorithms and data structures. However, they often fail to capture the full complexity and diversity of real-world coding tasks, which requires specialized domain knowledge, creativity, and integration of multiple components and libraries, as well as the ability to change existing code." => we are indeed in this case!

Specifically on page 24, there is "Front-end / Game development" with an interesting prompt 

```
Can you write a 3D game in HTML with Javascript, I want:
-There are three avatars, each is a sphere.
-The player controls its avatar using arrow keys to move.
-The enemy avatar is trying to catch the player.
-The defender avatar is trying to block the enemy.
-There are also random obstacles as cubes spawned randomly at the beginning and moving randomly. The avatars cannot cross those cubes.
-The player moves on a 2D plane surrounded by walls that he cannot cross. The wall should cover the boundary of the entire plane.
-Add physics to the environment using cannon.
-If the enemy catches the player, the game is over.
-Plot the trajectories of all the three avatars.
```

A possibility is to re-play the prompt (eg with ChatGPT3)... or to use another technology (eg pygame https://www.pygame.org/)
Demo here: https://youtu.be/qbIk7-JPB2c?t=1865



### Pong HTML/JS

I wanted to see what ChatGPT would write if I gave the minimum information, and not touching a single line of code. Here is how it went : 

```Write the code for a Pong game, using HTML and JavaScript.```
The ball was moving, but not the paddles.

```The paddles can't move, how can you fix this ?```
The problem was fixed, but there was no score, and the game went on even if the ball touched the left or right wall.

```I would like to add a score system, and end the game when the ball touches either the left or right wall```
A score was showing up, but stayed at zero no matter what was happening. Additionally, there was no "second player". The second paddle was under the name of 'ai', but didn't move ; not very interesting.

```The score doesn't go up, can you fix the problem ? I would like to add a second player too, that would play using 'W' and 'S’```
The game was now functional.

### Pong and Game of life

https://twitter.com/acherm/status/1636035908137893896
