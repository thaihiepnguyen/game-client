import pygame
from abc import ABC, abstractmethod

CHARACTER_RECT_WIDTH = 80
CHARACTER_RECT_HEIGHT = 180

class Character(ABC):
    def __init__(self, x: float, y: float):
        self._rect = pygame.Rect((x, y, CHARACTER_RECT_WIDTH, CHARACTER_RECT_HEIGHT))

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the character on the current screen surface.
        :param screen: The screen surface to draw on.
        """
        pass

    def move(self, screen: pygame.Surface, dx: float, dy: float) -> None:
        """
        Move the character by dx and dy, ensuring it stays within the screen bounds.
        :param screen: pygame.Surface
        :param dx: pixel to move in the x direction
        :param dy: pixel to move in the y direction
        :return:
        """
        self._rect.x += dx
        self._rect.y += dy
        # Ensure the character stays within the screen bounds
        self._rect.x = max(0, min(self._rect.x, screen.get_width() - self._rect.width))
        self._rect.y = max(0, min(self._rect.y, screen.get_height() - self._rect.height))