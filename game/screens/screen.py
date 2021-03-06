import pygame
from abc import ABC, abstractmethod


class Screen(ABC):
    @abstractmethod
    def render(self, surface: pygame.Surface, ticks: int) -> None:
        pass

    @abstractmethod
    def handle_events(self, ticks: int) -> None:
        pass

    @abstractmethod
    def is_over(self, ticks: int) -> bool:
        pass

    @abstractmethod
    def get_next_screen(self):
        pass
