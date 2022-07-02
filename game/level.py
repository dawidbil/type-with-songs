import game.utils as utils
from yaml import safe_load
from dataclasses import dataclass
from game.character import Character
from enum import IntEnum
from typing import List


class LettersColumns(IntEnum):
    timestamp = 0
    values = 1
    groups = 2


def create_character_from_letter(letter: List) -> Character:
    text = utils.generate_character_text(letter[LettersColumns.values], letter[LettersColumns.groups])
    return Character(text, None, letter[LettersColumns.timestamp])


@dataclass(frozen=True)
class Level:
    name: str
    letters: List[Character]

    @classmethod
    def load_from_yaml(cls, path: str):
        level = safe_load(open(path))
        letters = [create_character_from_letter(letter) for letter in level['letters']]
        return cls(level['name'], letters)
