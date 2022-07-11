import pygame
import pygame.freetype as freetype
import game.config as config
import game.widgets.widget as widget
from game.utils import Alignment


class Text(widget.Widget):
    def __init__(self,
                 font: freetype.Font,
                 text: str,
                 parent_rect: pygame.Rect,
                 padding: pygame.Rect = pygame.Rect(0, 0, 0, 0),
                 alignment: Alignment = None,
                 color=config.color_font):
        super().__init__(parent_rect, padding, alignment)
        self.font = font
        self.text = text
        self.color = color
        self.calculate_rect()

    def calculate_rect(self, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)):
        super().calculate_rect(self.font.get_rect(self.text))

    def render(self, surface: pygame.Surface, ticks: int):
        self.font.render_to(surface, self.rect, self.text, fgcolor=self.color)
