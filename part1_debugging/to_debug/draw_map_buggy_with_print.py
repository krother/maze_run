
from pygame import image, Rect, Surface
from load_tiles import load_tiles, get_tile_rect, SIZE
from generate_maze import create_maze

def parse_map(data):
    return data.strip().split('\n')

level = create_maze(12, 7)
level = parse_map(level)
#level = ['#']
#level = ['##']

def draw_map(data, img, tiles):
    """Returns an image of a tile-based map"""
    xs = len(data[0]) * SIZE
    ys = len(data) * SIZE
    map_img = Surface((xs, ys))
    print("xs={} \t ys={}".format(xs, ys))
    #print(data)
    #from pprint import pprint
    #pprint(data)
    #pprint(data, depth=1, width=50)
    for y, row in enumerate(data):
        #print("I'm stuck in Folsom prison.")
        for x, char in enumerate(row):
            #rect = get_tile_rect(xs, ys)
            rect = get_tile_rect(x, y)
            print(tiles[char], rect)
            #map_img.blit(img, tiles[char], rect)
            #print("x={} \t y={} \t {}".format(x,y,char))
            #map_img.blit(img, tiles[char], get_tile_rect(x, y))
            map_img.blit(img, rect, tiles[char])
        #return map_img
    return map_img


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    m = draw_map(level, tile_img, tiles)
    image.save(m, 'maze.png')
