
import pygame

from core.const import Colors

class Arrow:
    def __init__(self, x, y, direction, speed=800):
        self.__rect = pygame.Rect(x, y, 160, 30)
        self.__image = pygame.image.load('assets/images/characters/archer/Sprites/Arrow.png').convert_alpha()
        self.__image = pygame.transform.scale2x(self.__image)
        self.__direction = direction
        self.__speed = speed

    def get_rect(self):
        return self.__rect


    def update(self, delta_time):
        self.__rect.x += self.__direction * self.__speed * delta_time

    def draw(self, screen, debug=True):
        if debug:
            pygame.draw.rect(screen, Colors.RED.value, self.__rect)
        screen.blit(self.__image, (self.__rect.x, self.__rect.centery - self.__image.get_height() / 2))