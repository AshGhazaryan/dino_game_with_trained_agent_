import pygame
import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import os
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
DINO_WIDTH, DINO_HEIGHT = 40, 40
GROUND_HEIGHT = 300
FONT_SIZE = 24
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60

class DinoGame(gym.Env):
    def __init__(self):
        super(DinoGame, self).__init__()

        # Action space (0: Do nothing, 1: Jump)
        self.action_space = spaces.Discrete(2)

        # Observation space: (dino_y, dino_velocity, obstacle_x, obstacle_y, obstacle_type)
        self.observation_space = spaces.Box(low=np.array([0, -20, 0, 0, 0]),
                                            high=np.array([SCREEN_HEIGHT, 20, SCREEN_WIDTH, SCREEN_HEIGHT, 2]),
                                            dtype=np.float32)

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Google Dino Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)

        # Initialize game state variables
        self.dino_y = GROUND_HEIGHT - DINO_HEIGHT
        self.dino_velocity = 0
        self.is_jumping = False
        self.jump_count = 0  # Tracks the number of jumps (1 for first jump, 2 for double jump)
        self.obstacle_x = SCREEN_WIDTH
        self.obstacle_speed = 5  # Starting obstacle speed (no increase)
        self.reward = 0
        self.score = 0
        self.high_score = 0  # Initialize the high score
        self.obstacle_type = 'cactus'

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Reset game state
        self.dino_y = GROUND_HEIGHT - DINO_HEIGHT
        self.dino_velocity = 0
        self.is_jumping = False
        self.jump_count = 0  # Reset jump count
        self.obstacle_x = SCREEN_WIDTH
        self.obstacle_speed = 5  # Keep obstacle speed constant
        self.reward = 0
        self.score = 0
        self.obstacle_type = random.choice(['cactus', 'bird'])  # Randomize the obstacle type

        # Initial state: [dino_y, dino_velocity, obstacle_x, obstacle_y, obstacle_type]
        self.state = np.array([self.dino_y, self.dino_velocity, self.obstacle_x, GROUND_HEIGHT - 40, 0], dtype=np.float32)
        return self.state, {}

    def step(self, action):
        """ Takes in the self (DinoGame environment) and an action (int) to take a step in the environment.
            self: DinoGame environment
            action: int action to take in the environment, where 0 is do nothing and 1 is jump
        """
        # Action handling: Jumping
        if action == 1 and self.jump_count < 2:  # Allow up to 2 jumps
            if self.jump_count == 0:  # First jump
                self.dino_velocity = -15  # Negative velocity to move up
            elif self.jump_count == 1:  # Second jump (double jump)
                self.dino_velocity = -12  # Slightly less velocity than the first jump

            self.jump_count += 1  # Increment the jump count

        # Handle jumping physics
        if self.is_jumping or self.jump_count > 0:
            self.dino_y += self.dino_velocity
            self.dino_velocity += 1  # Gravity effect

            if self.dino_y >= GROUND_HEIGHT - DINO_HEIGHT:  # Touch ground
                self.dino_y = GROUND_HEIGHT - DINO_HEIGHT
                self.is_jumping = False
                self.jump_count = 0  # Reset jump count after landing

        # Update obstacle
        self.obstacle_x -= self.obstacle_speed
        if self.obstacle_x < 0:
            self.obstacle_x = SCREEN_WIDTH
            self.score += 1  # Increment score when the obstacle is avoided
            self.obstacle_type = random.choice(['cactus', 'bird'])  # Randomize the obstacle type

        # Check for collisions
        done = False
        if self.obstacle_type == 'cactus':
            if (50 + DINO_WIDTH > self.obstacle_x and  # Dino's right side is beyond obstacle's left side
                50 < self.obstacle_x + 20 and  # Dino's left side is beyond obstacle's right side
                self.dino_y + DINO_HEIGHT > GROUND_HEIGHT - 40):  # Dino is below the cactus
                done = True  # Collision occurs
        elif self.obstacle_type == 'bird':
            if (50 + DINO_WIDTH > self.obstacle_x and  # Dino's right side is beyond obstacle's left side
                50 < self.obstacle_x + 20 and  # Dino's left side is beyond obstacle's right side
                self.dino_y < GROUND_HEIGHT - 80):  # Dino is under the bird
                done = True  # Collision occurs

        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score

        # Update state and reward
        self.state = np.array([self.dino_y, self.dino_velocity, self.obstacle_x, GROUND_HEIGHT - 40,
                               0 if self.obstacle_type == 'cactus' else 1], dtype=np.float32)
        reward = 1 if not done else -100  # Negative reward for collision

        return self.state, reward, done, False, {}

    def render(self, mode="human"):
        self.screen.fill(WHITE)

        # Draw ground line
        pygame.draw.line(self.screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)

        # Draw Dino (represented as a rectangle)
        pygame.draw.rect(self.screen, BLACK, (50, self.dino_y, DINO_WIDTH, DINO_HEIGHT))

        # Draw obstacles
        if self.obstacle_type == 'cactus':
            pygame.draw.rect(self.screen, RED, (self.obstacle_x, GROUND_HEIGHT - 40, 20, 40))
        elif self.obstacle_type == 'bird':
            pygame.draw.rect(self.screen, RED, (self.obstacle_x, GROUND_HEIGHT - 80, 20, 20))  # Flying bird

        # Render score and high score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        high_score_text = self.font.render(f"High Score: {self.high_score}", True, BLACK)
        self.screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))

        # Update screen
        pygame.display.flip()
        self.clock.tick(FPS)

        return self.screen

    def close(self):
        pygame.quit()


# Register the environment
gym.envs.registration.register(
    id='Game-v0',
    entry_point='__main__:DinoGame'
)

if __name__ == "__main__":
    env = DinoGame()
    done = False
    obs, _ = env.reset()

    while not done:
        env.render()
        action = 0  # Default action is doing nothing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                action = 1  # Jump action

        # Apply action to environment
        obs, reward, done, truncated, info = env.step(action)
        print(f"Action: {action}, Reward: {reward}, Done: {done}")

    env.close()


