
# Chapter 08 - 

# cleaned code for loading tiles

import csv
import os

CONFIG_PATH = os.path.split(__file__)[0]
TILE_POSITION_FILE = CONFIG_PATH + 'tiles.txt'


def load_tile_positions(filename):
    """Returns a list of (name, x, y) tuples parsed from the file"""
    tile_positions = []
    with open(filename) as f:
        for row in csv.reader(f, delimiter='\t'):
            name = row[0]
            if not name.startswith('REMARK'):
                x = int(row[1])
                y = int(row[2])
                tile_positions.append((name, x, y))
    return tile_positions


if __name__ == '__main__':
    tile_positions = load_tile_positions(TILE_POSITION_FILE)
    print(tile_positions)
