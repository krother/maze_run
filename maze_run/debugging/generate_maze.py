
import random

XMAX, YMAX = 11, 6


def pick_random_position(positions):
    pos = random.choice(positions)
    positions.remove(pos)
    return pos

def count_neighbours(subset, total):
    count = sum([int(s in total) for s in subset])
    return count

def generate_dot_positions(xsize, ysize):
    positions = [(x,y) for x in range(1, xsize-1) for y in range(1, ysize-1)]
    dots = set()

    while positions:
        x, y = pick_random_position(positions)
        TOP, BOTTOM, LEFT, RIGHT = (x, y-1), (x, y+1), (x-1, y), (x+1, y)
        TL, TR, BL, BR = (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)
        if count_neighbours((BOTTOM, BR, RIGHT), dots) < 3 and \
           count_neighbours((TOP, TL, LEFT), dots) < 3 and \
           count_neighbours((TOP, TR, RIGHT), dots) < 3 and \
           count_neighbours((BOTTOM, BL, LEFT), dots) < 3:
            dots.add((x,y))
    return dots

def create_maze_string(dots, xsize, ysize):
    maze = ""
    for y in range(ysize):
        for x in range(xsize):
            maze += (x, y) in dots and "." or "#"
        maze += "\n"
    return maze

def create_maze(xsize, ysize):
    dots = generate_dot_positions(xsize, ysize)
    maze = create_maze_string(dots, xsize, ysize)
    return maze

if __name__ == '__main__':
    print(create_maze(XMAX, YMAX))
