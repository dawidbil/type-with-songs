import random
import pygame
from typing import Tuple
from functools import reduce
from pathlib import Path
from typing import Union
from string import ascii_uppercase, ascii_lowercase, digits
from enum import Flag, auto


LETTER_GROUPS = {
    "UPPERCASE": ascii_uppercase,
    "LOWERCASE": ascii_lowercase,
    "DIGITS": digits,
    "SYMBOLS": '''`-=[]\;',./!@#$%^&*()_+{}|:"<>?'''
}


class Alignment(Flag):
    top = auto()
    bottom = auto()
    left = auto()
    right = auto()


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


def generate_character_text(values: Union[str, None], groups: Union[str, None]) -> str:
    choices = values if values is not None else \
        reduce(lambda x, y: x + LETTER_GROUPS[y], groups.split('|'), '')
    return random.choices(list(choices), k=1)[0]
