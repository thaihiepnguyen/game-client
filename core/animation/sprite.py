import pygame
from typing import List

class Sprite:
    def __init__(self, dir: str, w: float, h: float, count: int):
        self.image = pygame.image.load(dir).convert_alpha()
        self.__w = w
        self.__h = h
        self.__count = count
        self.__frames = self.__convert_to_frames()

    def __convert_to_frames(self) -> List[pygame.Surface]:
        """
        Convert the sprite image into a list of frames based on the specified width, height, and count.
        :return: A list of pygame.Surface objects representing the frames of the sprite.
        """
        frames = []
        for i in range(self.__count):
            frame = self.image.subsurface(
                (i * self.__w, 0, self.__w, self.__h)
            )
            frames.append(frame)
        return frames

    def get_frames(self) -> List[pygame.Surface]:
        return self.__frames

    def get_width(self) -> float:
        return self.__w

    def get_height(self) -> float:
        return self.__h