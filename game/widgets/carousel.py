import pygame
import pygame.freetype as freetype
import game.config as config
import game.widgets.widget as widget
import game.widgets.text as text
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
        rect = copy(parent_rect)
        rect.height = config.menu_carousel_size * self.font.size
        self.calculate_rect(rect)

        texts = [text.Text(
            freetype.Font(None, font.size),
            item,
            self.rect,
            pygame.Rect(0, 0, 0, 0),
        ) for item in items]
        self._carousel_list = CarouselList(texts)

    def render(self, surface: pygame.Surface, ticks: int):
        offset = config.menu_carousel_size // 2
        for i in range(config.menu_carousel_size):
            index = i - offset
            text_widget = self._get_value_by_offset(index).value
            text_widget.font.size = (1 / (abs(index) + 1)) * config.menu_font_size
            text_widget.parent_rect = self._get_rect_by_index(i)
            text_widget.calculate_rect()
            text_widget.render(surface, ticks)

    def _get_rect_by_index(self, index):
        y = self.rect.top
        y += index * self.font.size
        return pygame.Rect(self.rect.x, y, self.rect.width, self.font.size)

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
