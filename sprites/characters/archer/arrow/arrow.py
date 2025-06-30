
import pygame

from core.const import Colors, WINDOW_WIDTH


class Arrow:
    def __init__(self, x, y, is_flipped: bool, speed: int = 800):
        self.__rect = pygame.Rect(x, y, 160, 30)
        self.__is_flipped = is_flipped
        self.__image = pygame.image.load('assets/images/characters/archer/Sprites/Arrow.png').convert_alpha()
        self.__image = pygame.transform.scale2x(self.__image)
        if is_flipped:
            self.__image = pygame.transform.flip(self.__image, True, False)
        self.__speed = speed

    def get_rect(self):
        return self.__rect

    def update(self, delta_time) -> bool:
        dx = (-1 if self.__is_flipped else 1) * self.__speed * delta_time
        self.__rect.x += dx

        if self.__rect.x <= 0 or self.__rect.x >= WINDOW_WIDTH:
            return False

        return True

    def draw(self, screen, debug=False):
        if debug:
            pygame.draw.rect(screen, Colors.RED.value, self.__rect)
        screen.blit(self.__image, (self.__rect.x, self.__rect.centery - self.__image.get_height() / 2))