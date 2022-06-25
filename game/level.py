import game.utils as utils
from yaml import safe_load
from dataclasses import dataclass
from game.character import Character
from typing import List


@dataclass(frozen=True)
class Level:
    name: str
    letters: List[Character]

    @classmethod
    def load_from_yaml(cls, path: str):
        level = safe_load(open(path))
        letters = [utils.create_character_from_letter(letter) for letter in level['letters']]
        return cls(level['name'], letters)
