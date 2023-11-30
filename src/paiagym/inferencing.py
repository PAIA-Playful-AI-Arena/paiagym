import sys
from typing import List

from paiagym.utils import import_game, import_script

def inferencing(game_name: str, scripts: List[str]) -> None:
    Game = import_game(game_name)
    game = Game()
    env = game.make_env()

    MLPlay = import_script(scripts[0])
    player = MLPlay(env, kart_names=['No 1'], seed=None, early_stop=False)

    observation, info = player.reset()

    while True:
        action = player.predict(observation)
        observation, reward, terminated, truncated, info = player.step(action)

        if terminated or truncated:
            env.close()
            break


if __name__ == '__main__':
    game_name = None
    script_path = None
    if len(sys.argv) > 2:
        game_name = sys.argv[1]
        script_path = sys.argv[2]
    
    inferencing(game_name=game_name, scripts=[script_path])