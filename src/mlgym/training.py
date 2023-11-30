import sys
from mlgym.games.kart3d.kart3d import kart_env

from mlgym.utils import import_script

if __name__ == '__main__':
    file_name = None
    script_path = None
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    if len(sys.argv) > 2:
        script_path = sys.argv[2]
    
    env = kart_env(file_name=file_name)
    MLPlay = import_script(script_path)
    player = MLPlay(env, kart_names=['No 1'], seed=None, early_stop=True)
    player.learn(total_timesteps=100_000)
    player.env.close()