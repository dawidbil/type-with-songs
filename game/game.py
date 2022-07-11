import pygame
import pygame.freetype as freetype
import logging
import game.config as config
from game.screens.menu import MainMenu


class Game:
    def __init__(self) -> None:
        pygame.init()
        freetype.init()
        pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
        self.surface = pygame.display.set_mode((config.screen_width, config.screen_height))
        self.screen = MainMenu()
        self.screen_timer = pygame.time.get_ticks()
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    def run_main_loop(self):
        is_over = False
        while not is_over:
            screen_duration = pygame.time.get_ticks() - self.screen_timer

            self.screen.handle_events(screen_duration)
            if len(pygame.event.get(pygame.QUIT)):
                is_over = True

            self.surface.fill(pygame.Color(config.color_background))
            self.screen.render(self.surface, screen_duration)
            pygame.display.update()

            if self.screen.is_over(screen_duration):
                self.screen = self.screen.get_next_screen()
                self.screen_timer = pygame.time.get_ticks()
                if self.screen is None:
                    is_over = True
