from typing import override

from pygame import Rect
from pygame.key import ScancodeWrapper

from core.character.character import Character
from core.const import ATTACK_COOLDOWN, Colors
from sprites.characters.fighter.fighter_animation import FighterAnimation

import pygame

class Fighter(Character):
    def __init__(self, x: float, y: float, animation: FighterAnimation):
        super().__init__(x, y, animation)
        self.__kick_way_box = None

    @override
    def handle_input(self, keys: ScancodeWrapper, delta_time: float) -> None:
        super().handle_input(keys, delta_time)
        if keys[pygame.K_LSHIFT]:
            self._defend()

    @override
    def get_atk_c_box(self) -> Rect | None:
        return None

    def get_kick_away_box(self) -> Rect | None:
        return self.__kick_way_box

    def __on_kick_animation_complete(self, _=None) -> None:
        self.__kick_way_box = None

    @override
    def _attack_c(self) -> None:
        super()._attack_c()
        (self._character_animation.get_animation_by_action(self._state)
         .subscribe_on_complete(self.__on_kick_animation_complete))

        w = 1.2 * self._rect.width
        h = 0.3 * self._rect.height
        x = (self._rect.centerx - w) if self._flipped else self._rect.centerx
        y = self._rect.y + self._rect.height * 0.5 - h * 0.5
        self.__kick_way_box = Rect(x, y, w, h)

    @override
    def _set_attack_count_down(self) -> float:
        """Set the cooldown time for attacks in milliseconds."""
        return ATTACK_COOLDOWN / 2

    def _set_speed(self) -> float:
        return 300

    def _set_weight(self) -> float:
        return 1

    def _set_jump_velocity(self) -> float:
        return 34

    def _set_atk(self) -> tuple[float, float, float]:
        return (
            15,  # Attack power for 'z' attack
            10,  # Attack power for 'x' attack
            20   # Attack power for 'c' attack
        )

    def _set_armor(self) -> float:
        return 3