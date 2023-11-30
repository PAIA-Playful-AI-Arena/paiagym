import importlib
import json
import os
import sys
import typing
import zipfile

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
    if os.path.exists('games/games-info.json'):
        with open('games/games-info.json', 'r') as fin:
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

def _is_root(info: zipfile.ZipInfo) -> bool:
    if info.is_dir():
        parts = info.filename.split('/')
        # Handle directory names with and without trailing slashes.
        if len(parts) == 1 or (len(parts) == 2 and parts[1] == ''):
            return True
    return False

def _members_without_root(archive: zipfile.ZipFile, root_filename: str) -> typing.Generator:
    for info in archive.infolist():
        parts = info.filename.split(root_filename)
        if len(parts) > 1 and parts[1]:
            # We join using the root filename, because there might be a subdirectory with the same name.
            info.filename = root_filename.join(parts[1:])
            yield info

def unzip(zip_path: str, destination: str) -> None:
    with zipfile.ZipFile(zip_path, mode='r') as archive:
        # We will use the first directory with no more than one path segment as the root.
        root = next(info for info in archive.infolist() if _is_root(info))
        if root:
            archive.extractall(path=destination, members=_members_without_root(archive, root.filename))
        else:
            print("No root directory found in zip.")