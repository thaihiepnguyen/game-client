from typing import override

from core.character.character import Character
from sprites.characters.samurai.samurai_animation import SamuraiAnimation

import pygame

class Samurai(Character):
    def __init__(self, x: float, y: float, animation: SamuraiAnimation):
        super().__init__(x, y, animation)
        self._scale = 2.5

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)
        self._character_animation.get_current_animation().set_scale(self._scale)

    def _set_speed(self) -> float:
        return 300

    def _set_weight(self) -> float:
        return 1

    def _set_jump_velocity(self) -> float:
        return 33

    def _set_atk(self) -> float:
        return 10

    def _set_armor(self) -> float:
        return 2