import pygame
from game.screens import InfiniteMode


def min_to_ms(min):
    return min * 60000


def print_and_update(mode, min):
    mode.update_interval(min_to_ms(min))
    print(mode.interval)


if __name__ == "__main__":
    pygame.init()
    pygame.freetype.init()
    mode = InfiniteMode()
    for i in range(1, 13):
        print_and_update(mode, i)
