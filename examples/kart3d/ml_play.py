import os
from stable_baselines3 import PPO

from wrapper import KartWrapper

class MLPlay:
    def __init__(self, env):
        self.env = KartWrapper(env)

        self.model_name = 'kart_model_ppo_vec'
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.model_name + '.zip')
        if os.path.exists(model_path):
            self.model = PPO.load(model_path, env=self.env)
        else:
            self.model = PPO('MultiInputPolicy', env=self.env, verbose=1)

    def learn(self, total_timesteps):
        self.model.learn(total_timesteps=total_timesteps, log_interval=1)
        self.model.save(self.model_name)
    
    def reset(self):
        return self.env.reset()
    
    def predict(self, observation):
        action, _states = self.model.predict(observation)
        return action

    def step(self, action):
        return self.env.step(action)