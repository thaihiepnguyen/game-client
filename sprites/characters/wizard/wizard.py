from typing import override


from core.character.character import Character
from sprites.characters.wizard.fireball.fireball import Fireball
from sprites.characters.wizard.wizard_animation import WizardAnimation

import pygame

class Wizard(Character):
    def __init__(self, animation: WizardAnimation):
        super().__init__(animation)
        self.__fire_balls: list[Fireball] = []

    @override
    def _set_speed(self) -> float:
        return 230

    @override
    def update(self, _: pygame.Surface, delta_time: float) -> None:
        super().update(_, delta_time)

        for fire_ball in self.__fire_balls[:]:  # Shallow copy
            if not fire_ball.update(delta_time):
                self.__fire_balls.remove(fire_ball)

    @override
    def draw(self, ground_y: float, screen: pygame.Surface, debug: bool = False) -> None:
        super().draw(ground_y, screen, debug)

        for fire_ball in self.__fire_balls:
            fire_ball.draw(screen, debug)

    def add_fire_ball(self, fire_ball: Fireball) -> None:
        self.__fire_balls.append(fire_ball)