from typing import override

from core.character.character import Character
from sprites.characters.yamabushi_tengu.yamabushi_tengu_animation import YamabushiTenguAnimation
from core.const import WINDOW_HEIGHT

import pygame

class YamabushiTengu(Character):
    def __init__(self, x: float, y: float, animation: YamabushiTenguAnimation, speed: float, atk: float, weight: float = 1, jump_velocity: float = 30):
        super().__init__(x, y, animation, speed, weight, jump_velocity, atk)
        self.__scale = 2.2

    @override
    def draw(self, screen: pygame.Surface, debug: bool=False) -> None:
        super().draw(screen)
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self._rect)

        image = self._character_animation.get_current_frame(self._flipped)

        self._character_animation.get_current_animation().set_scale(self.__scale)

        offset_x = self._rect.x - (45 * self.__scale)
        offset_y = self._rect.bottom - image.get_height()
       
        screen.blit(image, (offset_x, offset_y))

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)
        self._character_animation.get_current_animation().set_scale(
            self.__scale * screen.get_height() / WINDOW_HEIGHT
        )