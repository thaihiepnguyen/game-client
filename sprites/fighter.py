from typing import Dict, override

from core.character import ActionType, Character
from sprites.characters.animation_manager import AnimationManager
import pygame

class Fighter(Character):
    def __init__(self, x: float, y: float, speed: float, atk: float, weight: float = 1, jump_velocity: float = 30):
        super().__init__(x, y, speed, weight, jump_velocity, atk)
            
    
    @override
    def _set_animation(self):
        return AnimationManager(
            sprite_dir="assets/images/warrior/Sprites/warrior.png",
            animation_steps=[10, 8, 1, 7, 7, 3, 7],
            sprite_size=162,
            sprite_scale=4,
            action_index_map={
                "idle": 0,
                "run": 1,
                "jump": 2,
                "atk": 3
            }
        )

    @override
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)