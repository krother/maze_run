
from pygame import image, Rect

bg = image.load('bg.xpm')
ex = image.load('explo.xpm')

bg.blit(ex, Rect((15, 15, 0, 0)), Rect((0, 0, 32, 32)))

image.save(bg, 'merged.png')
