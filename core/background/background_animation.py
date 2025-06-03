from abc import ABC, abstractmethod

import pygame
from core.animation.animation import Animation


class BackgroundAnimation(ABC):
    def __init__(self):
        self.__animation: Animation = self._load_animation()

    @abstractmethod
    def _load_animation(self) -> Animation:
        """
        Load the background animation frames.
        This method should be implemented by subclasses to load specific background animations.
        :return: A pygame.Surface object representing the background animation.
        """
        pass

    def update(self, delta_time: float) -> None:
        """
        Update the background animation based on the elapsed time.
        :param delta_time: The time elapsed since the last update in seconds.
        :return:
        """
        self.__animation.update(delta_time)
    
    def get_current_frame(self) -> pygame.Surface:
        return self.__animation.get_current_frame(darken=60)