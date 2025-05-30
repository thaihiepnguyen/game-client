import pygame
from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, scene_manager):
        super().__init__()
        self._scene_manager = scene_manager

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the scene on the current screen surface.
        :param screen: The screen surface to draw on.
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle a single event.
        :param event: The event.
        """
        pass

    @abstractmethod
    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        """
        Update the scene with the given delta time.
        :param screen: The screen surface.
        :param delta_time: The delta time.
        """
        pass

