from typing import override

from core.character.character import Character
from sprites.characters.archer.archer_animation import ArcherAnimation

import pygame

from sprites.characters.archer.arrow.arrow import Arrow


class Archer(Character):
    def __init__(self, x: float, y: float, animation: ArcherAnimation):
        super().__init__(x, y, animation)
        self.__arrows = []

    def __shoot(self):
        if not self._can_attack():
            return
        self._state = 'atk_c'
        self._last_attack_time = pygame.time.get_ticks()
        self._character_animation.get_animation_by_action('atk_c').subscribe_on_complete(
            lambda _: self.__arrows.append(Arrow(self._rect.right, self._rect.centery - 40, not self._flipped))
        )

    def get_arrows(self) -> list[Arrow]:
        return self.__arrows

    @override
    def _set_speed(self) -> float:
        return 300

    @override
    def _set_weight(self) -> float:
        return 1

    @override
    def _set_jump_velocity(self) -> float:
        return 36

    @override
    def _set_atk(self) -> float:
        return 10

    @override
    def _set_armor(self) -> float:
        return 1

    @override
    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                self.__shoot()

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        super().update(screen, delta_time)

        for arrow in self.__arrows:
            arrow.update(delta_time)
            if arrow.get_rect().x < 0 or arrow.get_rect().x > screen.get_width():
                self.__arrows.remove(arrow)
            else:
                arrow.draw(screen)

