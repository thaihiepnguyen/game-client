from typing import List, Callable, Tuple
import pygame
from pygame.font import FontType


class Button:
    def __init__(self, text: str, font: FontType, pos: Tuple[float, float], size: Tuple[float, float], color: Tuple[int, int, int]):
        self.__text = text
        self.__font = font
        self.__x, self.__y = pos
        self.__width, self.__height = size
        self.__color = color
        self.__rect = pygame.Rect(self.__x, self.__y, self.__width, self.__height)
        self.__listeners: List[Callable[[pygame.event.Event], None]] = []

    def on_click(self, listener: Callable[[pygame.event.Event], None]) -> None:
        """
        Register a listener for the button click event.
        :param listener: A callable that will be called when the button is clicked.
        """
        self.__listeners.append(listener)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle mouse events for the button.
        :param event: The pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__rect.collidepoint(event.pos):
                for listener in self.__listeners:
                    listener(event)


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the button on the given screen surface.
        :param screen: The screen surface to draw on.
        """

        rect = pygame.draw.rect(screen, self.__color, self.__rect)
        text_surface = self.__font.render(self.__text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
