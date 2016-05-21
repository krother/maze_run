from draw_map import draw_grid, parse_grid
from event_loop import event_loop
from generate_maze import create_maze
from load_tiles import load_tiles
from moves import move, LEFT, RIGHT, UP, DOWN
from pygame import Rect
import pygame

pygame.init()
pygame.display.set_mode((800, 600))
display = pygame.display.get_surface()


DIRECTIONS = {
    276: LEFT, 275: RIGHT,
    273: UP, 274: DOWN
}


def game(key):
    """Handles key events in the game"""
    direction = DIRECTIONS.get(key)
    if direction:
        move(maze, direction)
    img = draw_grid(maze, tile_img, tiles)
    display.blit(img, Rect((0, 0, 384, 224)), Rect((0, 0, 384, 224)))
    pygame.display.update()


if __name__ == '__main__':
    maze = parse_grid(create_maze(12, 7))
    maze[1][1] = '*'
    maze[5][10] = 'x'
    tile_img, tiles = load_tiles()
    img = draw_grid(maze, tile_img, tiles)
    display.blit(img, Rect((0, 0, 384, 224)), Rect((0, 0, 384, 224)))
    pygame.display.update()
    event_loop(game)
