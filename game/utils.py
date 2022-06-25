import random
import game.constants as const
from game.constants import LettersColumns
from game.character import Character
from typing import List, Tuple
from functools import reduce


def generate_random_pos(width: int, height: int) -> Tuple:
    offset_x = width / 10
    offset_y = height / 10
    return random.randint(offset_x, width - offset_x), random.randint(offset_y, height - offset_y)


def linear_transition(start: int, end: int, duration: int, elapsed: int) -> int:
    delta = end - start
    scale = elapsed / duration
    return int(start + (delta * scale))


def linear_color_transition(color_start: Tuple, color_end: Tuple, duration: int, elapsed: int):
    return tuple([linear_transition(component_start, component_end, duration, elapsed)
                  for component_start, component_end in zip(color_start, color_end)])


def create_character_from_letter(letter: List) -> Character:
    text = generate_character_text(letter[LettersColumns.values], letter[LettersColumns.groups])
    pos = generate_random_pos(const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
    return Character(text, pos, letter[LettersColumns.timestamp])


def generate_character_text(values: str, groups: str) -> str:
    choices = values if values is not None else \
        reduce(lambda x, y: const.LETTER_GROUPS[x] + const.LETTER_GROUPS[y], groups.split('|'), '')
    print(const.LETTER_GROUPS[groups.split('|')[0]])
    return random.choices(list(choices), k=1)[0]
