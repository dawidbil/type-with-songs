import pygame
import logging
import pygame.font as font
import src.constants as const
import src.utils as utils


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.font = font.Font(None, const.FONT_SIZE)

        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    def render_text(self, text: str) -> pygame.Surface:
        return self.font.render(text, True, pygame.Color(const.COLOR_ALMOST_WHITE))

    def render_scaled_text(self, text: str, time_alive: int):
        surface = self.render_text(text)
        scale = min(time_alive, const.CHARACTER_SCALING_TIME) / const.CHARACTER_SCALING_TIME
        scaled_x = surface.get_width() * scale
        scaled_y = surface.get_height() * scale
        return pygame.transform.scale(surface, (scaled_x, scaled_y))

    def run_main_loop(self):
        character_queue = utils.create_character_queue()
        character_queue.sort()
        logging.debug("Character queue: %s", character_queue)

        is_over = False
        while not is_over:
            ticks = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_over = not is_over
                elif event.type == pygame.KEYDOWN:
                    for character in character_queue:
                        if event.key == pygame.key.key_code(character.text)\
                           and character.is_visible(ticks):
                            logging.debug("Hit key: %s", character.text)
                            character.enabled = False
                            break

            self.screen.fill(pygame.Color(const.COLOR_DARK_GREY))
            for character in character_queue:
                if character.is_visible(ticks):
                    text_surface = self.render_scaled_text(character.text, ticks - character.time_start)
                    text_rect = text_surface.get_rect(center=character.position)
                    self.screen.blit(text_surface, text_rect)
            pygame.display.update()
