
from pygame import image, Rect, Surface
from load_tiles import load_tiles, SIZE
from generate_maze import create_maze

def parse_map(data):
    return [list(row) for row in data.strip().split('\n')]

level = parse_map(create_maze(12, 7))
level[1][1] = '*'
level[5][10] = 'x'

def draw_map(data, img, tiles):
    """Returns an image of a tile-based map"""
    xs = len(data[0]) * SIZE
    ys = len(data) * SIZE
    map_img = Surface((xs, ys))
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            map_img.blit(img, Rect((x*SIZE, y*SIZE, 0, 0)), tiles[char])
    return map_img


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    m = draw_map(level, tile_img, tiles)
    image.save(m, 'map.png')
