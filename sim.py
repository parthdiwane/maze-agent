from enviorment import Enviorment
from agent import Agent
import pygame
import time
import numpy 

pygame.init()

env = Enviorment(screen_height=800, screen_width=800, cell_size=20)
action_dim = 4 # left, right, up, down
state_space = 2 # x, y cord
agent = Agent(action_dim=action_dim,state_dim=state_space,lr=0.001,gamma=0.99,epsilon=1.0,epsilon_decay=0.995,buffer_size=10000)

def runSim():
    batch_size = 32
    n_sims = 10

    screen = pygame.display.set_mode((env.maze_w, env.maze_h))
    pygame.display.set_caption("Maze Sim")

    for game_num in range(n_sims):
        done = False
        state = env.reset()
        net_reward = 0
        step_cnt = 0
        max_step = 700 # prevent inf loop

        maze = env.create_maze()
        while not done and step_cnt < max_step:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)

            agent.remember(state, action, reward, next_state, done)
            state = next_state
            net_reward += reward
            step_cnt += 1

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
            
            screen.fill(env.WHITE)
            env.draw_maze(screen, maze)
            env.draw_agent_path(screen)
            pygame.display.flip()

            if env.px == env.maze_w - 1 and env.py == env.maze_h - 1:
                done = True
                print(f"Maze completed! Reward: {net_reward}, Steps: {step_cnt}")
            if step_cnt >= max_step:
                print(f"Terminated. Reward: {net_reward}")

        time.sleep(0.1)

    pygame.quit() 



if __name__ == "__main__":
    runSim()