'''
Manage games (where is the execution path, ...) in the PAIAGym.
'''

from io import BytesIO
import json
import os
import shutil
from sys import platform
import requests
from typing import List

from paiagym.utils import unzip

def list_games() -> List:
    games_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'games')
    games = [f for f in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, f))]
    return games

def download_game(game_path: str) -> None:
    with open(os.path.join(game_path, 'game.json'), 'r') as fin:
        game = json.load(fin)
    
    game_url = None
    if 'url' in game:
        if platform == 'win32':
            if 'windows' in game['url'] and game['url']['windows'] is not None:
                game_url = game['url']['windows']
        elif platform == 'linux' or platform == 'linux2':
            if 'linux' in game['url'] and game['url']['linux'] is not None:
                game_url = game['url']['linux']
        elif platform == 'darwin':
            if 'mac' in game['url'] and game['url']['mac'] is not None:
                game_url = game['url']['mac']
    
    if game_url is not None:
        response = requests.get(game_url)
        unzip(BytesIO(response.content), os.path.join(game_path, 'build'))

def add(name: str, path: str, mode: str='dev') -> None:
    info_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'games/games-info.json')
    games = {}
    if os.path.exists(info_path):
        with open(info_path, 'r') as fin:
            games = json.load(fin)
    games[name] = { 'name': name, 'mode': mode, 'path': os.path.abspath(path) }
    with open(info_path, 'w') as fout:
        json.dump(games, fout, indent=4)

def install(name: str) -> None:
    uninstall(name)
    game_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'games/{name}')
    download_game(game_path)
    add(name, game_path, mode='prod')

def update(name: str, path: str) -> None:
    remove(name)
    if path is None:
        install(name)
    else:
        add(name, path)

def remove(name: str) -> None:
    info_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'games/games-info.json')
    games = {}
    if os.path.exists(info_path):
        with open(info_path, 'r') as fin:
            games = json.load(fin)
    if name in games:
        del games[name]
    with open(info_path, 'w') as fout:
        json.dump(games, fout, indent=4)

def uninstall(name: str) -> None:
    game_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'games/{name}/build')
    if os.path.exists(game_path):
        shutil.rmtree(game_path)
    remove(name)