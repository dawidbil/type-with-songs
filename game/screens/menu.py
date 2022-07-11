import os
import pygame
import pygame.freetype as freetype
import game.utils as utils
import game.config as config
import game.screens.screen as screen
import game.screens.standard as standard
import game.screens.infinite as infinite
from game.widgets.carousel import Carousel


class MainMenu(screen.Screen):
    def __init__(self):
        self.font = freetype.Font(None, size=config.menu_font_size)
        levels = os.listdir(os.path.join(utils.get_project_base_path(), 'levels'))
        levels = [level[:level.rfind('.')] for level in levels]
        levels.append("infinite")

        self.menu_rect = pygame.Rect(config.screen_left, config.screen_top, config.screen_width, config.screen_height)
        self.carousel = Carousel(levels,
                                 self.font,
                                 self.menu_rect,
                                 pygame.Rect((10, 10, 10, 10)))

        self._is_over = False
        self.next_screen = None

    def render(self, surface: pygame.Surface, ticks: int):
        self.carousel.render(surface, ticks)

    def handle_events(self, ticks: int) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.carousel.previous()
                elif event.key == pygame.K_DOWN:
                    self.carousel.next()
                elif event.key == pygame.K_RETURN:
                    text_widget = self.carousel.value
                    self.next_screen = infinite.InfiniteMode() if text_widget.text == "infinite" else \
                        standard.StandardMode(f"{text_widget.text}.yaml")
                    self._is_over = True
                elif event.key == pygame.K_ESCAPE:
                    self._is_over = True

    def is_over(self, ticks: int) -> bool:
        return self._is_over

    def get_next_screen(self):
        return self.next_screen
