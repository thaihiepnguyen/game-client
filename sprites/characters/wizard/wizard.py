from typing import override

from pygame.key import ScancodeWrapper

from core.character.character import Character
from sprites.characters.wizard.wizard_animation import WizardAnimation

import pygame

class Wizard(Character):
    def __init__(self, animation: WizardAnimation):
        super().__init__(animation)

    @override
    def _set_speed(self) -> float:
        return 230