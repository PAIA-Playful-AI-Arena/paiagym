import os
from sys import platform

class PAIAGame:
    def __init__(self):
        self.name = None
        self.result = None
    
    def env(self):
        pass

    def unity_path(self, game_dir: str):
        binary_path = os.path.join(game_dir, 'build')
        game_path = None
        if platform == 'win32':
            game_path = os.path.join(binary_path, 'windows', f'{self.name}', f'{self.name}.exe')
        elif platform == 'linux' or platform == 'linux2':
            game_path = os.path.join(binary_path, 'linux', f'{self.name}.x86_64')
        elif platform == 'darwin':
            game_path = os.path.join(binary_path, 'mac', f'{self.name}.app')
        if os.path.exists(game_path):
            return game_path
        else:
            return None
        
    def result_handler(self, env, game_data):
        pass