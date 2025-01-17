![game](https://github.com/user-attachments/assets/da9fb361-8a2e-4704-8d0b-6a623a5a8e5f)# dino_game_with_trained_agent_
Dino Game Explanation
The Dino Game is a simple browser-based game in which the player controls a dinosaur (Dino) that must jump over obstacles like cacti or avoid colliding with flying birds. The game starts automatically once the internet connection is lost, though you can play it anytime by triggering it through a browser's developer console. This Python version recreates the game using Pygame, with the addition of reinforcement learning (RL) training and other features.

Here’s a breakdown of the key components:

Game Mechanics Overview
State: The state in the game is defined by the environment around the dinosaur. It includes the position of the dino, the speed of the game, and any obstacles in front of it (such as cacti or flying birds). The game provides an observation for the agent that contains information on the distance to obstacles, dino’s position, and whether there’s a bird to avoid.

Action: The agent (player) has two main actions:

Action 0: Do nothing (Dino continues running).
Action 1: Jump (Dino leaps to avoid obstacles).
Reward: The reward system works as follows:

+1: For successfully avoiding an obstacle (i.e., jumping over a cactus or bird).
-1: For crashing into an obstacle.
0: If no action is taken, or nothing happens (like if there’s no obstacle).


Run the Game
>>python game.py<<

Contributions
This project was created at TUMO and uses various Python libraries to recreate the Dino game and integrate reinforcement learning techniques. The project leverages Gymnasium to create the game environment and Stable Baselines3 for implementing DQN, which is an RL algorithm used for training intelligent agents.

Key libraries used:

Pygame: For game rendering and interaction.
Pillow: For displaying animated GIFs (like in the starting screen).
Gymnasium: To define the game environment and interaction.
Stable Baselines3: For the reinforcement learning agent (DQN).

Changes to the Dino Game
In this version, the following changes or improvements have been made to the original game:

Starting Screen: A custom starting screen is added where players can choose to either start the game or view an introductory GIF.
Pygame Integration: The game logic is handled using the Pygame library, which allows for graphical rendering and event handling in Python.
Reinforcement Learning: An agent can be trained using Deep Q-Network (DQN), which enables the agent to learn how to play the game autonomously by rewarding it for correct actions (avoiding obstacles) and penalizing it for wrong actions (crashing into obstacles).

How the DQN Agent Works
The DQN Agent is a deep reinforcement learning agent that learns the optimal strategy for playing the Dino game by interacting with the environment. Here's how the process works:

State Representation: The agent perceives the game state, including the Dino’s position and the location of obstacles.

Action Selection: The agent chooses an action (jump or do nothing) based on its current state, which is mapped to a Q-value function. The agent selects actions that maximize its cumulative reward over time.

Learning: The agent is trained using a neural network that updates Q-values based on feedback from the environment. It uses the Deep Q-Learning algorithm to learn the optimal behavior.

Reward System: The agent receives positive rewards for jumping over obstacles successfully and negative rewards for colliding with them.


How to Train the RL Agent
The train_agent.py script will train the agent over multiple episodes. The agent will gradually learn to play the game better by adjusting its policy to maximize the reward over time. You can modify the training script to change parameters like the number of episodes or the learning rate.


![game](https://github.com/user-attachments/assets/1d063072-59fb-4937-afd9-73b7af77c698)



