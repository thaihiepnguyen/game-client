import pygame
from core.animation.sprite import Sprite

class Animation:
    def __init__(self, sprite: Sprite, frame_duration: float):
        """
        Initialize the Animation with a list of frames and the duration for each frame.
        :param sprite: List of sprites to be used in the animation.
        :param frame_duration: Duration for each frame in seconds.
        """
        self.__sprite = sprite
        self.__frames = sprite.get_frames()
        self.__frame_duration = frame_duration
        self.__current_frame_index = 0
        self.__time_since_last_frame = 0.0
        self.__scale = 1
        self.__on_complete_subscribers = []

    def subscribe_on_complete(self, callback):
        """
        Subscribe a callback to be called when the animation completes.
        :param callback: Function to call when the animation completes.
        """
        self.__on_complete_subscribers.append(callback)

    def update(self, delta_time: float):
        """Update the animation based on the elapsed time."""
        self.__time_since_last_frame += delta_time

        if self.__time_since_last_frame >= self.__frame_duration:
            self.__current_frame_index = (self.__current_frame_index + 1) % len(self.__frames)
            if self.is_complete():
                self.complete()
            self.__time_since_last_frame = 0.0

    def get_current_frame(self, flip: bool = False, darken: int = 0) -> pygame.Surface:
        """Get the current frame of the animation."""
        frame = self.__frames[self.__current_frame_index]
        if flip:
            frame = pygame.transform.flip(frame, True, False)
        if darken > 0:
            frame = frame.copy()
            dark_overlay = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, darken))
            frame.blit(dark_overlay, (0, 0))
    
        scaled_frame = pygame.transform.scale(frame, (self.__sprite.get_width() * self.__scale, self.__sprite.get_height() * self.__scale))
        return scaled_frame
    
    def set_scale(self, scale):
        self.__scale = scale

    def reset(self):
        """Reset the animation to the first frame."""
        self.__current_frame_index = 0
        self.__time_since_last_frame = 0.0

    def is_complete(self) -> bool:
        """Check if the animation has completed."""
        return self.__current_frame_index == len(self.__frames) - 1

    def complete(self):
        """Complete the animation immediately."""
        for callback in self.__on_complete_subscribers:
            callback(self)
        self.__on_complete_subscribers = []

    def get_sprite(self):
        """Get the sprite associated with the animation."""
        return self.__sprite