'''
Manage games (where is the execution path, ...) in the PAIAGym.
'''

from io import BytesIO
import json
import os
import sys
import requests
import shutil
from sys import platform
import zipfile
from typing import List

def list_all_games() -> List:
    games_dir = os.path.join(os.path.dirname(__file__), 'games')
    games = [f for f in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, f))]
    return games

def list_available_games(mode: str=None) -> List:
    info_path = os.path.join(os.path.dirname(__file__), f'games/games-info.json')
    games = {}
    if os.path.exists(info_path):
        with open(info_path, 'r') as fin:
            games = json.load(fin)
    
    available_games = []
    for name in games:
        if mode is None or games[name]['mode'] == mode:
            available_games.append(name)
    
    return available_games

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
        zipfile.ZipFile(BytesIO(response.content), 'r').extractall(os.path.join(game_path, 'build'))

def add(name: str, path: str, mode: str='dev') -> None:
    info_path = os.path.join(os.path.dirname(__file__), f'games/games-info.json')
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
    info_path = os.path.join(os.path.dirname(__file__), f'games/games-info.json')
    games = {}
    if os.path.exists(info_path):
        with open(info_path, 'r') as fin:
            games = json.load(fin)
    if name in games:
        del games[name]
    with open(info_path, 'w') as fout:
        json.dump(games, fout, indent=4)

def uninstall(name: str) -> None:
    game_path = os.path.join(os.path.dirname(__file__), f'games/{name}/build')
    if os.path.exists(game_path):
        shutil.rmtree(game_path)
    remove(name)

if __name__ == '__main__':
    games = []
    game = None
    path = None
    if len(sys.argv) > 1:
        op = sys.argv[1]
        if op == 'ls':
            games = []
            if len(sys.argv) > 2:
                if sys.argv[2] == '-a':
                    games = list_all_games()
                if sys.argv[2] == '-m':
                    if len(sys.argv) > 3:
                        mode = sys.argv[3]
                        games = list_available_games(mode)
            else:
                games = list_available_games()
            print('\n'.join(games))
        elif op == 'add':
            if len(sys.argv) > 2:
                game = sys.argv[2]
                if len(sys.argv) > 3:
                    path = sys.argv[3]
                add(game, path)
        elif op == 'install':
            if len(sys.argv) > 2:
                game = sys.argv[2]
                install(game)
        elif op == 'update':
            if len(sys.argv) > 2:
                game = sys.argv[2]
                if len(sys.argv) > 3:
                    path = sys.argv[3]
                update(game, path)
        elif op == 'remove':
            if len(sys.argv) > 2:
                game = sys.argv[2]
                remove(game)
        elif op == 'uninstall':
            if len(sys.argv) > 2:
                game = sys.argv[2]
                uninstall(game)