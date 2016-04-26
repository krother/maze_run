import pygame
from pygame import Rect
from draw_map import draw_grid, parse_grid
from event_loop import event_loop
from generate_maze import create_maze
from load_tiles import load_tiles
from moves import move, LEFT, RIGHT, UP, DOWN

pygame.init()
pygame.display.set_mode((800, 600))
display = pygame.display.get_surface()


DIRECTIONS = {
    276: LEFT, 275: RIGHT,
    273: UP, 274: DOWN
}

maze = parse_grid(create_maze(12, 7))

def game(key):
    """Handles key events in the game"""
    move(maze, DIRECTIONS.get(key, 0))
    map_img = draw_grid(maze, tile_img, tiles)
    display.blit(map_img, Rect((0, 0, 1784, 1524)), Rect((0, 0, 1784, 1524)))
    pygame.display.update()


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    maze[1][1] = '*'
    maze[5][10] = 'x'
    map_img = draw_grid(maze, tile_img, tiles)
    display.blit(map_img, Rect((0, 0, 384, 224)), Rect((0, 0, 384, 224)))
    pygame.display.update()
    event_loop(game)
