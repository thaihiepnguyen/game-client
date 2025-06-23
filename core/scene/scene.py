import pygame
from abc import ABC, abstractmethod

from core.network.tcp_client import TCPClient


class Scene(ABC):
    def __init__(self, scene_manager, tcp_client: TCPClient): # can not define type of this variable because of cicular dependency
        super().__init__()
        self._scene_manager = scene_manager
        self._tcp_client = tcp_client
    
    def _on_enter(self, data=dict | None) -> None:
        """
        Called when the scene is entered.
        This method can be overridden to perform any setup or initialization tasks.
        :param data: Optional data to initialize the scene with.
        """
        pass

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

