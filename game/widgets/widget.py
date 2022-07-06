import pygame
from abc import ABC, abstractmethod
from game.constants import Alignment


class Widget(ABC):
    @abstractmethod
    def __init__(self,
                 parent_rect:
                 pygame.Rect,
                 padding: pygame.Rect = pygame.Rect(0, 0, 0, 0),
                 alignment: Alignment = None):
        self.parent_rect = parent_rect
        self.padding = padding
        self.alignment = alignment
        self.rect = None

    @abstractmethod
    def render(self, surface: pygame.Surface, ticks: int):
        pass

    def resize_to_parent(self, rect: pygame.Rect):
        max_width = self.parent_rect.width - (self.padding.x + self.padding.w)
        if rect.width > max_width:
            rect.width = max_width
        max_height = self.parent_rect.height - (self.padding.y + self.padding.h)
        if rect.height > max_height:
            rect.height = max_height

    def calculate_rect(self, rect: pygame.Rect):
        self.resize_to_parent(rect)
        rect.center = self.parent_rect.center
        if self.alignment is not None:
            if Alignment.left in self.alignment:
                rect.left = self.parent_rect.left + self.padding.x
            elif Alignment.right in self.alignment:
                rect.right = self.parent_rect.right - self.padding.w
            if Alignment.top in self.alignment:
                rect.top = self.parent_rect.top + self.padding.y
            elif Alignment.bottom in self.alignment:
                rect.bottom = self.parent_rect.bottom - self.padding.h
        self.rect = rect
