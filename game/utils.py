import random
import game.constants as const
from string import ascii_uppercase, digits
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Character:
    text: str
    position: Tuple
    time_start: int
    enabled: bool = True

    def is_visible(self, tick: int) -> bool:
        return tick > self.time_start and self.enabled

    def __eq__(self, other):
        return self.time_start == other.time_start

    def __lt__(self, other):
        return self.time_start < other.time_start


def get_all_letters() -> List[str]:
    return list(ascii_uppercase + digits)


def generate_character_list(length: int) -> List[str]:
    return random.choices(get_all_letters(), k=length)


def generate_random_pos(width: int, height: int) -> Tuple:
    offset = max(width, height) / 10
    return random.randint(offset, width - offset), random.randint(offset, height - offset)


def generate_random_start_time(max_time: int) -> int:
    return random.randint(0, max_time)


def generate_character_with_random_position(character: str, start_time: int) -> Character:
    return Character(
        character,
        generate_random_pos(const.SCREEN_WIDTH, const.SCREEN_HEIGHT),
        start_time
    )


def generate_character_queue() -> List[Character]:
    interval = const.CHARACTER_APPEARING_DURATION / const.CHARACTER_QUEUE_LENGTH
    timestamps = [interval * i for i in range(1, const.CHARACTER_QUEUE_LENGTH)]
    return [generate_character_with_random_position(character, timestamp)
            for character, timestamp in zip(generate_character_list(const.CHARACTER_QUEUE_LENGTH), timestamps)]


def linear_color_transition(color_start: Tuple, color_end: Tuple, duration: int, elapsed: int):
    color_delta = [(end - start) for start, end in zip(color_start, color_end)]
    scale = elapsed / duration
    return tuple([start + (delta * scale) for start, delta in zip(color_start, color_delta)])
