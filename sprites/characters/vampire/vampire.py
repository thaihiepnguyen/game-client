from typing import override

from pygame.key import ScancodeWrapper

from core.character.character import Character
from sprites.characters.vampire.vampire_animation import VampireAnimation

import pygame

class Vampire(Character):
    def __init__(self, animation: VampireAnimation):
        super().__init__(animation)

    @override
    def _set_speed(self) -> float:
        return 230