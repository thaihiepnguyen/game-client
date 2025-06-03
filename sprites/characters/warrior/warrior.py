from typing import override

from core.character.character import Character
from sprites.characters.warrior.warrior_animation import WarriorAnimation
import pygame

class Warrior(Character):
    def __init__(self, x: float, y: float, animation: WarriorAnimation, speed: float, atk: float, weight: float = 1, jump_velocity: float = 30):
        super().__init__(x, y, animation, speed, weight, jump_velocity, atk)

    @override
    def draw(self, screen: pygame.Surface, debug: bool = False) -> None:
        super().draw(screen)

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)