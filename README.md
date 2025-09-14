# maze-rl


How to run:
    Packages required:
    pygame, numpy, pytorch, matplotlib

    1. run: source/venv/bin/activate
    2. run: python3 sim.py


Sim performs better when multiple sims are used as we get more training data and Q(s,a) is futher improved/


Maze Agent that uses reinforcement leanring to find the end of a maze

we use the standard bellman equation for the Q(s,a)
agent is trained on a Deep Q Network (DQN) and employs strategies like epsilon greedy


Epsilon is orginally at 1 and the decay is 0.995 (decreases slower over time)
gamma = 0.99. This allows the agent to favor future reward as the return is higher over time.


To actually train the agent we employ a mini batch and replay buffer and when the conditions of the replay buffer are met we employ a gradient decent alg to reduce loss. 

