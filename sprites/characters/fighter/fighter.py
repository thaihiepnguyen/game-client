from typing import override

from pygame import Rect
from pygame.key import ScancodeWrapper

from core.character.character import Character
from sprites.characters.fighter.fighter_animation import FighterAnimation

import pygame

class Fighter(Character):
    def __init__(self, animation: FighterAnimation):
        super().__init__(animation)

    @override
    def _set_speed(self) -> float:
        return 300