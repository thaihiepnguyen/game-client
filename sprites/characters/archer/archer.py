from typing import override

import pygame

from core.character.character import Character
from sprites.characters.archer.archer_animation import ArcherAnimation

from sprites.characters.archer.arrow.arrow import Arrow


class Archer(Character):
    def __init__(self, animation: ArcherAnimation):
        super().__init__(animation)
        self.__arrows: list[Arrow] = []

    @override
    def _set_speed(self) -> float:
        return 250

    @override
    def update(self, _: pygame.Surface, delta_time: float) -> None:
        super().update(_, delta_time)

        for arrow in self.__arrows[:]:  # Shallow copy
            if arrow.update(delta_time):
                self.__arrows.remove(arrow)

    @override
    def draw(self, ground_y: float, screen: pygame.Surface, debug: bool = False) -> None:
        super().draw(ground_y, screen, debug)

        for arrow in self.__arrows:
            arrow.draw(screen, debug)

    def add_arrow(self, arrow: Arrow) -> None:
        self.__arrows.append(arrow)