from typing import override

from pygame import Rect

from core.character.character import Character
from core.const import WINDOW_WIDTH
from sprites.characters.archer.archer_animation import ArcherAnimation

import pygame

from sprites.characters.archer.arrow.arrow import Arrow


class Archer(Character):
    def __init__(self, animation: ArcherAnimation):
        super().__init__(animation)
        self.__is_subscribed_on_complete = False
        self.__arrows = []

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)

        for arrow in self.__arrows:
            arrow.update(delta_time)
            if arrow.get_rect().x < 0 or arrow.get_rect().x > WINDOW_WIDTH:
                self.__arrows.remove(arrow)
            else:
                arrow.draw(screen)

    @override
    def get_atk_z_box(self) -> Rect:
        w = 1.7 * self._rect.width
        h = 0.3 * self._rect.height
        x = (self._rect.centerx - w) if self._flipped else self._rect.centerx
        y = self._rect.y + self._rect.height * 0.3 - h * 0.5
        return Rect(x, y, w, h)

    @override
    def get_atk_x_box(self) -> Rect:
        w = 1.8 * self._rect.width
        h = 0.6 * self._rect.height
        x = (self._rect.centerx - w) if self._flipped else self._rect.centerx
        y = self._rect.y + self._rect.height * 0.5 - h * 0.5
        return Rect(x, y, w, h)

    @override
    def get_atk_c_box(self) -> Rect | None:
        return None

    def _set_speed(self) -> float:
        return 300

    def _set_weight(self) -> float:
        return 1

    def _set_jump_velocity(self) -> float:
        return 32

    def _set_atk(self) -> tuple[float, float, float]:
        return (
            10,  # Attack power for 'z' attack
            15,  # Attack power for 'x' attack
            20   # Attack power for 'c' attack
        )

    def _set_armor(self) -> float:
        return 1

    def __on_shoot_animation_complete(self, _: None):
        self.__arrows.append(Arrow(self._rect.right, self._rect.centery - 40, self._flipped))
        self.__is_subscribed_on_complete = False

    def get_arrow(self) -> Arrow | None:
        if self.__is_subscribed_on_complete:
            return None

        self._character_animation.get_animation_by_action('atk_c').subscribe_on_complete(
            self.__on_shoot_animation_complete
        )

        self.__is_subscribed_on_complete = True
        return self.__arrows.pop() if len(self.__arrows) > 0 else None