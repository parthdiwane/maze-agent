import pygame 
import numpy as np
import random

class Enviorment:
    def __init__(self, screen_width, screen_height, cell_size):
        self.maze_w = screen_width
        self.maze_h = screen_height
        self.cell_size = cell_size

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (192, 192, 192)

        # agent params
        self.px = 0 
        self.py = 0

        self.maze = None
    
    def create_maze(self):
        """
            function returns maze as a matrix

            1 represents border 
            0 represents free moving space 
            2 represents end of maze (always going to be the bottom right point)
        """
        self.maze = np.zeros((self.maze_h, self.maze_w))
        self.maze[0, :] = 1  # top border
        self.maze[-1, :] = 1  # bottom border
        self.maze[:, 0] = 1  # left border
        self.maze[:, -1] = 1  # right border

        for i in range(2, self.maze_h-2, 2):
            for j in range(2, self.maze_w-2, 2):
                if np.random.random() < 0.3:  # 30% chance of wall
                    self.maze[i, j] = 1
        
        # end of maze
        self.maze[1,1] = 0
        self.maze[self.maze_h-2, self.maze_w-2] = 2 
    
        return self.maze
    
    def draw_maze(self, screen, maze):
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen,self.BLACK,(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif maze[y][x] == 2:
                    pygame.draw.rect(screen,self.RED,(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
    

    
    def draw_agent_path(self, screen):
        pygame.draw.rect(screen, self.GREEN, (self.px * self.cell_size, self.py * self.cell_size, self.cell_size,self.cell_size))

    def reset(self):
        self.px, self.py = 1, 1
        return self._get_state()


    def step(self, action):
        """
            0 = up
            1 = down 
            2 = left 
            3 = right
        """
        dx, dy = 0, 0
        if action == 0:  # up
            dy = -1
        elif action == 1:  # down
            dy = 1
        elif action == 2:  # left
            dx = -1
        else:  # right
            dx = 1

        new_x = self.px + dx
        new_y = self.py + dy

        # Check if move is within bounds
        if not ((new_x >= 0 and new_x < self.maze_w) and (new_y >= 0 and new_y < self.maze_h)):
            reward = -0.75
            print(f"Hit boundary at ({new_x}, {new_y})")
        else:
            if self.maze[new_y][new_x] == 1: # hit wall
                reward = -0.75
                print(f"Hit wall at ({new_x}, {new_y})")
            else:
                reward = -0.01
                self.px, self.py = new_x, new_y

        # Check if reached goal
        done = (self.px == self.maze_w - 2 and self.py == self.maze_h - 2)
        if done:
            reward = 1.0
            print(f"reached end")
        return self._get_state(), reward, done, {}
    

    def _get_state(self):
        # normalized x and y positions of the agent
        return np.array([self.px / self.maze_w, self.py / self.maze_h], dtype=np.float32) 