from typing import override

from core.character.character import Character

from sprites.characters.gorgon.gorgon_animation import GorgonAnimation


class Gorgon(Character):
    def __init__(self, animation: GorgonAnimation):
        super().__init__(animation)

    @override
    def jump(self) -> None:
        return

    @override
    def _set_speed(self) -> float:
        return 300