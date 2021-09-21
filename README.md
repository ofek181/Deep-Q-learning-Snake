# Deep Q learning Snake
## An attempt at using a Deep Q neural network to learn how to play the game "Snake":
![image](https://user-images.githubusercontent.com/80195693/134158257-fa82b0e3-ee7e-4850-a3c7-24abfd4e04ab.png)

## The snake game itself was programmed using python and pygame. 
### "game_logic" contains the class Logic which represents the logic of the snake game. 
### "snake_game" contains the class Snake which implements the snake game itself, you can play snake if you'd like by calling the Snake object.
### the "consts" file contains the constants of the game such as screen width, height and more, you can change this constants to determine the board size and more.
### "experience_replay" is responsible for randomly sampling experiences from the ExperienceBuffer, This tackles the problem of autocorrelation leading to unstable training.
### "dqn_input" contains the class InputBuffer which is responsible for dealing with the input of the model, One frame is not enough since the model needs to understand the direction of the snake object, therefor 2 frames are used as inputs for the model.
### "dqn_model" contains the deep neural network that is used for the learning model of the agent. I used a CNN model with 2 conv layers and 1 hidden layer but you can play with the hyperparameters to see which fits best.
### "dqn_agent" is the implementation of the reinforcement learning agent used in the game. The agent is a value-based reinforcement learning agent that estimates the return or future rewards.

#### I trained a model with a 25x20 board (250 on 200) for 400,000 episodes (half of them were exploration and half were exploitation), with max step of 1000.
##### this model is named: 25x20x400000x1000. 
##### you can load it using the load_model method to test the model (its location is in the trained_model folder) or you can train your own model!  
