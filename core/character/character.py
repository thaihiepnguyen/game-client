import pygame
from abc import ABC, abstractmethod
from core.const import ATTACK_COOLDOWN, CHARACTER_HEIGHT, CHARACTER_WIDTH, Colors, GRAVITY, LOCK_FPS, SHADOW_HEIGHT, SHADOW_WIDTH, WINDOW_WIDTH
from core.character.character_animation import CharacterAnimation

class Character(ABC):
    def __init__(self, x: float, y: float, character_animation: CharacterAnimation):
        # --- Stats ---
        self._max_hp = 100
        self._current_hp = self._max_hp
        self._atk = self._set_atk()
        self._armor = self._set_armor()

        # --- Movement / Physics ---
        self._velocity_y = 0.0
        self._speed = self._set_speed()
        self._weight = self._set_weight()
        self._jump_velocity = self._set_jump_velocity()

        # --- State Flags ---
        self._moving = False
        self._attacking = False
        self._taking_damage = False
        self._is_on_defense = False
        self._flipped = False

        # --- Timers ---
        self._last_attack_time = 0

        # --- Graphics & Hitboxes ---
        self._rect = pygame.Rect(x, y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self._shadow_rect = pygame.Rect(x, y, SHADOW_WIDTH, SHADOW_HEIGHT)
        self._character_animation = character_animation

        # --- Sanity Check ---
        if self._speed < 0 or self._weight <= 0 or self._jump_velocity < 0 or self._atk < 0 or self._armor < 0:
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

    # --- Public Setters ---
    def set_defense(self, is_on_defense: bool): self._is_on_defense = is_on_defense

    # --- Public Getters ---
    def get_rect(self) -> float: return self._rect
    def get_hp(self) -> float: return self._current_hp
    def get_max_hp(self) -> float: return self._max_hp
    def get_atk(self) -> float: return self._atk
    def get_speed(self) -> float: return self._speed
    def is_on_defense(self) -> bool: return self._is_on_defense
    def is_dead(self) -> bool: return self._current_hp <= 0

    # --- Core Actions ---
    def attack(self, opponent: "Character") -> None:
        if not self._can_attack():
            return

        self._attacking = True
        self._last_attack_time = pygame.time.get_ticks()

        attack_w = 1.8 * self._rect.width
        attack_h = 0.3 * self._rect.height
        attack_x = self._rect.centerx - attack_w if self._flipped else self._rect.centerx
        attack_y = self._rect.y + 20

        attack_rect = pygame.Rect(attack_x, attack_y, attack_w, attack_h)

        if attack_rect.colliderect(opponent._rect) and opponent.get_hp() > 0:
            if not opponent.is_on_defense():
                intersection = attack_rect.clip(opponent._rect)
                damage_ratio = intersection.width / opponent._rect.width
                opponent.take_damage(self, damage_ratio)

    def move(self, dx: float) -> None:
        if self._attacking or self._is_on_defense:
            return

        self._moving = dx != 0
        self._rect.x = max(0, min(self._rect.x + dx, WINDOW_WIDTH - self._rect.width))

    def jump(self) -> None:
        if self._velocity_y == 0.0 and not self._is_on_defense:
            self._velocity_y = -self._jump_velocity * LOCK_FPS

    def take_damage(self, opponent: "Character", ratio: float = 1.0) -> None:
        self._taking_damage = True
        damage = (opponent.get_atk() - self._armor) * ratio
        self._current_hp = max(0.0, self._current_hp - damage)

    def idle(self): self._moving = False

    def look_at(self, opponent: "Character") -> None:
        if not self.is_dead():
            self._flipped = self._rect.centerx > opponent._rect.centerx

    def apply_gravity(self, ground_y: float, delta_time: float) -> None:
        self._velocity_y += GRAVITY * self._weight * delta_time
        self._rect.y += self._velocity_y * delta_time

        if self._rect.bottom >= ground_y:
            self._rect.bottom = ground_y
            self._velocity_y = 0.0

    def _determine_action(self) -> str:
        if self._current_hp == 0: return 'death'
        if self._taking_damage: return 'hit'
        if self._attacking: return 'atk'
        if self._velocity_y != 0.0: return 'jump'
        if self._is_on_defense: return 'def'
        if self._moving: return 'walk'
        return 'idle'

    def _can_attack(self) -> bool:
        return (pygame.time.get_ticks() - self._last_attack_time) >= ATTACK_COOLDOWN

    # --- Update & Animation ---
    @abstractmethod
    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        action = self._determine_action()
        self._character_animation.update(action, delta_time)

        if self._character_animation.get_current_animation().is_complete():
            if action == 'atk': self._attacking = False
            if action == 'hit': self._taking_damage = False
            if action == 'death': self._character_animation.stop_update()

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
