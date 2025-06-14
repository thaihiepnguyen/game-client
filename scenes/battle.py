from typing import override

from core.scene.scene import Scene
from sprites.backgrounds.bridge.bridge_animation import BridgeAnimation
from sprites.backgrounds.countryside.countryside_animation import CountrysideAnimation
from sprites.backgrounds.temple.temple_animation import TempleAnimation
from sprites.backgrounds.tokyo.tokyo_animation import TokyoAnimation
from sprites.characters.archer.archer import Archer
from sprites.characters.archer.archer_animation import ArcherAnimation
from sprites.characters.fighter.fighter import Fighter
from sprites.characters.fighter.fighter_animation import FighterAnimation
from sprites.characters.gorgon.gorgon import Gorgon
from sprites.characters.gorgon.gorgon_animation import GorgonAnimation
from sprites.characters.yamabushi_tengu.yamabushi_tengu import YamabushiTengu
from sprites.characters.yamabushi_tengu.yamabushi_tengu_animation import YamabushiTenguAnimation
from sprites.backgrounds.street.street_animation import StreetAnimation

from sprites.health_bar import HealthBar
from core.const import CHARACTER_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH
import pygame

class BattleScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.__bg_animation = CountrysideAnimation()
        self.__fighter = Archer(
            x=100, 
            y=200,
            animation=ArcherAnimation(),
        )
        self.__health_bar_tl = HealthBar(
            pos='topleft',
            character=self.__fighter
        )
        self.__opponent = Gorgon(
            x=WINDOW_WIDTH - 100 - CHARACTER_WIDTH,
            y=200,
            animation=GorgonAnimation(),
        )
        self.__health_bar_tr = HealthBar(
            pos='topright',
            character=self.__opponent
        )

    @override
    def draw(self, screen: pygame.Surface) -> None:
        scaled_bg_image = pygame.transform.scale(self.__bg_animation.get_current_frame(), (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(scaled_bg_image, (0, 0))
        self.__fighter.draw(screen)
        self.__health_bar_tl.draw(screen)
        self.__opponent.draw(screen)
        self.__health_bar_tr.draw(screen)
        self.__fighter.look_at(self.__opponent)
        self.__opponent.look_at(self.__fighter)

    @override
    def handle_event(self, event: pygame.event.Event):
        self.__fighter.handle_event(event)

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        self.__bg_animation.update(delta_time)

        ground_y = WINDOW_HEIGHT * self.__bg_animation.get_ground_y_ratio()
        self.__fighter.apply_gravity(ground_y, delta_time)
        self.__opponent.apply_gravity(ground_y, delta_time)

        if self.__fighter.is_dead() or self.__opponent.is_dead():
            # game end logic can be handled here
            pass

        self.__fighter.update(screen, delta_time)
        self.__opponent.update(screen, delta_time)

        fighter_atk_hitbox = self.__fighter.get_attack_hitbox(screen)
        opponent_hurt_box = self.__opponent.get_rect()
        get_kick_away_box = self.__fighter.get_kick_away_box() if hasattr(self.__fighter, 'get_kick_away_box') else None
        arrows = self.__fighter.get_arrows() if hasattr(self.__fighter, 'get_arrows') else []

        if get_kick_away_box is not None:
            if get_kick_away_box.colliderect(opponent_hurt_box) and not self.__opponent.is_defend():
                self.__opponent.take_damage(max(0.0, self.__fighter.get_atk() - self.__opponent.get_armor()), 200)

        if fighter_atk_hitbox is not None:
            if fighter_atk_hitbox.colliderect(opponent_hurt_box) and not self.__opponent.is_defend():
                intersection = fighter_atk_hitbox.clip(opponent_hurt_box)
                damage_ratio = intersection.width / self.__opponent.get_rect().width
                damage = self.__fighter.get_atk() * damage_ratio - self.__opponent.get_armor()
                self.__opponent.take_damage(max(0.0, damage))

        if len(arrows) != 0:
            for arrow in arrows:
                if arrow.get_rect().colliderect(opponent_hurt_box) and not self.__opponent.is_defend():
                    damage = arrow.get_damage() - self.__opponent.get_armor()
                    self.__opponent.take_damage(max(0.0, damage))

        keys = pygame.key.get_pressed()
        self.__fighter.handle_input(keys, delta_time)