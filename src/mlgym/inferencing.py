import sys
from kart import kart_env
from ml_play import MLPlay

if __name__ == '__main__':
    file_name = None
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    
    env = kart_env(file_name=file_name, render_mode='video')
    player = MLPlay(env, kart_names=['No 1'], seed=None, early_stop=False)

    observation, info = player.env.reset()
    player.env.begin_render(480, 270)

    while True:
        action = player.predict(observation)
        observation, reward, terminated, truncated, info = player.env.step(action)

        if terminated or truncated:
            print('Progress: %.3f' %observation['Progress'])
            player.env.end_render()
            video = player.env.render()
            with open('video.mp4', 'wb') as fout:
                fout.write(video)
                print('Video saved')
            player.env.close()
            break