import random
import src.constants as const
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
    custom_characters = '!@#$%^&*()`~_+{}:"<>?|-=[];,./\\\''
    return list(ascii_uppercase + digits)


def generate_character_queue(length: int) -> List[str]:
    return random.choices(get_all_letters(), k=length)


def generate_random_pos(width: int, height: int) -> Tuple:
    return random.randint(0, width), random.randint(0, height)


def generate_random_start_time(max_time: int) -> int:
    return random.randint(0, max_time)


def create_character(character) -> Character:
    return Character(
        character,
        generate_random_pos(const.SCREEN_WIDTH - const.FONT_SIZE, const.SCREEN_HEIGHT - const.FONT_SIZE),
        generate_random_start_time(const.CHARACTER_APPEARING_MAX_TIME)
    )


def create_character_queue() -> List[Character]:
    return [create_character(character) for character in generate_character_queue(const.CHARACTER_QUEUE_LENGTH)]
