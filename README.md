# PAIAGym

A platform to run Gymnasium or PettingZoo games with AI.

## Installation

```
pip install paiagym
```

## Usage

Install a game:
```
paiagym install <game_name>
```

Uninstall a game:
```
paiagym uninstall <game_name>
```

Run the inferencing with given information by the environment variable:
```
paiagym run
```

Run the inferencing with given script path:
```
paiagym run <game_name> -i <script_path>
```

Run the training with given information by the environment variable:
```
paiagym train
```

Run the training with given script path:
```
paiagym train <game_name> -i <script_path>
```

List all added games:
```
paiagym ls
```

List all available games:
```
paiagym ls -a
```

List games in development:
```
paiagym ls -m dev
```

List games in production:
```
paiagym ls -m prod
```

## Usage for Container

You can checkout the Dockerfile for the Docker container.

To build the Docker image:
```
docker build -t paiagym:base . --no-cache
```

If you are using Linux server, run before starting the container (install and config X server with NVIDIA Driver):
```
sudo sh display.sh
```
display.sh can be found at [display.sh](https://github.com/PAIA-Playful-AI-Arena/paiagym/blob/master/display.sh).

To start the container:
```
docker run -it --rm --gpus all -v /tmp/.X11-unix:/tmp/.X11-unix paiagym:base
```