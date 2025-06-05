from typing import override

from core.scene.scene import Scene
from sprites.backgrounds.bridge.bridge_animation import BridgeAnimation
from sprites.backgrounds.countryside.countryside_animation import CountrysideAnimation
from sprites.backgrounds.temple.temple_animation import TempleAnimation
from sprites.backgrounds.tokyo.tokyo_animation import TokyoAnimation
from sprites.characters.yamabushi_tengu.yamabushi_tengu import YamabushiTengu
from sprites.characters.samurai.samurai import Samurai
from sprites.characters.yamabushi_tengu.yamabushi_tengu_animation import YamabushiTenguAnimation
from sprites.characters.samurai.samurai_animation import SamuraiAnimation
from sprites.backgrounds.street.street_animation import StreetAnimation

from sprites.health_bar import HealthBar
import pygame

class BattleScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.__bg_animation = StreetAnimation()
        self.__fighter = YamabushiTengu(
            x=100, 
            y=200,
            animation=YamabushiTenguAnimation(),
            speed=300, 
            weight=1,
            jump_velocity=38,
            atk=10
        )
        self.__health_bar_tl = HealthBar(
            'topleft',
            self.__fighter
        )
        self.__opponent = YamabushiTengu(
            x=500, 
            y=200,
            animation=YamabushiTenguAnimation(),
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
        scaled_bg_image = pygame.transform.scale(self.__bg_animation.get_current_frame(), (screen.get_width(), screen.get_height()))
        screen.blit(scaled_bg_image, (0, 0))
        self.__fighter.draw(screen)
        self.__health_bar_tl.draw(screen)
        self.__opponent.draw(screen)
        self.__health_bar_tr.draw(screen)
        self.__fighter.look_at(self.__opponent)
        self.__opponent.look_at(self.__fighter)

    @override
    def handle_event(self, event: pygame.event.Event):
        pass

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        self.__bg_animation.update(delta_time)

        ground_y = screen.get_height() * self.__bg_animation.get_ground_y_ratio()
        self.__fighter.apply_gravity(ground_y, delta_time)
        self.__opponent.apply_gravity(ground_y, delta_time)

        if self.__fighter.is_dead() or self.__opponent.is_dead():
            # game end logic can be handled here
            pass

        self.__fighter.update(screen, delta_time)
        self.__opponent.update(screen, delta_time)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and keys[pygame.K_LSHIFT]:
            self.__fighter.run(screen, -self.__fighter.get_speed() * delta_time * 1.5)
            return
        if keys[pygame.K_RIGHT] and keys[pygame.K_LSHIFT]:
            self.__fighter.run(screen, self.__fighter.get_speed() * delta_time * 1.5)
            return
        if keys[pygame.K_LEFT]:
            self.__fighter.move(screen, -self.__fighter.get_speed() * delta_time)
        if keys[pygame.K_RIGHT]:
            self.__fighter.move(screen, self.__fighter.get_speed() * delta_time)
        if keys[pygame.K_z]:
            self.__fighter.attack(screen, self.__opponent)
        if keys[pygame.K_SPACE]:
            self.__fighter.jump()
        if not any(keys):
            self.__fighter.idle()
