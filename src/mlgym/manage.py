'''
Manage games (where is the execution path, ...) in the MLGym.
'''

from io import BytesIO
import json
import os
import requests
from typing import Dict
import zipfile

MLGYM_GAMES_URL = 'https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/mlgym/master/games.json'

def get_games() -> Dict:
    response = requests.get(MLGYM_GAMES_URL)
    games = json.loads(response.content)
    return games

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
    game_url = games[name]
    response = requests.get(game_url)
    game_path = f'games/{name}'
    zipfile.ZipFile(BytesIO(response.content)).extractall(game_path)
    add(name, game_path)

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
    os.rmdir(games[name]['path'])
    remove(name)