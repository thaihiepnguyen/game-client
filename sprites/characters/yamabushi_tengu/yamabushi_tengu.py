from typing import override

from pygame.key import ScancodeWrapper

from core.character.character import Character
from sprites.characters.yamabushi_tengu.yamabushi_tengu_animation import YamabushiTenguAnimation

import pygame

class YamabushiTengu(Character):
    def __init__(self, animation: YamabushiTenguAnimation):
        super().__init__(animation)

    @override
    def handle_input(self, keys: ScancodeWrapper, delta_time: float) -> None:
        super().handle_input(keys, delta_time)
        if keys[pygame.K_LSHIFT]:
            self._defend()

    def _set_speed(self) -> float:
        return 300

    def _set_weight(self) -> float:
        return 1

    def _set_jump_velocity(self) -> float:
        return 34

    def _set_atk(self) -> tuple[float, float, float]:
        return (
            10,  # Attack power for 'z' attack
            15,  # Attack power for 'x' attack
            20   # Attack power for 'c' attack
        )

    def _set_armor(self) -> float:
        return 2