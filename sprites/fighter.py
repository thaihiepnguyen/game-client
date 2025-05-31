from typing import override

from core.character import Character
import pygame

class Fighter(Character):
    def __init__(self, x: float, y: float, speed: float, weight: float = 1, jump_velocity: float = 30):
        super().__init__(x, y, speed, weight, jump_velocity)

    @override
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (255, 0, 0), self._rect)