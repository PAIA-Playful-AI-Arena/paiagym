import sys

from paiagym.utils import import_game, import_script

if __name__ == '__main__':
    script_path = None
    if len(sys.argv) > 1:
        script_path = sys.argv[1]
    
    Game = import_game('kart3d')
    game = Game()
    env = game.env(file_name=game.unity_path(), render_mode='video')

    MLPlay = import_script(script_path)
    player = MLPlay(env, kart_names=['No 1'], seed=None, early_stop=False)

    observation, info = player.env.reset()
    player.env.unwrapped.begin_render(960, 540)

    while True:
        action = player.predict(observation)
        observation, reward, terminated, truncated, info = player.env.step(action)

        if terminated or truncated:
            print('Progress: %.3f' %observation['Progress'])
            player.env.unwrapped.end_render()
            video = player.env.render()
            with open('video.mp4', 'wb') as fout:
                fout.write(video)
                print('Video saved')
            player.env.close()
            break