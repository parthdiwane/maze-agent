from enviorment import Enviorment
from agent import Agent
import pygame
import time
import numpy 

env = Enviorment(screen_height=800, screen_width=800, cell_size=20)
action_dim = 4 # left, right, up, down
state_space = 2
agent = Agent(action_dim=action_dim,state_dim=state_space,lr=0.001,gamma=0.99,epsilon=1.0,epsilon_decay=0.995,buffer_size=10000)

def runSim():
    batch_size = 32
    done = False
    state = env.reset()
    net_reward = 0


    n_sims = 500
    for game_num in range(n_sims):
        maze = env.create_maze()
        screen = pygame.display.set_mode((env.maze_w, env.maze_h))
        screen.fill(env.WHITE)
        env.draw_maze(screen,maze)
        env.draw_agent_path(screen)
        while not done:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = (0.01 * next_state) + 0.99 * state # soft launch state
            agent.remember(state, action, reward, next_state, done)
            state = next_state

            net_reward += reward
            agent.replay(batch_size=batch_size)
        
            if env.px == env.maze_w - 1 and env.py == env.maze_h - 1:
                done = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
        print(f"Game Number: {game_num + 1}, total reward: {net_reward}")\

if __name__ == "__main__":
    runSim()