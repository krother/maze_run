
from pygame import image, Rect, Surface
from load_tiles import load_tiles

SIZE = 32

MAP_DATA = """
#######
#     #
#     #
# *   #
#     #
#     #
#######""".strip().split('\n')

def draw_map(data, img, tiles):
    xs = len(data[0]) * SIZE
    ys = len(data) * SIZE
    m = Surface((xs, ys))
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            m.blit(img, Rect((x*SIZE, y*SIZE, 0,0)), tiles[char])
    return m


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    m = draw_map(MAP_DATA, tile_img, tiles)
    image.save(m, 'map.png')
