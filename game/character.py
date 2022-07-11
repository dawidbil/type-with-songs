import game.utils as utils
import game.config as config
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Character:
    text: str
    position: Tuple
    time_start: int
    time_end: int = -1
    scale: float = 0.
    color: Tuple = tuple(config.color_font)

    def update_state(self, tick: int) -> None:
        self.__update_color(tick)
        self.__update_scale(tick)

    def __update_color(self, tick: int) -> None:
        time_alive = tick - self.time_start
        color = utils.linear_color_transition(
            config.color_font,
            config.color_font_decaying,
            config.character_decaying_duration,
            min(max(0, time_alive - config.character_fading_in_duration), config.character_decaying_duration)
        )
        alpha = 255 if not self.has_ended() else \
            utils.linear_transition(255, 0, config.character_fading_out_duration, tick - self.time_end)
        self.color = color + (alpha, )

    def __update_scale(self, tick: int) -> None:
        time_alive = tick - self.time_start
        self.scale = min(time_alive, config.character_fading_in_duration) / config.character_fading_in_duration
        if self.has_ended():
            fading_away_scale = min(tick - self.time_end, config.character_fading_out_duration) \
                / config.character_fading_out_duration
            self.scale += (config.character_fading_out_scale - self.scale) * fading_away_scale

    def has_started(self, tick: int) -> bool:
        return tick > self.time_start

    def has_ended(self) -> bool:
        return self.time_end != -1

    def is_fading_away(self, tick: int) -> bool:
        return self.has_ended() and tick - self.time_end < config.character_fading_out_duration

    def is_decayed(self, tick: int) -> bool:
        return not self.has_ended() and \
               tick - self.time_start > config.character_decaying_duration + config.character_fading_in_duration

    def is_visible(self, tick: int) -> bool:
        return (self.has_started(tick) and not self.has_ended()) or self.is_fading_away(tick)

    def __eq__(self, other):
        return self.time_start == other.time_start

    def __lt__(self, other):
        return self.time_start < other.time_start
