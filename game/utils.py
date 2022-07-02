import os
import random
import pygame
import game.constants as const
from typing import Tuple
from functools import reduce
from pathlib import Path


def get_project_base_path() -> str:
    return Path(__file__).parent.parent


def generate_random_pos(rect: pygame.Rect, size: Tuple) -> Tuple:
    return random.randint(rect.left + size[0], rect.right - size[0]),\
           random.randint(rect.top + size[1], rect.bottom - size[1])


def linear_transition(start: int, end: int, duration: int, elapsed: int) -> int:
    delta = end - start
    scale = elapsed / duration
    return int(start + (delta * scale))


def linear_color_transition(color_start: Tuple, color_end: Tuple, duration: int, elapsed: int):
    return tuple([linear_transition(component_start, component_end, duration, elapsed)
                  for component_start, component_end in zip(color_start, color_end)])


def generate_character_text(values: str, groups: str) -> str:
    choices = values if values is not None else \
        reduce(lambda x, y: x + const.LETTER_GROUPS[y], groups.split('|'), '')
    return random.choices(list(choices), k=1)[0]
