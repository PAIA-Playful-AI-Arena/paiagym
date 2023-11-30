import sys

from paiagym.utils import import_game, import_script

if __name__ == '__main__':
    script_path = None
    if len(sys.argv) > 1:
        script_path = sys.argv[1]
    
    Game = import_game('kart3d')
    game = Game()
    env = game.env(file_name=game.unity_path())

    MLPlay = import_script(script_path)
    player = MLPlay(env, kart_names=['No 1'], seed=None, early_stop=True)
    player.learn(total_timesteps=100_000)
    player.env.close()