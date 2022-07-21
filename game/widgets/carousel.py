import pygame
import pygame.freetype as freetype
import game.config as config
import game.widgets.widget as widget
import game.widgets.text as text
from functools import reduce
from copy import copy
from typing import List
from game.utils import Alignment


class CarouselList:
    class Node:
        def __init__(self, value, previous=None, next=None):
            self.value = value
            self.previous = previous
            self.next = next

    def __init__(self, values: List):
        if not len(values):
            raise ValueError("List cannot be empty.")
        head = CarouselList.Node(values[0])
        tail = head
        for value in values[1:]:
            tail.next = CarouselList.Node(value, previous=tail)
            tail = tail.next
        tail.next = head
        head.previous = tail
        self.current = head

    @property
    def next(self):
        return self.current.next

    @property
    def previous(self):
        return self.current.previous

    @property
    def value(self):
        return self.current.value


class Carousel(widget.Widget):
    def __init__(self,
                 items: List,
                 font: freetype.Font,
                 parent_rect: pygame.Rect,
                 padding: pygame.Rect = pygame.Rect(0, 0, 0, 0),
                 alignment: Alignment = None):
        super().__init__(parent_rect, padding, alignment)
        self.font = font
        self.calculate_rect()

        texts = [text.Text(
            freetype.Font(None, font.size),
            item,
            self.rect,
            padding=pygame.Rect(0, 0, 0, 0),
            alignment=Alignment.left
        ) for item in items]
        self._carousel_list = CarouselList(texts)

    # https://imgur.com/a/C2YBfzZ
    # index<=>offset, offset<=>max_offset xd
    def render(self, surface: pygame.Surface, ticks: int):
        # surface.fill((70, 30, 30), self.rect)
        max_offset = config.menu_carousel_size // 2
        for i in range(config.menu_carousel_size):
            offset = i - max_offset
            scale = self._get_scale_by_index(offset)
            rect = pygame.Rect(0, 0, self.rect.width, config.menu_font_size)
            rect.center = self.parent_rect.center
            rect.y -= config.menu_font_size * offset
            text_widget = self._get_value_by_offset(offset).value
            text_widget.parent_rect = rect
            text_widget.font.size = scale * config.menu_font_size
            text_widget.calculate_rect()
            text_widget.render(surface, ticks)

    @staticmethod
    def _get_scale_by_index(index):
        return 1 / (abs(index) + 1)

    def _get_value_by_offset(self, offset):
        node = self._carousel_list.current
        for i in range(abs(offset)):
            if offset < 0:
                node = node.previous
            else:
                node = node.next
        return node

    def next(self):
        self._carousel_list.current = self._carousel_list.next

    def previous(self):
        self._carousel_list.current = self._carousel_list.previous

    @property
    def value(self):
        return self._carousel_list.value
