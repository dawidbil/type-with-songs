import pygame
import logging
import pygame.font as font
import game.constants as const
import game.utils as utils
from game.character import Character
from game.level import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.font = font.Font(None, const.FONT_SIZE)

        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    def render_character(self, character: Character):
        text_surface = self.font.render(character.text, True, character.color)
        text_surface = pygame.transform.scale(
            text_surface,
            (text_surface.get_width() * character.scale, text_surface.get_height() * character.scale)
        )
        text_rect = text_surface.get_rect(center=character.position)
        self.screen.blit(text_surface, text_rect)

    def run_main_loop(self):
        level = Level.load_from_yaml("levels/first.yaml")
        character_queue = level.letters
        # character_queue = utils.generate_character_queue()
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
                        try:
                            if event.key == pygame.key.key_code(character.text)\
                               and character.is_visible(ticks):
                                logging.debug("Hit key: %s", character.text)
                                character.time_end = ticks
                                break
                        except ValueError as exception:
                            print(exception)
                            print(character)

            self.screen.fill(pygame.Color(const.COLOR_BACKGROUND))
            for character in character_queue:
                if character.is_visible(ticks):
                    character.update_state(ticks)
                    self.render_character(character)
            pygame.display.update()

            if all([character.has_ended() and not character.is_fading_away(ticks) for character in character_queue]):
                is_over = True
