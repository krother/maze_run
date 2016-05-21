
from util import debug_print
from pygame import image, Rect, Surface
from pygame.locals import KEYDOWN
import pygame
import sys
import random
import csv
import os

CONFIG_PATH = os.path.split(__file__)[0]

TILE_POSITION_FILE = CONFIG_PATH + 'tiles.txt'
TILE_IMAGE_FILE = CONFIG_PATH + '../images/tiles.xpm'


# ------------ CONSTANTS ----------------

SIZE = 32

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

DIRECTIONS = {
    276: LEFT, 275: RIGHT,
    273: UP, 274: DOWN
}

# ------------- LOADING TILES -----------

def get_tile_rect(x, y):
    """Converts tile indices to a pygame.Rect"""
    return Rect(x*SIZE, y*SIZE, SIZE, SIZE)

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


def load_tiles(position_filename=TILE_POSITION_FILE, image_filename=TILE_IMAGE_FILE):
    """Returns a tuple of (image, tile_dict)"""
    tile_positions = load_tile_positions(position_filename)
    tile_image = image.load(image_filename)
    tiles = {}
    for symbol, x, y in tile_positions:
        tiles[symbol] = get_tile_rect(x, y)
    return tile_image, tiles


# ------------- GENERATING MAZES ------------

def create_grid_string(dots, xsize, ysize):
    grid = ""
    for y in range(ysize):
        for x in range(xsize):
            grid += "." if (x, y) in dots else "#"
        grid += "\n"
    return grid


def get_all_dot_positions(xsize, ysize):
    return [(x, y) for x in range(1, xsize-1) for y in range(1, ysize-1)]


def get_neighbors(x, y):
    # design flaw: defects are hard to spot in this function
    return [
        (x, y-1), (x, y+1), (x-1, y), (x+1, y),
        (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)
        ]


def generate_dot_positions(xsize, ysize):
    positions = get_all_dot_positions(xsize, ysize)
    dots = set()
    while positions != []:
        x, y = random.choice(positions)
        neighbors = get_neighbors(x, y)
        free = [nb in dots for nb in neighbors]
        if free.count(True) < 5:
            dots.add((x, y))
        positions.remove((x, y))
    return dots


def create_maze(xsize, ysize):
    """Returns a xsize*ysize maze as a string"""
    dots = generate_dot_positions(xsize, ysize)
    maze = create_grid_string(dots, xsize, ysize)
    return maze


# ------------- DRAWING GRIDS --------------

def parse_grid(data):
    """Parses the string representation into a nested list"""
    return [list(row) for row in data.strip().split("\n")]


def draw_grid(data, tile_img, tiles):
    """Returns an image of a tile-based grid"""
    debug_print("drawing level", data)
    xsize = len(data[0]) * SIZE
    ysize = len(data) * SIZE
    img = Surface((xsize, ysize))
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            rect = get_tile_rect(x, y)
            img.blit(tile_img, rect, tiles[char])
    return img

# ------------- GAME MECHANICS --------------

def get_player_pos(level, player_char='*'):
    """Returns a (x, y) tuple of player char on the level"""
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == player_char:
                return x, y


def move(level, direction):
    """Handles moves on the level"""
    oldx, oldy = get_player_pos(level)
    newx = oldx + direction[0]
    newy = oldy + direction[1]
    if level[newy][newx] == 'x':
        sys.exit(0)
    if level[newy][newx] != '#':
        level[oldy][oldx] = ' '
        level[newy][newx] = '*'









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


# previous function changed to use tile positions
def load_tiles(position_filename=TILE_POSITION_FILE, image_filename=TILE_IMAGE_FILE):
    """Returns a tuple of (image, tile_dict)"""
    tile_positions = load_tile_positions(position_filename)
    tile_image = image.load(image_filename)
    tiles = {}
    for symbol, x, y in tile_positions:
        tiles[symbol] = get_tile_rect(x, y)
    return tile_image, tiles

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

def event_loop(callbacks, delay=10, repeat=KEY_REPEAT_TIME):
    """Processes events and updates callbacks."""
    repeat_key = None
    running = True
    while running:
        pygame.event.pump()
        event = pygame.event.poll()
        action = callbacks.get(event.type)
        if action:
            action(event)
        pygame.time.delay(delay)
        if event.type == EXIT:
            running = False

# ------------- GAME MECHANICS --------------

def exit_game():
    eve = pygame.event.Event(EXIT)
    pygame.event.post(eve)

# ------------- MAIN GAME --------------

def load_level(fn):
    data = open(fn).read()
    maze = TileGrid(data)
    return maze

def draw(event):
    img = maze.draw_grid(tile_img, tiles)
    draw_player(img, tile_img, tiles)
    rect = Rect((0, 0, maze.xsize*SIZE, maze.ysize*SIZE))
    display.blit(img, rect, rect)
    pygame.display.update()
    
def handle_key(event):
    """Handles key events in the game"""
    direction = DIRECTIONS.get(event.key)
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


callbacks = {
    KEYDOWN: handle_key,
    DRAW: draw,
}

if __name__ == '__main__':
    size = Position(12, 7)
    display = create_display()
    maze = create_random_maze(size)
    maze[Position(1, 1)] = "*"
    #maze = load_level(LEVEL_FILE)
    tile_img = image.load(TILE_IMAGE_FILE)
    tiles = load_tiles(TILE_POSITION_FILE)
    pygame.time.set_timer(DRAW, DRAW_REPEAT_TIME)
    event_loop(callbacks)

