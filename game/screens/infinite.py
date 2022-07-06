import math
import game.constants as const
import game.screens.mode as mode
from game.character import Character
from game.utils import generate_character_text, generate_random_pos
from logging import getLogger


class InfiniteMode(mode.ModeBase):
    def __init__(self) -> None:
        super().__init__()
        self.interval = const.INFINITE_MODE_START_INTERVAL
        self.time_since_last_spawn = 0
        self.update_score()

    def update_score(self):
        super().update_score()
        self.score_text.text = f"{self.score}/?"

    def update_interval(self, ticks: int) -> None:
        interval = const.INFINITE_MODE_START_INTERVAL - (ticks * const.INFINITE_MODE_INTERVAL_DROP_SPEED) / math.log10(ticks)
        self.interval = max(interval, const.INFINITE_MODE_MIN_INTERVAL)
        getLogger(__name__).debug(f"Interval: {self.interval}")

    def update_spawn_time(self, ticks: int) -> None:
        if ticks - self.time_since_last_spawn > self.interval:
            self.spawn_character(ticks)
            self.time_since_last_spawn = ticks
            self.update_interval(ticks)

    def spawn_character(self, ticks: int) -> None:
        text = generate_character_text(None, "UPPERCASE|LOWERCASE|DIGITS|SYMBOLS")
        text_rect = self.font.get_rect(text)
        position = generate_random_pos(self.game_rect, text_rect.size)
        self.character_queue.append(Character(text, position, ticks))

    def handle_events(self, ticks: int) -> None:
        super().handle_events(ticks)
        self.update_spawn_time(ticks)

    def is_over(self, ticks: int) -> bool:
        have_characters_decayed = [character.is_decayed(ticks) for character in self.character_queue]
        return any(have_characters_decayed) or self._is_over
