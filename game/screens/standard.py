import game.screens.mode as mode
from game.utils import generate_random_pos
from game.level import Level


class StandardMode(mode.ModeBase):
    def __init__(self, level_filename: str) -> None:
        super().__init__()
        self.level = Level.load_from_yaml(f"levels/{level_filename}")
        self.generate_characters_positions()
        self.character_queue = self.level.letters
        self.character_queue.sort()
        self.queue_size = len(self.character_queue)
        self.update_score()

    def update_score(self):
        super().update_score()
        self.score_text.text = f"{self.score}/{self.queue_size}"

    def generate_characters_positions(self):
        for letter in self.level.letters:
            text_rect = self.font.get_rect(letter.text)
            letter.position = generate_random_pos(self.game_rect, text_rect.size)
