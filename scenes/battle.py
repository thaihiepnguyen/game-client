from typing import override

from core.scene import Scene
from core.const import BACKGROUND_IMAGE
from sprites.fighter import Fighter
from core.gui.button import Button
from sprites.health_bar import HealthBar
import pygame

class BattleScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.__bg_image = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        self.__fighter = Fighter(
            x=100, 
            y=200, 
            speed=300, 
            weight=1,
            jump_velocity=30,
            atk=10
        )
        self.__health_bar_tl = HealthBar(
            'topleft',
            self.__fighter
        )
        self.__opponent = Fighter(
            x=500, 
            y=200, 
            speed=300, 
            weight=1,
            jump_velocity=30,
            atk=6
        )
        self.__health_bar_tr = HealthBar(
            'topright',
            self.__opponent
        )

    @override
    def draw(self, screen: pygame.Surface) -> None:
        scaled_bg_image = pygame.transform.scale(self.__bg_image, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_bg_image, (0, 0))
        self.__fighter.draw(screen)
        self.__health_bar_tl.draw(screen)
        self.__opponent.draw(screen)
        self.__health_bar_tr.draw(screen)
        self.__fighter.look_at(self.__opponent)

    @override
    def handle_event(self, event: pygame.event.Event):
        pass

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        speed = self.__fighter.get_speed()
        ground_y = screen.get_height() * 4.075 / 5
        self.__fighter.apply_gravity(ground_y, delta_time)
        self.__opponent.apply_gravity(ground_y, delta_time)

        if self.__fighter.is_dead() or self.__opponent.is_dead():
            pass

        self.__fighter.update(screen, delta_time)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.__fighter.move(screen, -speed * delta_time) # each frame move speed * delta_time pixels
        if keys[pygame.K_RIGHT]:
            self.__fighter.move(screen, speed * delta_time)
        if keys[pygame.K_z]:
            self.__fighter.attack(screen, self.__opponent)
        if keys[pygame.K_SPACE]:
            self.__fighter.jump()