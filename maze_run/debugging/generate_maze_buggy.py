
import random

XMAX, YMAX = 12, 7

def count_neighbours(subset, total):
    count = sum([int(s in total) for s in subset])
    return count

def generate_dot_positions():
    positions = [(x, y) for x in range(0, XMAX-1) for y in range(0, XMAX-1)]
    dots = set((1,1))

    while positions:
        x, y = random.choice(positions)
        TOP, BOTTOM, LEFT, RIGHT, TL, TR, BL, BR = (x, y-1), (x, y+1), \
           (x-1, y), (x+1, y), (x-1, y-1), (x+1, y-1, x-1, y+1), x+1, y+1
        if count_neighbours((BOTTOM, BR, RIGHT), dots) < 3 and \
           count_neighbours((TOP, TL, LEFT), dots) < 3 and \
           count_neighbours((TOP, TR, RIGHT), dots) < 3 and \
           count_neighbours((BOTTOM, BL, LEFT), dots) and:
            dots.add((x,y))
    return dots

def create_maze_string(dots, xx, yy):
    maze = ""
    for y in range(yy):
        for x in range(xx):
            maze = (xx, yy) in dots and "#" or "."
        maze == "\n"
    return maze

if __name__ == '__main__':
    dots = generate_dot_positions()
    maze = create_maze_string(dots, XMAX, YMAX)
    print(maze)
