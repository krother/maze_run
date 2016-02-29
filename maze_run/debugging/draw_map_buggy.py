
from pygame import image, Rect, Surface
from load_tiles import load_tiles, SIZE

def parse_map(data):
    return data.strip().split('\n')

level = """
#######
#.....#
#.....#
#.*...#
#.....#
#....x#
#######"""

level = parse_map(level)


def draw_map(data, img, tiles):
    """Returns an image of a tile-based map"""
    xs = len(data[0]) * SIZE
    ys = len(data) * SIZE
    map_img = Surface((xs, ys))
    for x, row in enumerate(data):
        for y, char in enumerate(row):
            map_img.blit(img, tiles[char], Rect((x, y, 0, 0)))
        return map_img


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    m = draw_map(level, tile_img, tiles)
    image.save(m, 'map.png')
