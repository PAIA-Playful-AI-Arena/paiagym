import importlib
import json
import os
import sys

def get_module(path: str) -> str:
    # Get the module (the definition of the MLPlay class) name
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    
    sys.path.insert(0, os.path.dirname(path))
    
    module = os.path.basename(path)
    if module.endswith('.py'):
        module = module[:-3]
    
    return module

def import_game(name: str):
    games = {}
    if os.path.exists('games/list.json'):
        with open('games/list.json', 'r') as fin:
            games = json.load(fin)
    game_dir = games[name]['path']

    with open(os.path.join(game_dir, 'game.json'), 'r') as fin:
        game_info = json.load(fin)
    game_path = os.path.join(game_dir, game_info['script'])
    module = get_module(game_path)
    game = importlib.import_module(module)
    return game.Game

def import_script(script_path: str):
    module = get_module(script_path)
    ml_play = importlib.import_module(module)
    return ml_play.MLPlay