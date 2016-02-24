
from load_tiles import load_tiles
from draw_map import draw_map, level
import pygame
from pygame import image, Rect
import sys


pygame.init()
pygame.display.set_mode((640, 400))
display = pygame.display.get_surface()


def get_player_pos(level, player_char='*'):
    """Returns a (x, y) tuple of player char on the level"""
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == player_char:
                return x, y

def move(level, direction):
    """Handles moves on the level"""
    oldx, oldy = get_player_pos(level)
    newx, newy = oldx, oldy
    if direction == 'LEFT':
        newx = newx - 1
    if direction == 'RIGHT':
        newx = newx + 1
    if direction == 'UP':
        newy = newy - 1
    if direction == 'DOWN':
        newy = newy + 1
    if level[newy][newx] == 'x':
        sys.exit(0)
    if level[newy][newx] != '#':
        level[oldy][oldx] = ' '
        level[newy][newx] = '*'


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    mm = MAP_DATA
    for direction in ['RIGHT', 'RIGHT', 'UP', 'UP', 'LEFT']:
        move(mm, direction)
    img = draw_map(mm, tile_img, tiles)
    image.save(img, 'moved.png')
