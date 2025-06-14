
import pygame

from core.const import Colors

class Arrow:
    def __init__(self, x, y, is_flipped: bool, speed: int = 800, damage: float = 10.0):
        self.__damage = damage
        self.__rect = pygame.Rect(x, y, 160, 30)
        self.__is_flipped = is_flipped
        self.__image = pygame.image.load('assets/images/characters/archer/Sprites/Arrow.png').convert_alpha()
        self.__image = pygame.transform.scale2x(self.__image)
        if is_flipped:
            self.__image = pygame.transform.flip(self.__image, True, False)
        self.__speed = speed

    def get_rect(self):
        return self.__rect

    def get_damage(self) -> float:
        return self.__damage

    def update(self, delta_time):
        dx = (-1 if self.__is_flipped else 1) * self.__speed * delta_time
        self.__rect.x += dx

    def draw(self, screen, debug=False):
        if debug:
            pygame.draw.rect(screen, Colors.RED.value, self.__rect)
        screen.blit(self.__image, (self.__rect.x, self.__rect.centery - self.__image.get_height() / 2))