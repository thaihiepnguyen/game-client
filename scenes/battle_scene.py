from typing import override

from core.background.background_factory import BackgroundFactory
from core.character.character_factory import CharacterFactory
from core.scene.scene import Scene
from sprites.health_bar.health_bar import HealthBar
from core.const import CHARACTER_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH
import pygame

class BattleScene(Scene):
    def __init__(self, scene_manager, tcp_client):
        super().__init__(scene_manager, tcp_client)
        self.__room_id = None
        self.__char = None
        self.__oppo = None
        self.__bg = None
        self.__side = None
        self.__bg_animation = None
        self.__fighter = None
        self.__opponent = None
        self.__health_bar_tl = None
        self.__health_bar_tr = None

    @override
    def _on_enter(self, data: dict):
        self.__room_id = data.get('room_id', None)
        self.__char = data.get('char', None)
        self.__oppo = data.get('oppo', None)
        self.__bg = data.get('bg', None)
        self.__side = data.get('side', None)
        print(f"BattleScene: Entering with room_id={self.__room_id}, char={self.__char}, oppo={self.__oppo}, bg={self.__bg}, side={self.__side}")

        self.__bg_animation = BackgroundFactory.create_background(self.__bg)
        self.__fighter = CharacterFactory.create_character(self.__char)
        self.__opponent = CharacterFactory.create_character(self.__oppo)
        if not self.__side: # if character is on the left side
            self.__fighter.set_x(100)
            self.__fighter.set_y(200)
            self.__health_bar_tl = HealthBar(
                pos='topleft',
                character=self.__fighter
            )
            self.__opponent.set_x(WINDOW_WIDTH - 100 - CHARACTER_WIDTH)
            self.__opponent.set_y(200)
            self.__health_bar_tr = HealthBar(
                pos='topright',
                character=self.__opponent
            )
        else:  # if character is on the right side
            self.__fighter.set_x(WINDOW_WIDTH - 100 - CHARACTER_WIDTH)
            self.__fighter.set_y(200)
            self.__health_bar_tl = HealthBar(
                pos='topright',
                character=self.__fighter
            )
            self.__opponent.set_x(100)
            self.__opponent.set_y(200)
            self.__health_bar_tr = HealthBar(
                pos='topleft',
                character=self.__opponent
            )

    def draw(self, screen: pygame.Surface) -> None:
        if self.__bg_animation is None or self.__fighter is None or self.__opponent is None: return
        scaled_bg_image = pygame.transform.scale(self.__bg_animation.get_current_frame(), (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(scaled_bg_image, (0, 0))
        self.__fighter.draw(screen)
        self.__health_bar_tl.draw(screen)
        self.__opponent.draw(screen)
        self.__health_bar_tr.draw(screen)
        self.__fighter.look_at(self.__opponent)
        self.__opponent.look_at(self.__fighter)

    def handle_event(self, event: pygame.event.Event):
        if self.__fighter is None: return
        self.__fighter.handle_event(event)

    def update(self, screen: pygame.Surface, delta_time: float):
        if self.__bg_animation is None or self.__fighter is None or self.__opponent is None: return
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