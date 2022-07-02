import pygame
import pygame.freetype as freetype
import game.constants as const
import game.widgets as widgets
from game.constants import Alignment


class Text(widgets.Widget):
    def __init__(self,
                 font: freetype.Font,
                 text: str,
                 parent_rect: pygame.Rect,
                 padding: pygame.Rect = pygame.Rect(0, 0, 0, 0),
                 alignment: Alignment = None,
                 color=const.COLOR_FONT):
        super().__init__(parent_rect, padding, alignment)
        self.font = font
        self.text = text
        self.color = color
        self.calculate_rect()

    def calculate_rect(self, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)):
        super().calculate_rect(self.font.get_rect(self.text))

    def render(self, surface: pygame.Surface, ticks: int):
        self.font.render_to(surface, self.rect, self.text, fgcolor=self.color)
