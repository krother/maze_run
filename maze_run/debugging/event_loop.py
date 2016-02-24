
from pygame.locals import KEYDOWN
from pygame.event import Event
import pygame


def event_loop(handle_key, delay=10):
    """Processes events and updates callbacks."""
    while True:
        pygame.event.pump()
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            handle_key(event.key)
        pygame.time.delay(delay)

def print_key(key):
    print(key)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((60, 40))
    event_loop(print_key)

