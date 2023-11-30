import sys
from paiagym.manage import add, install, list_all_games, list_available_games, remove, uninstall, update
from paiagym.inferencing import inferencing
from paiagym.training import training

def main():
    games = []
    game = None
    path = None
    script_path = None

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
        elif op == 'run':
            if len(sys.argv) > 4:
                game = sys.argv[2]
                if sys.argv[3] == '-i':
                    script_path = sys.argv[4]
                    inferencing(game_name=game, scripts=[script_path])
        elif op == 'train':
            if len(sys.argv) > 4:
                game = sys.argv[2]
                if sys.argv[3] == '-i':
                    script_path = sys.argv[4]
                    training(game_name=game, scripts=[script_path])

if __name__ == '__main__':
    main()