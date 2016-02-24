
from pygame import image, Rect, Surface

SIZE = 32

tile_image = image.load('tiles.xpm')

tiles = {
    '#': Rect(0, 0, 32, 32),
    ' ': Rect(0, 32, 32, 64),
    '*': Rect(0, 96, 32, 128),
    }

mapdata = """
#######
#     #
#     #
# *   #
#     #
#     #
#######""".strip().split('\n')

def draw_map(data, tiles, img):
    xs = len(data[0]) * SIZE
    ys = len(data) * SIZE
    m = Surface((xs, ys))
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            m.blit(img, Rect((x*SIZE, y*SIZE, 0,0)), tiles[char])
    return m

m = draw_map(mapdata, tiles, tile_image)
image.save(m, 'map.png')
