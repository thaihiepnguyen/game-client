from typing import override

from pygame.key import ScancodeWrapper

from core.character.character import Character
from sprites.characters.yamabushi_tengu.yamabushi_tengu_animation import YamabushiTenguAnimation

import pygame

class YamabushiTengu(Character):
    def __init__(self, x: float, y: float, animation: YamabushiTenguAnimation):
        super().__init__(x, y, animation)

    @override
    def handle_input(self, keys: ScancodeWrapper, delta_time: float) -> None:
        super().handle_input(keys, delta_time)
        if keys[pygame.K_LSHIFT]:
            self._defend()

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)

    @override
    def _set_speed(self) -> float:
        return 300

    @override
    def _set_weight(self) -> float:
        return 1

    @override
    def _set_jump_velocity(self) -> float:
        return 34

    @override
    def _set_atk(self) -> float:
        return 40

    @override
    def _set_armor(self) -> float:
        return 2