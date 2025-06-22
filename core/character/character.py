import pygame
from abc import ABC, abstractmethod

from pygame import Rect
from pygame.key import ScancodeWrapper

from core.const import ATTACK_COOLDOWN, CHARACTER_HEIGHT, CHARACTER_WIDTH, Colors, GRAVITY, LOCK_FPS, SHADOW_HEIGHT, SHADOW_WIDTH, WINDOW_WIDTH
from core.character.character_animation import CharacterAnimation
from typing import List

class Character(ABC):
    def __init__(self, character_animation: CharacterAnimation):
        # --- Stats ---
        self.__max_hp = 100
        self.__current_hp = self.__max_hp
        self.__atk_z, self.__atk_x, self.__atk_c = self._set_atk()
        self.__armor = self._set_armor()
        self.__attack_count_down = self._set_attack_count_down()

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
        self._rect = pygame.Rect(0, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self._shadow_rect = pygame.Rect(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
        self._character_animation = character_animation
        self.__atk_rect = None

        # --- Sanity Check ---
        if self.__speed < 0 or self.__weight <= 0 or self.__jump_velocity < 0 or self.__atk_z < 0 or self.__atk_x < 0 or self.__atk_c < 0 or self.__armor < 0:
            raise ValueError('Speed, weight, jump_velocity, atk and armor must be non-negative.')

    # --- Abstract Setters for Subclasses ---
    @abstractmethod
    def _set_speed(self) -> float:
        """Set the speed of the character, affecting movement speed."""
        pass

    @abstractmethod
    def _set_weight(self) -> float:
        """Set the weight of the character, affecting gravity and jump physics."""
        pass

    @abstractmethod
    def _set_jump_velocity(self) -> float:
        """Set the jump velocity for the character."""
        pass

    @abstractmethod
    def _set_atk(self) -> tuple[float, float, float]:
        """Set the attack values for different attack types (z, x, c)."""
        pass

    @abstractmethod
    def _set_armor(self) -> float:
        """Set the armor value for the character, affecting damage taken."""
        pass

    def _set_attack_count_down(self) -> int:
        """Set the cooldown time for attacks in milliseconds."""
        return ATTACK_COOLDOWN

    # --- Public Getters ---
    def get_rect(self) -> Rect: return self._rect
    def get_hp(self) -> float: return self.__current_hp
    def get_max_hp(self) -> float: return self.__max_hp
    def get_atk(self) -> float:
        if self._state == 'atk_z':
            return self.__atk_z
        elif self._state == 'atk_x':
            return self.__atk_x
        return self.__atk_c
    def get_speed(self) -> float: return self.__speed
    def get_armor(self) -> float: return self.__armor
    def is_dead(self) -> bool: return self.__current_hp <= 0
    def is_defend(self) -> bool: return self._state == 'def'

    # --- Public Setters ---
    def set_x(self, x: int) -> None:
        """
        Set the x-coordinate of the character's position.
        Ensures the character does not move out of bounds.
        """
        self._rect.x = max(0, min(x, WINDOW_WIDTH - self._rect.width))

    def set_y(self, y: int) -> None:
        """
        Set the y-coordinate of the character's position.
        Ensures the character does not move out of bounds.
        """
        self._rect.y = max(0, y)

    # --- Core Actions ---
    def _attack_z(self) -> None:
        self._state = 'atk_z'

    def _attack_x(self) -> None:
        self._state = 'atk_x'

    def _attack_c(self) -> None:
        self._state = 'atk_c'

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

    def take_damage(self, damage: float, knock_back: int = 15) -> None:
        if self.__is_invincible:
            return

        self._state = 'hit'
        self.__current_hp = max(0.0, self.__current_hp - damage)

        self.__is_invincible = True
        self.__invincibility_time = pygame.time.get_ticks()

        x = max(0, min(int(self._rect.x + knock_back * (1 if self._flipped else -1)), WINDOW_WIDTH - self._rect.width))
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

    def get_atk_z_box(self) -> Rect:
        w = 1.2 * self._rect.width
        h = 0.3 * self._rect.height
        x = (self._rect.centerx - w) if self._flipped else self._rect.centerx
        y = self._rect.y + self._rect.height * 0.5 - h * 0.5
        return Rect(x, y, w, h)

    def get_atk_x_box(self) -> Rect:
        w = 1.2 * self._rect.width
        h = 0.3 * self._rect.height
        x = (self._rect.centerx - w) if self._flipped else self._rect.centerx
        y = self._rect.y + self._rect.height * 0.5 - h * 0.5
        return Rect(x, y, w, h)

    def get_atk_c_box(self) -> Rect | None:
        w = 1.2 * self._rect.width
        h = 0.3 * self._rect.height
        x = (self._rect.centerx - w) if self._flipped else self._rect.centerx
        y = self._rect.y + self._rect.height * 0.5 - h * 0.5
        return Rect(x, y, w, h)

    def get_attack_hitbox(self, screen: pygame.Surface, debug: bool = False) -> Rect | None:
        if self._state == 'atk_z':
            self.__atk_rect = self.get_atk_z_box()
        elif self._state == 'atk_x':
            self.__atk_rect = self.get_atk_x_box()
        elif self._state == 'atk_c':
            self.__atk_rect = self.get_atk_c_box()
        else:
            self.__atk_rect = None

        if self.__atk_rect is not None:
            if debug:
                pygame.draw.rect(screen, Colors.RED.value, self.__atk_rect)

        return self.__atk_rect

    def __can_attack(self) -> bool:
        return (pygame.time.get_ticks() - self._last_attack_time) >= self.__attack_count_down

    def handle_event(self, event: pygame.event.Event):
        """Handle input events for the character."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if not self.__can_attack():
                    return
                self._attack_z()
                self._last_attack_time = pygame.time.get_ticks()

            if event.key == pygame.K_x:
                if not self.__can_attack():
                    return
                self._attack_x()
                self._last_attack_time = pygame.time.get_ticks()

            if event.key == pygame.K_c:
                if not self.__can_attack():
                    return
                self._attack_c()
                self._last_attack_time = pygame.time.get_ticks()

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
        """Return a list of actions that should only run once per input."""
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
