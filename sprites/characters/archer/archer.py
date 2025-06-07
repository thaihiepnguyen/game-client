from typing import override

from core.character.character import Character
from sprites.characters.archer.archer_animation import ArcherAnimation
from core.const import WINDOW_HEIGHT

import pygame


class Archer(Character):
    def __init__(self, x: float, y: float, animation: ArcherAnimation):
        super().__init__(x, y, animation)
        self._scale = 2.5

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)
        self._character_animation.get_current_animation().set_scale(
            self._scale * screen.get_height() / WINDOW_HEIGHT
        )

    def _set_speed(self) -> float:
        return 300

    def _set_weight(self) -> float:
        return 1

    def _set_jump_velocity(self) -> float:
        return 30

    def _set_atk(self) -> float:
        return 10

    def _set_armor(self) -> float:
        return 1