import pygame
import pygame.freetype as freetype
import game.constants as const
from game.widgets.Widget import Widget
from enum import Flag, auto


class Alignment(Flag):
    top = auto()
    bottom = auto()
    left = auto()
    right = auto()


class TextWidget(Widget):
    def __init__(self,
                 font: freetype.Font,
                 text: str,
                 rect: pygame.Rect,
                 padding: pygame.Rect,
                 alignment: Alignment = None,
                 color=const.COLOR_FONT):
        self.font = font
        self.text = text
        self.color = color
        self.text_rect = None
        self.calculate_text_rect(rect, alignment, padding)

    def calculate_text_rect(self, rect: pygame.Rect, alignment: Alignment, padding: pygame.Rect):
        self.text_rect = self.font.get_rect(self.text)
        self.text_rect.center = rect.center
        if Alignment.left in alignment:
            self.text_rect.left = rect.left + padding.x
        elif Alignment.right in alignment:
            self.text_rect.right = rect.right - padding.w
        if Alignment.top in alignment:
            self.text_rect.top = rect.top + padding.y
        elif Alignment.bottom in alignment:
            self.text_rect.bottom = rect.bottom - padding.h

    def render(self, surface: pygame.Surface, ticks: int):
        self.font.render_to(surface, self.text_rect, self.text, fgcolor=self.color)
