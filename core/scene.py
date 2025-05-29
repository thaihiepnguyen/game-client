import pygame
from abc import ABC, abstractmethod


class Scene(ABC):
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        """
        Draw the scene on the given screen surface.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """
        Handle a single event.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        pass

    @abstractmethod
    def update(self, delta_time: float):
        """
        Update the scene with the given delta time.

        Args:
            delta_time (float): The time since the last update in seconds.
        """
        pass

