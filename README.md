# Snake using Deep Q learning and pygame
![image](https://user-images.githubusercontent.com/80195693/134565864-dc5b75b8-aa18-48ba-8b43-7c29bfeb07e3.png)

## Files
<p>1. "game_logic" contains the class Logic which represents the logic of the snake game.<br>
2. "snake_game" contains the class Snake which implements the snake game itself, you can play snake if you'd like by calling the Snake object.<br>
3. the "consts" file contains the constants of the game such as screen width, height and more, you can change this constants to determine the board size and more.<br>
4. "experience_replay" is responsible for randomly sampling experiences from the ExperienceBuffer, This tackles the problem of autocorrelation leading to unstable training.<br>
5. "dqn_input" contains the class InputBuffer which is responsible for dealing with the input of the model, One frame is not enough since the model needs to understand the direction of the snake object, therefor 2 frames are used as inputs for the model.<br>
6. "dqn_model" contains the deep neural network that is used for the learning model of the agent. I used a CNN model with 2 conv layers and 1 hidden layer but you can play with the hyperparameters to see which fits best.<br>
7. "dqn_agent" is the implementation of the reinforcement learning agent used in the game. The agent is a value-based reinforcement learning agent that estimates the return or future rewards.</p>

## Experiment

<p>I trained a model with a 15x10 board (150 on 100) for 100,000 episodes.<br>
Half of them were exploration and half were exploitation, with max step of 2000.<br>
The trained model is named: 15x10x100000x2000.<br>
The learning curve of the following model during training is as follows:</p>

![15x10x100000x2000](https://user-images.githubusercontent.com/80195693/134649726-298d97f3-b306-4316-95d6-151e8c4a34ba.png)


<p> I later tested the model for 100 episodes and obtained the following results:</p>

![histogram](https://user-images.githubusercontent.com/80195693/134652157-2326a65b-5e7f-459a-9694-cda9b0c1a92e.png)

Max Score: 57, Min Score: 8, Average Score: 32.16

