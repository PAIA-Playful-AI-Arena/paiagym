from gymnasium import Wrapper
from paiagym.config import bool_ENV

class KartWrapper(Wrapper):
    def __init__(self, env):
        super().__init__(env)

        self.early_stop = bool_ENV('EARLY_STOP', False)

        self.progress = 0
        self.cnt = 0
    
    def reset(self, *, seed=None, options=None):
        self.progress = 0
        self.cnt = 0
        observation, info = self.env.reset(seed=seed, options=options)
        return observation, info

    def step(self, action):
        observation, reward, terminated, truncated, info = self.env.step(action)
        reward = self.new_reward(observation['Progress'], observation['RaySensor'])
        if reward <= -0.1:
            self.cnt += 1
        if self.cnt > 100:
            if self.early_stop:
                truncated = True
        return observation, reward, terminated, truncated, info
    
    def new_reward(self, progress, rays):
        reward = 0

        if rays[0] < 0.5:
            return -0.1

        if progress > self.progress:
            reward = 0.1 + float(progress * 10)
            self.progress = progress
        elif progress < self.progress:
            reward = -0.1 + float((progress - self.progress) * 1000)
        else:
            reward = -0.01
        
        if rays[0] > 0.5 and rays[1] > 0.5 and rays[2] > 0.5 and rays[3] > 0.5 and rays[4] > 0.5:
            reward += 0.01
        
        return reward