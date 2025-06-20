import pygame
from core.character.character import Character
from core.const import WINDOW_HEIGHT, WINDOW_WIDTH



class HealthBar:
    def __init__(self, pos: str, character: Character):
        self.__radius = 4
        self.__pos = pos  # 'topleft', 'topcenter', etc.
        self.__character = character

    def draw(self, screen: pygame.Surface):
        # Dynamic size: 40% of screen width, 5% of screen height
        bar_width = int(WINDOW_WIDTH * 0.4)
        bar_height = int(WINDOW_HEIGHT * 0.05)

        # Calculate current health percentage
        ratio = self.__character.get_hp() / self.__character.get_max_hp()
        current_width = int(bar_width * ratio)

        # Determine position
        if self.__pos == 'topleft':
            x = 10
            y = 10
            fill_x = x
        elif self.__pos == 'topcenter':
            x = (WINDOW_WIDTH - bar_width) // 2
            y = 10
            fill_x = x
        elif self.__pos == 'topright':
            x = WINDOW_WIDTH - bar_width - 10
            y = 10
            fill_x = x + (bar_width - current_width)
        else:
            x, y = 10, 10
            fill_x = x


        # Draw backgrounds bar
        pygame.draw.rect(screen, (80, 0, 0), (x, y, bar_width, bar_height), 0, self.__radius)
        # Draw health fill
        pygame.draw.rect(screen, (0, 255, 0), (fill_x, y, current_width, bar_height),0, self.__radius if ratio == 1 else 0)

        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2, self.__radius)