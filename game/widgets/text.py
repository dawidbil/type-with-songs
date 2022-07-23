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
                 color=config.color_menu_font):
        super().__init__(parent_rect, padding, alignment)
        self.font = font
        self.text = text
        self.color = color
        self.calculate_rect()

    def calculate_rect(self, rect: pygame.Rect = None):
        super().calculate_rect(self.font.get_rect(self.text) if rect is None else rect)

    def render(self, surface: pygame.Surface, ticks: int):
        # surface.fill((30, 30, 70), self.parent_rect)
        # surface.fill((30, 70, 30), self.rect)
        self.font.render_to(surface, self.rect, self.text, fgcolor=self.color)
