import pygame
import logging
import pygame.font as font
import game.constants as const
import game.utils as utils


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.font = font.Font(None, const.FONT_SIZE)

        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    def render_text(self, text: str, time_alive: int) -> pygame.Surface:
        font_color = utils.linear_color_transition(
            const.COLOR_FONT,
            const.COLOR_FONT_WAITING,
            const.CHARACTER_DECAYING_TIME,
            min(max(0, time_alive - const.CHARACTER_SCALING_TIME), const.CHARACTER_DECAYING_TIME)
        )
        return self.font.render(text, True, font_color)

    def render_scaled_text(self, text: str, time_alive: int):
        surface = self.render_text(text, time_alive)
        # scale is value from 0 to 1
        # its value is raising along with time_alive until it reaches const value - then min function stops it
        scale = min(time_alive, const.CHARACTER_SCALING_TIME) / const.CHARACTER_SCALING_TIME
        scaled_x = surface.get_width() * scale
        scaled_y = surface.get_height() * scale
        return pygame.transform.scale(surface, (scaled_x, scaled_y))

    def run_main_loop(self):
        character_queue = utils.generate_character_queue()
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

            self.screen.fill(pygame.Color(const.COLOR_BACKGROUND))
            for character in character_queue:
                if character.is_visible(ticks):
                    text_surface = self.render_scaled_text(character.text, ticks - character.time_start)
                    text_rect = text_surface.get_rect(center=character.position)
                    self.screen.blit(text_surface, text_rect)
            pygame.display.update()

            if not any([character.enabled for character in character_queue]):
                is_over = True
