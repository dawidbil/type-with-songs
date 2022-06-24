import random
import game.constants as const
from game.constants import LettersColumns
from game.character import Character
from string import ascii_uppercase, digits
from typing import List, Tuple
from functools import reduce


def get_all_letters() -> List[str]:
    return list(ascii_uppercase + digits)


def generate_character_list(length: int) -> List[str]:
    return random.choices(get_all_letters(), k=length)


def generate_random_pos(width: int, height: int) -> Tuple:
    offset_x = width / 10
    offset_y = height / 10
    return random.randint(offset_x, width - offset_x), random.randint(offset_y, height - offset_y)


def generate_random_start_time(max_time: int) -> int:
    return random.randint(0, max_time)


def generate_character_with_random_position(character: str, start_time: int) -> Character:
    return Character(
        character,
        generate_random_pos(const.SCREEN_WIDTH, const.SCREEN_HEIGHT),
        start_time
    )


def generate_character_queue() -> List[Character]:
    interval = const.CHARACTERS_APPEARING_DURATION / const.CHARACTERS_QUEUE_LENGTH
    timestamps = [interval * i for i in range(1, const.CHARACTERS_QUEUE_LENGTH)]
    return [generate_character_with_random_position(character, timestamp)
            for character, timestamp in zip(generate_character_list(const.CHARACTERS_QUEUE_LENGTH), timestamps)]


def linear_transition(start: int, end: int, duration: int, elapsed: int) -> int:
    delta = end - start
    scale = elapsed / duration
    return int(start + (delta * scale))


def linear_color_transition(color_start: Tuple, color_end: Tuple, duration: int, elapsed: int):
    return tuple([linear_transition(component_start, component_end, duration, elapsed)
                  for component_start, component_end in zip(color_start, color_end)])


def create_character_from_letter(letter: List) -> Character:
    text = get_letter_from_groups(letter[LettersColumns.values], letter[LettersColumns.groups])
    pos = generate_random_pos(const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
    return Character(text, pos, letter[LettersColumns.timestamp])


def get_letter_from_groups(values: str, groups: str) -> str:
    if values != '':
        return random.choices(list(values), k=1)[0]
    else:
        # sorry
        letters = reduce(lambda x, y: const.LETTER_GROUPS[x] + const.LETTER_GROUPS[y], groups.split('|'))
        return random.choices(list(letters), k=1)[0]

