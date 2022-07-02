import pygame
import logging
import game.constants as const
from game.screen.StandardModeScreen import StandardModeScreen


class Game:
    def __init__(self, level_filename: str) -> None:
        pygame.init()
        pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
        self.surface = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.level_filename = level_filename
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    def run_main_loop(self):
        screen = StandardModeScreen(self.level_filename)

        is_over = False
        while not is_over:
            ticks = pygame.time.get_ticks()

            screen.handle_events(ticks)
            if len(pygame.event.get(pygame.QUIT)) != 0:
                is_over = True

            self.surface.fill(pygame.Color(const.COLOR_BACKGROUND))
            screen.render(self.surface, ticks)
            pygame.display.update()

            if screen.is_over(ticks):
                is_over = True
