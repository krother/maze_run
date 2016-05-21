
from pygame import image, Rect, Surface
from load_tiles import load_tiles, get_tile_rect, SIZE
from generate_maze import create_maze

def parse_map(data):
    return data.strip().split('\n')

level = create_maze(12, 7)
level = parse_map(level)
#level = ['#']

def draw_map(data, img, tiles):
    """Returns an image of a tile-based map"""
    xs = len(data[0]) * SIZE
    ys = len(data) * SIZE
    map_img = Surface((xs, ys))
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            rect = get_tile_rect(xs, ys)
            map_img.blit(img, tiles[char], rect)
        return map_img


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    m = draw_map(level, tile_img, tiles)
    image.save(m, 'maze.png')
