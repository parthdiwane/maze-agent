import torch 
import torch.nn as nn
import torch.optim as optim 
import torch.nn.functional as F
import numpy as np
from collections import deque
from dqn import DQN
import random

class Agent():
    def __init__(self, state_dim, action_dim, lr, gamma, epsilon, epsilon_decay, buffer_size):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.memory = deque(maxlen=buffer_size)
        self.model = DQN(state_dim, action_dim)
        self.optimizer = optim.Adam(self.model.parameters(),lr=lr)


    """ 
        takes action a

        employs epsilon-greedy algorithm

    """
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_dim)
        q_values = self.model(torch.tensor(state, dtype=torch.float32))
        return torch.argmax(q_values).item()
    

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state,action,reward,next_state,done))
    
    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return 'replay memory length not met'
        minibatch = random.sample(self.memory,batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward 
            if not done:
                target = reward + self.gamma * torch.max(self.model(torch.tensor(next_state, dtype=torch.float32))).item()
            target_f = self.model(torch.tensor(state, dtype=torch.float32)).numpy()
            target_f[action] = target
            self.optimizer.zero_grad()
            loss = nn.MSELoss()(torch.tensor(target_f), self.model(torch.tensor(state, dtype=torch.float32)))
            loss.backward()
            self.optimizer.step()
            

            if self.epsilon > 0.01:
                self.epsilon *= self.epsilon_decay
        