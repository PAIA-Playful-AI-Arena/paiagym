'''
Manage games (where is the execution path, ...) in the PAIAGym.
'''

from io import BytesIO
import json
import os
import shutil
from sys import platform
import requests
from typing import Dict
import zipfile

PAIAGYM_GAMES_URL = 'https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/paiagym/master/games.json'

def get_games() -> Dict:
    response = requests.get(PAIAGYM_GAMES_URL)
    games = json.loads(response.content)
    return games

def download_game(game_path: str) -> None:
    with open(os.path.join(game_path, 'game.json'), 'wb') as fin:
        game = json.load(fin)
    
    if platform == 'win32':
        pass
    elif platform == 'linux' or platform == 'linux2':
        pass
    elif platform == 'darwin':
        pass

def add(name: str, path: str) -> None:
    games = {}
    if os.path.exists('games/list.json'):
        with open('games/list.json', 'r') as fin:
            games = json.load(fin)
    games[name] = { 'name': name, 'path': os.path.abspath(path) }
    with open('games/list.json', 'w') as fout:
        json.dump(games, fout, indent=4)

def install(name: str) -> None:
    games = get_games()
    if not name in games or games[name] is None:
        game_url = f'https://github.com/PAIA-Playful-AI-Arena/paiagym-{name}/archive/refs/heads/master.zip'
    else:
        game_url = games[name]
    response = requests.get(game_url)
    game_path = f'games/{name}'
    zipfile.ZipFile(BytesIO(response.content)).extractall(game_path)
    download_game(game_path)
    add(name, game_path)

def update(name: str, path: str) -> None:
    remove(name)
    if path is None:
        install(name)
    else:
        add(name, path)

def remove(name: str) -> None:
    games = {}
    if os.path.exists('games/list.json'):
        with open('games/list.json', 'r') as fin:
            games = json.load(fin)
    if name in games:
        del games[name]
    with open('games/list.json', 'w') as fout:
        json.dump(games, fout, indent=4)

def uninstall(name: str) -> None:
    if os.path.exists('games/list.json'):
        with open('games/list.json', 'r') as fin:
            games = json.load(fin)
    shutil.rmtree(games[name]['path'])
    remove(name)