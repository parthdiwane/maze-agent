# maze-rl

Maze Agent that uses reienforcement leanring to find the end of a maze

we use the standard bellman equation for the Q(s,a)
agent is trained on a Deep Q Netowork (DQN) and employs strategies like epsilon greedy

Epsilon is orginally at 1 and the decay is 0.995 (decreases slower over time)
gamma = 0.99, which favors current reward over future reward.

