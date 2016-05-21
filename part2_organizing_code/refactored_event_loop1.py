"""
Part II - Organizing Code

LOGGING
  TODO: log scripted moves
  TODO: replay functionality
  TODO: use 2-3 output channels

COMMAND-LINE INTERFACE
  added command-line arguments
    TODO: fix and check all

"""

from util import debug_print
from pygame import image, Rect, Surface
from pygame.locals import KEYDOWN, KEYUP, USEREVENT
import pygame
import sys
import random
import json
import os
from collections import namedtuple
from functools import partial
import argparse

# ------------ CONSTANTS ----------------

CONFIG_PATH = os.path.split(__file__)[0]

TILE_POSITION_FILE = CONFIG_PATH + 'tiles.json'
TILE_IMAGE_FILE = CONFIG_PATH + '../images/tiles.xpm'

LEVEL_FILE = 'level.txt'

SIZE = 32
SPEED = 4

Position = namedtuple("Position", ["x", "y"])

LEFT = Position(-1, 0)
RIGHT = Position(1, 0)
UP = Position(0, -1)
DOWN = Position(0, 1)

DIRECTIONS = {
    276: LEFT, 275: RIGHT,
    273: UP, 274: DOWN
}

KEY_REPEAT_TIME = 250
KEY_REPEATED = USEREVENT + 1

DRAW_REPEAT_TIME = 100
DRAW = USEREVENT + 2

UPDATE = USEREVENT + 3
UPDATE_REPEAT_TIME = 20

MOVE_GHOST = USEREVENT + 4
MOVE_GHOST_TIME = 500

EXIT = USEREVENT + 5

# !! potential concurrency issues when timers too tight

# ------------- LOADING TILES -----------

def get_tile_rect(pos):
    """Converts tile indices to a pygame.Rect"""
    return Rect(pos.x*SIZE, pos.y*SIZE, SIZE, SIZE)

def load_tiles(json_fn):
    """Loads tile positions from a JSON file name"""
    tiles = {}
    jd = json.loads(open(json_fn).read())
    for tile in jd.values():
        abbrev = tile["abbrev"]
        pos = Position(tile["x"], tile["y"])
        rect = get_tile_rect(pos)
        tiles[abbrev] = rect
    return tiles


# ------------- GENERATING MAZES ------------

class MazeGenerator:
    """Generates two-dimensional mazes consisting of walls and dots."""
    
    @staticmethod
    def create_grid_string(dots, xsize, ysize):
        grid = ""
        for y in range(ysize):
            for x in range(xsize):
                grid += "." if Position(x, y) in dots else "#"
            grid += "\n"
        return grid

    @staticmethod
    def get_all_dot_positions(xsize, ysize):
        return [Position(x, y) for x in range(1, xsize-1) for y in range(1, ysize-1)]

    @staticmethod
    def get_neighbors(pos):
        return [
            Position(pos.x  , pos.y-1), Position(pos.x  , pos.y+1), 
            Position(pos.x-1, pos.y  ), Position(pos.x+1, pos.y  ),
            Position(pos.x-1, pos.y-1), Position(pos.x+1, pos.y-1), 
            Position(pos.x-1, pos.y+1), Position(pos.x+1, pos.y+1)
            ]

    @staticmethod
    def generate_dot_positions(xsize, ysize):
        positions = MazeGenerator.get_all_dot_positions(xsize, ysize)
        dots = set()
        while positions != []:
            pos = random.choice(positions)
            neighbors = MazeGenerator.get_neighbors(pos)
            free = [nb in dots for nb in neighbors]
            if free.count(True) < 5:
                dots.add(pos)
            positions.remove(pos)
        return dots

    @staticmethod
    def create_maze(size):
        """Returns a size.x * size.y maze as a string"""
        dots = MazeGenerator.generate_dot_positions(size.x, size.y)
        maze = MazeGenerator.create_grid_string(dots, size.x, size.y)
        return maze

# ------------- DRAWING GRIDS --------------

class TileGrid:

    def __init__(self, data):
        self._grid = self.parse_grid(data)

    def parse_grid(self, data):
        """Parses the string representation into a nested list"""
        return [list(row) for row in data.strip().split("\n")]

    @property
    def rows(self):
        return self._grid
    
    @property
    def xsize(self):
        return len(self.rows[0])

    @property
    def ysize(self):
        return len(self.rows)

    def __getitem__(self, pos):
        return self._grid[pos.y][pos.x]

    def __setitem__(self, pos, value):
        self._grid[pos.y][pos.x] = value

    def __iter__(self):
        """Iterate over all grid tiles"""
        for y, row in enumerate(self.rows):
            for x, char in enumerate(row):
                pos = Position(x, y)
                yield pos, char
        
    def find_tile(self, query='*'):
        """Returns a Position tuple for the given char on the level"""
        for pos, char in self:
            if char == query:
                return pos

    def draw_grid(self, tile_img, tiles):
        """Returns an image of a tile-based grid"""
        #debug_print("drawing level", data)
        img = Surface((self.xsize * SIZE, self.ysize * SIZE))
        for pos, char in self:
            rect = get_tile_rect(pos)
            img.blit(tile_img, rect, tiles[char])
        return img

# ------------- SPRITES --------------


def move(level, direction):
    """Handles moves on the level"""
    old = level.find_tile("*")
    # avoids problem with finding: if '*' on map it might not be there
    new = Position(old.x + direction.x, old.y + direction.y)
    if level[new] in [" ", ".", "x"]:
        level[old] = ' '
        if level[new] == 'x':
            exit_game()
        level[new] = '*'


def draw_player(img, tile_img, tiles):
    """Returns an image of a tile-based grid"""
    pos = maze.find_tile("*")
    rect = get_tile_rect(pos)
    img.blit(tile_img, rect, tiles["*"])

# ------------- EVENT LOOP --------------

def event_loop(handle_key, delay=10, repeat=KEY_REPEAT_TIME):
    """Processes events and updates callbacks."""
    repeat_key = None
    running = True
    while running:
        pygame.event.pump()
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            handle_key(event.key)
            repeat_key = event.key
            pygame.time.set_timer(KEY_REPEATED, KEY_REPEAT_TIME)
        elif event.type == KEYUP:
            if event.key == repeat_key:
                repeat_key = None
                pygame.time.set_timer(KEY_REPEATED, 0)
        elif event.type == KEY_REPEATED:
            handle_key(repeat_key)
        elif event.type == DRAW:
            draw()
        elif event.type == EXIT:
            running = False
        pygame.time.delay(delay)

# ------------- GAME MECHANICS --------------

def exit_game():
    eve = pygame.event.Event(EXIT)
    pygame.event.post(eve)

# ------------- MAIN GAME --------------

def load_level(fn):
    data = open(fn).read()
    maze = TileGrid(data)
    return maze

def draw():
    img = maze.draw_grid(tile_img, tiles)
    draw_player(img, tile_img, tiles)
    rect = Rect((0, 0, maze.xsize*SIZE, maze.ysize*SIZE))
    display.blit(img, rect, rect)
    pygame.display.update()
    
def game(key):
    """Handles key events in the game"""
    direction = DIRECTIONS.get(key)
    if direction:
        move(maze, direction)

def create_random_maze(size):
    maze_data = MazeGenerator.create_maze(size)
    maze = TileGrid(maze_data)
    maze[Position(size.x-2, size.y-2)] = 'x'
    return maze

def create_display():
    pygame.init()
    pygame.display.set_mode((800, 600))
    display = pygame.display.get_surface()
    return display


if __name__ == '__main__':
    size = Position(12, 7)
    display = create_display()
    maze = create_random_maze(size)
    maze[Position(1, 1)] = "*"
    #maze = load_level(LEVEL_FILE)
    tile_img = image.load(TILE_IMAGE_FILE)
    tiles = load_tiles(TILE_POSITION_FILE)
    pygame.time.set_timer(DRAW, DRAW_REPEAT_TIME)
    event_loop(game)
