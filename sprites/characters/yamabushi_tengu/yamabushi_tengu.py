from typing import override

from core.character.character import Character
from sprites.characters.yamabushi_tengu.yamabushi_tengu_animation import YamabushiTenguAnimation
from core.const import WINDOW_HEIGHT, WINDOW_WIDTH

import pygame

class YamabushiTengu(Character):
    def __init__(self, x: float, y: float, animation: YamabushiTenguAnimation):
        super().__init__(x, y, animation)
        self.__scale = 2.2

    @override
    def draw(self, screen: pygame.Surface, debug: bool=False) -> None:
        super().draw(screen)
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self._rect)

        image = self._character_animation.get_current_frame(self._flipped)

        self._character_animation.get_current_animation().set_scale(self.__scale)

        offset_x = self._rect.x - (48 * self.__scale) * screen.get_width() / WINDOW_WIDTH
        offset_y = self._rect.bottom - image.get_height()
       
        screen.blit(image, (offset_x, offset_y))

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)
        self._character_animation.get_current_animation().set_scale(
            self.__scale * screen.get_height() / WINDOW_HEIGHT
        )


    def _set_speed(self) -> float:
        return 600

    def _set_weight(self) -> float:
        return 1

    def _set_jump_velocity(self) -> float:
        return 33

    def _set_atk(self) -> float:
        return 10

    def _set_armor(self) -> float:
        return 2