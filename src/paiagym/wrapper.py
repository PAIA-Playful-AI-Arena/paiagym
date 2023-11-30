from gymnasium import Wrapper

class GameData:
    def __init__(self):
        self.action = None
        self.observation = None
        self.reward = None
        self.terminated = None
        self.truncated = None
        self.info = None

class PAIAWrapper(Wrapper):
    def __init__(self, env, result_handler=None):
        super().__init__(env)
        self.env = env
        self.game_data = GameData()
        self.result = None
        self._result_handler = result_handler
    
    def reset(self, *, seed=None, options=None):
        observation, info = self.env.reset(seed=seed, options=options)
        self.game_data.observation = observation
        self.game_data.info = info
        self.game_handlers()

        self.env.unwrapped.begin_render(960, 540)
        
        return observation, info

    def step(self, action):
        observation, reward, terminated, truncated, info = self.env.step(action)
        self.game_data.action = action
        self.game_data.observation = observation
        self.game_data.reward = reward
        self.game_data.terminated = terminated
        self.game_data.truncated = truncated
        self.game_data.info = info
        self.game_handlers()
        return observation, reward, terminated, truncated, info

    def game_handlers(self):
        if self._result_handler is not None:
            self.result = self._result_handler(self.env, self.game_data)
        
        if self.game_data.terminated or self.game_data.truncated:
            print(self.result)

            self.env.unwrapped.end_render()
            video = self.env.render()
            with open('video.mp4', 'wb') as fout:
                fout.write(video)
                print('Video saved')