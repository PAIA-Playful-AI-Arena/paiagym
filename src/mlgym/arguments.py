import argparse

parser = argparse.ArgumentParser()


parser.add_argument('-v', '--verbosity', help='increase output verbosity')
parser.add_argument('-i', '--input-ai', action='append', help='the scripts of players')

args = parser.parse_args()

print(args.input_ai)