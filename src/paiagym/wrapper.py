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
    def __init__(self, env, on_start=None, on_step=None, on_finish=None):
        super().__init__(env)
        self.env = env
        self.game_data = GameData()
        self.result = None
        self._on_start = self.on_start if on_start is None else on_start
        self._on_step = self.on_step if on_step is None else on_step
        self._on_finish = self.on_finish if on_finish is None else on_finish
    
    def reset(self, *, seed=None, options=None):
        observation, info = self.env.reset(seed=seed, options=options)
        self.game_data.observation = observation
        self.game_data.info = info

        self._on_start(self.env, self.game_data)
        self.result = self._on_step(self.env, self.game_data)
        
        return observation, info

    def step(self, action):
        observation, reward, terminated, truncated, info = self.env.step(action)
        self.game_data.action = action
        self.game_data.observation = observation
        self.game_data.reward = reward
        self.game_data.terminated = terminated
        self.game_data.truncated = truncated
        self.game_data.info = info
        
        self.result = self._on_step(self.env, self.game_data)

        if terminated or truncated:
            self._on_finish(self.env, self.game_data, self.result)

        return observation, reward, terminated, truncated, info
    
    def on_start(self, env, game_data):
        env.unwrapped.begin_render(960, 540)
    
    def on_step(self, env, game_data):
        return None # result
    
    def on_finish(self, env, game_data, result):
        env.unwrapped.end_render()
        video = env.render()
        with open('video.mp4', 'wb') as fout:
            fout.write(video)
            print('Video saved')
        
        print(result)