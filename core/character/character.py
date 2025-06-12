import pygame
from abc import ABC, abstractmethod

from pygame.key import ScancodeWrapper

from core.const import ATTACK_COOLDOWN, CHARACTER_HEIGHT, CHARACTER_WIDTH, Colors, GRAVITY, LOCK_FPS, SHADOW_HEIGHT, SHADOW_WIDTH, WINDOW_WIDTH
from core.character.character_animation import CharacterAnimation
from typing import List

class Character(ABC):
    def __init__(self, x: float, y: float, character_animation: CharacterAnimation):
        # --- Stats ---
        self.__max_hp = 100
        self.__current_hp = self.__max_hp
        self.__atk = self._set_atk()
        self.__armor = self._set_armor()

        # --- Movement / Physics ---
        self._velocity_y = 0.0
        self.__speed = self._set_speed()
        self.__weight = self._set_weight()
        self.__jump_velocity = self._set_jump_velocity()

        # --- State Flags ---
        self._state = 'idle'
        self.__stop_update = False
        self._flipped = False
        self.__is_invincible = False

        # --- Timers ---
        self._last_attack_time = 0
        self.__invincibility_time = 0

        # --- Graphics & Hitboxes ---
        self._rect = pygame.Rect(x, y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self._shadow_rect = pygame.Rect(x, y, SHADOW_WIDTH, SHADOW_HEIGHT)
        self._character_animation = character_animation
        self.__atk_rect = None

        # --- Sanity Check ---
        if self.__speed < 0 or self.__weight <= 0 or self.__jump_velocity < 0 or self.__atk < 0 or self.__armor < 0:
            raise ValueError("Speed, weight, jump_velocity, and atk must be non-negative.")

    # --- Abstract Setters for Subclasses ---
    @abstractmethod
    def _set_speed(self) -> float: pass

    @abstractmethod
    def _set_weight(self) -> float: pass

    @abstractmethod
    def _set_jump_velocity(self) -> float: pass

    @abstractmethod
    def _set_atk(self) -> float: pass

    @abstractmethod
    def _set_armor(self) -> float: pass

    # --- Public Getters ---
    def get_rect(self) -> pygame.rect.Rect: return self._rect
    def get_hp(self) -> float: return self.__current_hp
    def get_max_hp(self) -> float: return self.__max_hp
    def get_atk(self) -> float: return self.__atk
    def get_speed(self) -> float: return self.__speed
    def get_armor(self) -> float: return self.__armor
    def is_dead(self) -> bool: return self.__current_hp <= 0

    # --- Core Actions ---
    def _attack_z(self) -> None:
        if not self._can_attack():
            return

        self._state = 'atk_z'
        self._last_attack_time = pygame.time.get_ticks()

    def _attack_x(self) -> None:
        if not self._can_attack():
            return

        self._state = 'atk_x'
        self._last_attack_time = pygame.time.get_ticks()

    def _prevent_move_actions(self):
        return ['atk_z', 'atk_x', 'atk_c', 'def', 'hit']

    def walk(self, dx: float) -> None:
        if self._state in self._prevent_move_actions():
            return

        x = max(0, min(int(self._rect.x + dx), WINDOW_WIDTH - self._rect.width))
        if self._state == 'jump':
            self._rect.x = x
            return

        self._state = 'walk'
        self._rect.x = x

    def _jump(self) -> None:
        if self._state in self._prevent_move_actions():
            return

        self._state = 'jump'
        if self._velocity_y == 0.0:
            self._velocity_y = -self.__jump_velocity * LOCK_FPS

    def _defend(self) -> None:
        self._state = 'def'

    def is_defend(self) -> bool:
        return self._state == 'def'

    def take_damage(self, damage: float, knock_back: int = 15) -> None:
        if self.__is_invincible:
            return

        self._state = 'hit'
        self.__current_hp = max(0.0, self.__current_hp - damage)

        self.__is_invincible = True
        self.__invincibility_time = pygame.time.get_ticks()

        x = max(0, min(int(self._rect.x + knock_back * int(self._flipped)), WINDOW_WIDTH - self._rect.width))
        self._rect.x = x

    def look_at(self, opponent: "Character") -> None:
        if not self.is_dead():
            self._flipped = self._rect.centerx > opponent._rect.centerx

    def apply_gravity(self, ground_y: float, delta_time: float) -> None:
        self._velocity_y += GRAVITY * self.__weight * delta_time
        self._rect.y += self._velocity_y * delta_time

        if self._rect.bottom >= ground_y:
            self._rect.bottom = int(ground_y)
            self._velocity_y = 0.0

    def get_attack_hitbox(self) -> pygame.rect.Rect | None:
        if self._state == 'atk_z' or self._state == 'atk_x':
            if self.__atk_rect is None:
                attack_w = 1.8 * self._rect.width
                attack_h = 0.3 * self._rect.height
                attack_x = self._rect.centerx - attack_w if self._flipped else self._rect.centerx
                attack_y = self._rect.y + 20

                self.__atk_rect = pygame.Rect(attack_x, attack_y, attack_w, attack_h)
        else:
            self.__atk_rect = None

        return self.__atk_rect

    def _can_attack(self) -> bool:
        return (pygame.time.get_ticks() - self._last_attack_time) >= ATTACK_COOLDOWN

    def handle_event(self, event: pygame.event.Event):
        """Handle input events for the character."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self._attack_z()

            if event.key == pygame.K_x:
                self._attack_x()

            if event.key == pygame.K_SPACE:
                self._jump()

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LSHIFT]:
                if self._state == 'walk' or self._state == 'def':
                    self._state = 'idle'

    def handle_input(self, keys: ScancodeWrapper, delta_time: float) -> None:
        if keys[pygame.K_LEFT]:
            dx = self.get_speed() * delta_time
            self.walk(-dx)
        if keys[pygame.K_RIGHT]:
            dx = self.get_speed() * delta_time
            self.walk(dx)

    def _one_loop_actions(self) -> List[str]:
        return ['atk_z', 'atk_x', 'atk_c', 'hit', 'jump']

    # --- Update & Animation ---
    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        if self.__stop_update:
            return

        if self.is_dead():
            self._state = 'death'

        self._character_animation.update(self._state, delta_time)

        if self._character_animation.get_current_animation().is_complete():
            if self._state == 'death':
                self.__stop_update = True
            if self._state in self._one_loop_actions():
                self._state = 'idle'

        if self.__is_invincible:
            if pygame.time.get_ticks() - self.__invincibility_time > 500:
                self.__is_invincible = False

    # --- Drawing ---
    def draw(self, screen: pygame.Surface, debug: bool = False) -> None:
        if debug:
            pygame.draw.rect(screen, Colors.RED.value, self._rect)

        image = self._character_animation.get_current_frame(self._flipped)

        offset_x = self._rect.centerx - image.get_width() / 2
        offset_y = self._rect.bottom - image.get_height()

        if self._velocity_y == 0.0:
            self._shadow_rect.centerx = self._rect.centerx
            self._shadow_rect.y = self._rect.bottom - 10
            pygame.draw.ellipse(screen, Colors.BLACK.value, self._shadow_rect)

        screen.blit(image, (offset_x, offset_y))
