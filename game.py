from env import DinoGame
import pygame
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