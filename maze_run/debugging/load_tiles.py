
from pygame import image, Rect, Surface

tile_image = image.load('tiles.xpm')

tiles = {
    '#': Rect(0, 0, 32, 32),
    ' ': Rect(0, 32, 32, 64),
    '*': Rect(0, 96, 32, 128),
    }

m = Surface((96, 32))
m.blit(tile_image, Rect((0, 0, 0, 0)), tiles['#'])
m.blit(tile_image, Rect((32, 0, 0, 0)), tiles[' '])
m.blit(tile_image, Rect((64, 0, 0, 0)), tiles['*'])
image.save(m, 'tile_combo.png')

