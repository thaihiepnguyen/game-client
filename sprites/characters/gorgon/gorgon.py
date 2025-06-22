from typing import override

from core.character.character import Character

from sprites.characters.gorgon.gorgon_animation import GorgonAnimation


class Gorgon(Character):
    def __init__(self, animation: GorgonAnimation):
        super().__init__(animation)

    @override
    def _jump(self) -> None:
        return

    def _set_speed(self) -> float:
        return 350

    def _set_weight(self) -> float:
        return 1

    def _set_jump_velocity(self) -> float:
        return 0

    def _set_atk(self) -> tuple[float, float, float]:
        return (
            10,  # Attack power for 'z' attack
            15,  # Attack power for 'x' attack
            20   # Attack power for 'c' attack
        )

    def _set_armor(self) -> float:
        return 3