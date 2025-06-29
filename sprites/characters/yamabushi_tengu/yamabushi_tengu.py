from typing import override

from pygame.key import ScancodeWrapper

from core.character.character import Character
from sprites.characters.yamabushi_tengu.yamabushi_tengu_animation import YamabushiTenguAnimation

import pygame

class YamabushiTengu(Character):
    def __init__(self, animation: YamabushiTenguAnimation):
        super().__init__(animation)

    @override
    def _set_speed(self) -> float:
        return 230