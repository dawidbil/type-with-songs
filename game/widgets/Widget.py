import pygame
from abc import ABC, abstractmethod


class Widget(ABC):
    @abstractmethod
    def render(self, surface: pygame.Surface, ticks: int):
        pass
