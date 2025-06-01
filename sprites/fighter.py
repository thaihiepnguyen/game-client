from typing import Dict, override

from core.character import ActionType, Character
import pygame

class Fighter(Character):
    def __init__(self, x: float, y: float, speed: float, atk: float, weight: float = 1, jump_velocity: float = 30):
        super().__init__(x, y, speed, weight, jump_velocity, atk)
            
    @override
    def _set_sprite_dir(self) -> str:
        return "assets/images/warrior/Sprites/warrior.png"

    @override
    def _set_action_index_map(self) -> Dict[ActionType, int]:
        return super()._set_action_index_map()
    
    @override
    def _set_animation_steps(self) -> list:
        return [10, 8, 1, 7, 7, 3, 7]

    @override
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)