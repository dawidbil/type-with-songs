import pygame
import logging
import game.constants as const
import game.screens as screens


class Game:
    def __init__(self, level_filename: str) -> None:
        pygame.init()
        pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
        self.surface = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.level_filename = level_filename
        self.screen = screens.MainMenuScreen()
        self.screen_start = pygame.time.get_ticks()
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    def run_main_loop(self):
        is_over = False
        while not is_over:
            screen_ticks = pygame.time.get_ticks() - self.screen_start

            self.screen.handle_events(screen_ticks)
            if len(pygame.event.get(pygame.QUIT)):
                is_over = True

            self.surface.fill(pygame.Color(const.COLOR_BACKGROUND))
            self.screen.render(self.surface, screen_ticks)
            pygame.display.update()

            if self.screen.is_over(screen_ticks):
                self.screen = self.screen.get_next_screen()
                self.screen_start = pygame.time.get_ticks()
                if self.screen is None:
                    is_over = True
