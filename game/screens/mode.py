import os.path
import logging
import pygame
import pygame.freetype as freetype
import game.config as config
import game.screens.screen as screen
import game.screens.menu as menu
from game.widgets.text import Text
from game.utils import get_project_base_path, Alignment
from game.character import Character


class ModeBase(screen.Screen):
    def __init__(self):
        self.font = freetype.Font(os.path.join(get_project_base_path(), "PTSerif-Regular.ttf"), size=config.font_size)
        scoreboard_bottom = config.scoreboard_font_size + config.scoreboard_padding[1] + config.scoreboard_padding[3]

        self.game_rect = pygame.Rect(config.screen_left, scoreboard_bottom, config.screen_width,
                                     config.screen_height - scoreboard_bottom)

        self.score_rect = pygame.Rect(config.screen_left, config.screen_top, config.screen_width, scoreboard_bottom)
        self.score_font = freetype.Font(None, size=config.scoreboard_font_size)
        self.score_text = Text(self.score_font,
                               "0/0",
                               self.score_rect,
                               pygame.Rect(config.scoreboard_padding),
                               alignment=Alignment.left,
                               color=config.color_score_font)
        self.timer_text = Text(self.score_font,
                               "00:00",
                               self.score_rect,
                               pygame.Rect(config.scoreboard_padding),
                               alignment=Alignment.right,
                               color=config.color_score_font)
        self.character_queue = []
        self.score = -1
        self._is_over = False

    def update_score(self):
        self.score += 1

    def update_timer(self, ticks: int):
        mins = int(ticks / 60000)
        secs = int(ticks / 1000) % 60
        self.timer_text.text = f"{mins:02d}:{secs:02d}"

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
        for event in pygame.event.get(pygame.TEXTINPUT):
            for character in self.character_queue:
                if event.text == character.text and character.is_visible(ticks):
                    logging.debug("Hit key: %s", character.text)
                    character.time_end = ticks
                    self.update_score()
                    break

    def is_over(self, ticks: int) -> bool:
        have_characters_ended = [character.has_ended() and not character.is_fading_away(ticks)
                                 for character in self.character_queue]
        return all(have_characters_ended) or self._is_over

    def get_next_screen(self):
        return menu.MainMenu()
