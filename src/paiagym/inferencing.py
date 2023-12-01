import sys

from paiagym.config import ENV
from paiagym.utils import import_game, import_script

def inferencing() -> None:
    # environment variables
    game_name = ENV.get('GAME_NAME', '')
    input_scripts = ENV.get('INPUT_SCRIPTS', 'ml_play.py').split(':')

    Game = import_game(game_name)
    game = Game()
    env = game.make_env()

    MLPlay = import_script(input_scripts[0])
    player = MLPlay(env)

    observation, info = player.reset()

    while True:
        action = player.predict(observation)
        observation, reward, terminated, truncated, info = player.step(action)

        if terminated or truncated:
            env.close()
            break


if __name__ == '__main__':
    game_name = None
    input_scripts = None
    if len(sys.argv) > 2:
        game_name = sys.argv[1]
        input_scripts = sys.argv[2]
    
    if game_name is not None:
        ENV['GAME_NAME'] = game_name
    if input_scripts is not None:
        ENV['INPUT_SCRIPTS'] = input_scripts
    
    inferencing()