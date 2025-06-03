import pygame
from core.animation.sprite import Sprite

class Animation:
    def __init__(self, sprite: Sprite, frame_duration: float, loop: bool = True):
        """
        Initialize the Animation with a list of frames and the duration for each frame.
        :param sprite: List of sprites to be used in the animation.
        :param frame_duration: Duration for each frame in seconds.
        """
        self.__sprite = sprite
        self.__frames = sprite.get_frames()
        self.__frame_duration = frame_duration
        self.__loop = loop
        self.__current_frame_index = 0
        self.__time_since_last_frame = 0.0

    def update(self, delta_time: float):
        """Update the animation based on the elapsed time."""
        self.__time_since_last_frame += delta_time

        if self.__time_since_last_frame >= self.__frame_duration:
            self.__current_frame_index = (self.__current_frame_index + 1) % len(self.__frames)
            self.__time_since_last_frame = 0.0

    def get_current_frame(self, flip: bool = False) -> pygame.Surface:
        """Get the current frame of the animation."""
        frame = self.__frames[self.__current_frame_index]
        return pygame.transform.flip(frame, flip, False) if flip else frame

    def reset(self):
        """Reset the animation to the first frame."""
        self.__current_frame_index = 0
        self.__time_since_last_frame = 0.0

    def is_complete(self) -> bool:
        """Check if the animation has completed."""
        return self.__current_frame_index == len(self.__frames) - 1

    def get_sprite(self):
        """Get the sprite associated with the animation."""
        return self.__sprite