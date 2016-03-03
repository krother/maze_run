
import random

def count_neighbours(subset, total):
    count = sum([int(s in total) for s in subset])
    return count

def pick_random_position(positions):
    pos = random.choice(positions)
    positions.remove(pos)
    return pos

XMAX, YMAX = 10, 5
positions = [(x,y) for x in range(1, XMAX) for y in range(1, YMAX)]
dots = set((pick_random_position(positions)))

while positions:
    x, y = pick_random_position(positions)
    TOP, BOTTOM, LEFT, RIGHT = ((x, y-1), (x, y+1), (x-1, y), (x+1, y))
    TL, TR, BL, BR = ((x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1))
    if count_neighbours((BOTTOM, BR, RIGHT), dots) < 3 and \
       count_neighbours((TOP, TL, LEFT), dots) < 3 and \
       count_neighbours((TOP, TR, RIGHT), dots) < 3 and \
       count_neighbours((BOTTOM, BL, LEFT), dots) < 3:
        dots.add((x,y))

maze = ""
for y in range(YMAX+1):
    for x in range(XMAX+1):
        maze += (x,y) in dots and "." or "#"
    maze += "\n"
print(maze)
