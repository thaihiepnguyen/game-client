import pygame
from abc import ABC, abstractmethod

CHARACTER_RECT_WIDTH = 80
CHARACTER_RECT_HEIGHT = 180

class Character(ABC):
    def __init__(self, x: float, y: float):
        self.rect = pygame.Rect((x, y, CHARACTER_RECT_WIDTH, CHARACTER_RECT_HEIGHT))

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
        self.rect.x += dx
        self.rect.y += dy
        # Ensure the character stays within the screen bounds
        self.rect.x = max(0, min(self.rect.x, screen.get_width() - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen.get_height() - self.rect.height))