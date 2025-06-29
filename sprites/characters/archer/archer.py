from typing import override

from pygame import Rect

from core.character.character import Character
from sprites.characters.archer.archer_animation import ArcherAnimation

from sprites.characters.archer.arrow.arrow import Arrow


class Archer(Character):
    def __init__(self, animation: ArcherAnimation):
        super().__init__(animation)
        self.__is_subscribed_on_complete = False
        self.__arrows = []

    @override
    def _set_speed(self) -> float:
        return 250