import json
import os
from gymnasium import Wrapper

from paiagym.config import ENV, bool_ENV, int_ENV

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
        # environment variables
        record_video = bool_ENV('RECORD_VIDEO', False)
        width = int_ENV('VIDEO_WIDTH', 1920)
        height = int_ENV('VIDEO_HEIGHT', 1080)
        fullscreen = bool_ENV('VIDEO_FULLSCREEN', False)
        
        if record_video:
            env.unwrapped.begin_render(screen_width=width, screen_height=height, fullscreen=fullscreen)
    
    def on_step(self, env, game_data):
        return None # result
    
    def on_finish(self, env, game_data, result):
        # environment variables
        save_game_result = bool_ENV('SAVE_GAME_RESULT', False)
        game_result_dir = os.path.abspath(ENV.get('GAME_RESULT_DIR', 'result'))
        game_result_filename = ENV.get('GAME_RESULT_FILENAME', 'game_result.json')
        record_video = bool_ENV('RECORD_VIDEO', False)
        video_filename = ENV.get('VIDEO_FILENAME', 'video.mp4')

        if record_video or save_game_result:
            if not os.path.exists(game_result_dir):
                os.makedirs(game_result_dir)

        if record_video:
            env.unwrapped.end_render()
            video = env.render()
            video_path = os.path.join(game_result_dir, video_filename)
            with open(video_path, 'wb') as fout:
                fout.write(video)
                print(f'Video saved at {video_path}')
        
        game_result_path = os.path.join(game_result_dir, game_result_filename)
        with open(game_result_path, 'w') as fout:
            game_result = [
                {
                    'player': '1P',
                    'progress': result['progress'],
                    'used_time': result['used_time']
                }
            ]
            print(game_result)
            if save_game_result:
                json.dump(game_result, fout, indent=4)
                print(f'Game result saved at {game_result_path}')