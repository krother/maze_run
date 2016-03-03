
from pygame import image, Rect, Surface
from load_tiles import load_tiles, get_tile_rect, SIZE

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
    print("Hello, I'm here")
    from pprint import pprint
    pprint(data)
    xs = len(data[0]) * SIZE
    ys = len(data) * SIZE
    map_img = Surface((xs, ys))
    for x, row in enumerate(data):
        print("A" * 40)
        for y, char in enumerate(row):
            print(x, y, char)
            rect = get_tile_rect(x, y)
            #rect = Rect((x*SIZE, y*SIZE, x*SIZE + SIZE, y+SIZE + SIZE))
            print(tiles[char], rect)
            map_img.blit(img, tiles[char], rect)
            #map_img.blit(img, rect, tiles[char])
            #map_img.blit(img, Rect((0, 64, 32, 96)),Rect((5, 3, 0, 0)))
            #map_img.blit(img, Rect((0, 0, 32, 32)),Rect((0, 0, 32, 32))) 
    return map_img


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    m = draw_map(level, tile_img, tiles)
    image.save(m, 'map.png')
