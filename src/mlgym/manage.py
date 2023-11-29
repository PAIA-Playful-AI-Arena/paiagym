'''
Manage games (where is the execution path, ...) in the MLGym.
'''

import json
import os
import requests
from typing import Dict

MLGYM_GAMES_URL = 'https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/mlgym/master/games.json'

def get_games() -> Dict:
    response = requests.get(MLGYM_GAMES_URL)
    print(response.content)

def add(name: str, path: str) -> None:
    games = {}
    if os.path.exists('games/list.json'):
        with open('games/list.json', 'r') as fin:
            games = json.load(fin)
    games[name] = { 'name': name, 'path': os.path.abspath(path) }
    with open('games/list.json', 'w') as fout:
        json.dump(games, fout, indent=4)

def install(name: str) -> None:
    # TODO: download directly, save in the /games
    add(name, package.path())

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
    # TODO: delete in the /games
    remove(name)