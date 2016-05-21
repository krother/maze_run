
from load_tiles import load_tiles
from draw_map import draw_map, MAP_DATA
import pygame
from pygame import image, Rect


pygame.init()
pygame.display.set_mode((640, 400))
display = pygame.display.get_surface()


def get_player_pos(mm):
    for y, row in enumerate(mm):
        for x, char in enumerate(row):
            if char == '*':
                return x, y

def move(mm, direction):
    x, y = get_player_pos(mm)
    mm[y][x] = ' '
    if direction == 'LEFT':
        mm[y][x-1] = '*'
    if direction == 'RIGHT':
        mm[y][x+1] = '*'
    if direction == 'UP':
        mm[y-1][x] = '*'
    if direction == 'DOWN':
        mm[y+1][x] = '*'


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    mm = MAP_DATA
    for direction in ['RIGHT', 'RIGHT', 'UP', 'UP', 'LEFT']:
        move(mm, direction)
    img = draw_map(mm, tile_img, tiles)
    image.save(img, 'moved.png')
