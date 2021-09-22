# Deep Q learning Snake
## An attempt at using a Deep Q neural network to learn how to play the game "Snake":
![image](https://user-images.githubusercontent.com/80195693/134158257-fa82b0e3-ee7e-4850-a3c7-24abfd4e04ab.png)

## The snake game itself was programmed using python and pygame. 
1. "game_logic" contains the class Logic which represents the logic of the snake game. 
2. "snake_game" contains the class Snake which implements the snake game itself, you can play snake if you'd like by calling the Snake object.
3. the "consts" file contains the constants of the game such as screen width, height and more, you can change this constants to determine the board size and more.
4. "experience_replay" is responsible for randomly sampling experiences from the ExperienceBuffer, This tackles the problem of autocorrelation leading to unstable training.
5. "dqn_input" contains the class InputBuffer which is responsible for dealing with the input of the model, One frame is not enough since the model needs to understand the direction of the snake object, therefor 2 frames are used as inputs for the model.
6. "dqn_model" contains the deep neural network that is used for the learning model of the agent. I used a CNN model with 2 conv layers and 1 hidden layer but you can play with the hyperparameters to see which fits best.
7. "dqn_agent" is the implementation of the reinforcement learning agent used in the game. The agent is a value-based reinforcement learning agent that estimates the return or future rewards.

##### I trained a model with a 12x10 board (120 on 100) for 250,000 episodes (half of them were exploration and half were exploitation), with max step of 2000.
##### the trained model is named: 12x10x250000x2000. 
##### you can load it using the load_model method to test the model (its location is in the trained_model folder) or you can train your own model!  
