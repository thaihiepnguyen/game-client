from core.character import Character
import pygame

class Fighter(Character):
    def __init__(self, x, y):
        super().__init__(x, y)


    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (255, 0, 0), self.rect)