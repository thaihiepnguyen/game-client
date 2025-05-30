from typing import override

from core.character import Character
import pygame

class Fighter(Character):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    @override
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (255, 0, 0), self._rect)