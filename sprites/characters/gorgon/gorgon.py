from typing import override

from core.character.character import Character

from sprites.characters.gorgon.gorgon_animation import GorgonAnimation


class Gorgon(Character):
    def __init__(self, x: float, y: float, animation: GorgonAnimation):
        super().__init__(x, y, animation)

    @override
    def _jump(self) -> None:
        return

    @override
    def _set_speed(self) -> float:
        return 300

    @override
    def _set_weight(self) -> float:
        return 1

    @override
    def _set_jump_velocity(self) -> float:
        return 36

    @override
    def _set_atk(self) -> float:
        return 10

    @override
    def _set_armor(self) -> float:
        return 1