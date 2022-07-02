import os
import pygame
import pygame.freetype as freetype
import game.screens as screens
import game.widgets as widgets
import game.utils as utils
import game.constants as const


class MainMenuScreen(screens.Screen):
    def __init__(self):
        self.font = freetype.Font(None, size=const.MENU_FONT_SIZE)
        levels = os.listdir(os.path.join(utils.get_project_base_path(), 'levels'))
        levels = [level[:level.rfind('.')] for level in levels]

        self.menu_rect = pygame.Rect(const.SCREEN_LEFT, const.SCREEN_TOP, const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        self.carousel = widgets.Carousel(levels,
                                         self.font,
                                         self.menu_rect,
                                         pygame.Rect((10, 10, 10, 10)),
                                         const.Alignment.bottom)

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
                    self.next_screen = screens.StandardModeScreen(f"{text_widget.text}.yaml")
                    self._is_over = True
                elif event.key == pygame.K_ESCAPE:
                    self._is_over = True

    def is_over(self, ticks: int) -> bool:
        return self._is_over

    def get_next_screen(self):
        return self.next_screen
