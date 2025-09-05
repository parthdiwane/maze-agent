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
    
    def create_maze(self):
        """
            function returns maze as a matrix
            1 represents border 
            0 represents free moving space 
            2 represents end of maze (always going to be the bottom right point)
        """
        maze = [[0] * self.maze for _ in range(self.maze_h)]
        # randomly add borders
        for _ in range(200):
            x = random.randint(0, self.maze_w - 1)
            y = random.randint(0, self.maze_h - 1)
            maze[y][x] = 1
    
        # end of maze is bottom right corner
        maze[self.maze_h - 1][self.maze_w - 1] = 2

        return maze
    
    def draw_maze(self, screen, maze):
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen,self.BLACK,(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif maze[y][x] == 2:
                    pygame.draw.rect(screen,self.RED,(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
    


    def move(self, dx, dy, maze):
        new_x = dx + self.px
        new_y = dy + self.py

        if 0 <= new_x < self.maze_w and 0 <= new_y < self.maze_h and maze[new_y][new_x] != 1:
            self.px = new_x
            self.py = new_y
    
    def draw_agent_path(self, screen):
        pygame.draw.rect(screen, self.GREEN, (self.px * self.cell_size, self.py * self.cell_size, self.cell_size,self.cell_size))
        