import logging
import pygame
import pygame.freetype as freetype
import game.constants as const
import game.screens as screens
from game.utils import generate_random_pos
from game.level import Level
from game.character import Character
from game.widgets.Text import Text
from game.constants import Alignment


class StandardModeScreen(screens.Screen):
    def __init__(self, level_filename: str) -> None:
        freetype.init()
        self.font = freetype.Font(None, size=const.FONT_SIZE)
        scoreboard_bottom = const.SCOREBOARD_FONT_SIZE + const.SCOREBOARD_PADDING_TOP + const.SCOREBOARD_PADDING_BOTTOM

        self.game_rect = pygame.Rect(const.SCREEN_LEFT, scoreboard_bottom, const.SCREEN_WIDTH,
                                     const.SCREEN_HEIGHT - scoreboard_bottom)

        self.score_rect = pygame.Rect(const.SCREEN_LEFT, const.SCREEN_TOP, const.SCREEN_WIDTH, scoreboard_bottom)
        self.score_font = freetype.Font(None, size=const.SCOREBOARD_FONT_SIZE)
        self.score_text = Text(self.score_font,
                               "0/0",
                               self.score_rect,
                               pygame.Rect(const.SCOREBOARD_PADDING),
                               alignment=Alignment.left,
                               color=const.COLOR_SCORE_FONT)
        self.timer_text = Text(self.score_font,
                               "00:00",
                               self.score_rect,
                               pygame.Rect(const.SCOREBOARD_PADDING),
                               alignment=Alignment.right,
                               color=const.COLOR_SCORE_FONT)

        self.level = Level.load_from_yaml(f"levels/{level_filename}")
        self.generate_characters_positions()
        self.character_queue = self.level.letters
        self.character_queue.sort()
        self.queue_size = len(self.character_queue)
        self.score = -1
        self._is_over = False
        self.update_score()

    def update_score(self):
        self.score += 1
        self.score_text.text = f"{self.score}/{self.queue_size}"

    def update_timer(self, ticks: int):
        mins = int(ticks / 60000)
        secs = int(ticks / 1000) % 60
        self.timer_text.text = f"{mins:02d}:{secs:02d}"

    def generate_characters_positions(self):
        for letter in self.level.letters:
            text_rect = self.font.get_rect(letter.text)
            letter.position = generate_random_pos(self.game_rect, text_rect.size)

    def render_character(self, surface: pygame.Surface, character: Character):
        font_scaled = self.font.size * character.scale
        text_rect = self.font.get_rect(character.text, size=font_scaled)
        text_rect.center = character.position
        self.font.render_to(surface, text_rect, character.text, fgcolor=character.color, size=font_scaled)

    def render(self, surface: pygame.Surface, ticks: int) -> None:
        self.score_text.render(surface, ticks)
        self.timer_text.render(surface, ticks)
        for character in self.character_queue:
            if character.is_visible(ticks):
                character.update_state(ticks)
                self.render_character(surface, character)

    def handle_events(self, ticks: int) -> None:
        self.update_timer(ticks)
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_ESCAPE:
                self._is_over = True
            for character in self.character_queue:
                if event.key == pygame.key.key_code(character.text) \
                        and character.is_visible(ticks):
                    logging.debug("Hit key: %s", character.text)
                    character.time_end = ticks
                    self.update_score()
                    break

    def is_over(self, ticks: int) -> bool:
        have_characters_ended = [character.has_ended() and not character.is_fading_away(ticks)
                                 for character in self.character_queue]
        return all(have_characters_ended) or self._is_over

    def get_next_screen(self):
        return screens.MainMenuScreen()
