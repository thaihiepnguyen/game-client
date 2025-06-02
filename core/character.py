import pygame
from abc import ABC, abstractmethod
from core.const import ATTACK_COOLDOWN, GRAVITY, LOCK_FPS
from enum import Enum

from sprites.characters.animation_manager import AnimationManager

CHARACTER_RECT_WIDTH = 40
CHARACTER_RECT_HEIGHT = 90

class ActionType(Enum):
    IDLE = "idle"
    JUMP = "jump"
    RUN = "run"
    ATK = "atk"


class Character(ABC):
    def __init__(self, x: float, y: float, speed: float, weight: float, jump_velocity: float, atk: float):
        if speed < 0 or weight <= 0 or jump_velocity < 0 or atk < 0:
            raise ValueError("Speed, weight, jump_velocity, and atk must be non-negative.")

        # Health attributes
        self._max_hp = 100
        self._current_hp = self._max_hp
        self._atk = atk
        self._last_attack_time = 0

        # Movement attributes
        self._rect = pygame.Rect(x, y, CHARACTER_RECT_WIDTH, CHARACTER_RECT_HEIGHT)
        self._velocity_y = 0.0
        self._speed = speed
        self._weight = weight
        self._jump_velocity = jump_velocity
        self._moving = False
        self._attacking = False
        self._flipped = False

        # Animation setup
        self._animation_manager = self._set_animation()


    @abstractmethod
    def draw(self, screen: pygame.Surface, debug: bool = False) -> None:
        """
        Draw the character on the current screen surface.
        :param screen: The screen surface to draw on.
        """
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self._rect)

        image = self._animation_manager.get_current_frame(self._flipped)

        sprite_scale = self._animation_manager.sprite_scale()

        offset_x = self._rect.x - (72 * sprite_scale)
        offset_y = self._rect.y - (56 * sprite_scale)
        screen.blit(image, (offset_x, offset_y))

    @abstractmethod
    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        """
        Update the scene with the given delta time.
        :param screen: The screen surface.
        :param delta_time: The delta time.
        """

        action_type = self._determine_action()

        self._animation_manager.update(action_type)

        if self._animation_manager.is_animation_complete():
            if action_type == 'atk':
                self._attacking = False
            self._animation_manager.reset_frame()

    @abstractmethod
    def _set_animation(self) -> AnimationManager:
        pass

    def apply_gravity(self, ground_y: float, delta_time: float) -> None:
        """Apply gravity to the character's vertical movement."""
        self._velocity_y += GRAVITY * self._weight * delta_time
        self._rect.y += self._velocity_y * delta_time

        if self._rect.bottom >= ground_y:
            self._rect.bottom = ground_y
            self._velocity_y = 0.0

    def move(self, screen: pygame.Surface, dx: float) -> None:
        """Move the character horizontally within screen bounds."""
        if self._attacking:
            return

        self._moving = dx != 0
        self._rect.x += dx
        self._rect.clamp_ip(screen.get_rect())

    def jump(self) -> None:
        """Make the character jump if on the ground."""
        if self._velocity_y == 0.0:  # Only jump if on ground
            self._velocity_y = -self._jump_velocity * LOCK_FPS

    def attack(self, screen: pygame.Surface, opponent: "Character", debug: bool = False) -> None:
        """Attack an opponent if cooldown allows."""
        if not self._can_attack() or self._velocity_y != 0.0:
            return

        self._attacking = True
        self._last_attack_time = pygame.time.get_ticks()

        attack_width = 1.5 * self._rect.width
        attack_x = self._rect.centerx - attack_width if self._flipped else self._rect.centerx
        attacking_rect = pygame.Rect(attack_x, self._rect.y, attack_width, self._rect.height)

        if attacking_rect.colliderect(opponent._rect) and opponent.get_hp() > 0:
            opponent.take_damage(self)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), attacking_rect)

    def look_at(self, opponent: "Character") -> None:
        """Flip the character to face the opponent."""
        self._flipped = self._rect.centerx > opponent._rect.centerx

    def take_damage(self, opponent: "Character") -> None:
        """Reduce HP based on opponent's attack."""
        self._current_hp = max(0, self._current_hp - opponent.get_atk())

    def idle(self) -> None:
        """Set the character to idle state."""
        self._moving = False

    def get_hp(self) -> float:
        """Get current HP."""
        return self._current_hp

    def get_max_hp(self) -> float:
        """Get maximum HP."""
        return self._max_hp

    def get_atk(self) -> float:
        """Get attack value."""
        return self._atk

    def is_dead(self) -> bool:
        """Check if the character is dead."""
        return self._current_hp <= 0
    
    def get_speed(self) -> float:
        return self._speed

    def _determine_action(self) -> str:
        """Determine the current action based on state."""
        if self._velocity_y != 0.0:
            return 'jump'
        if self._attacking:
            return 'atk'
        if self._moving:
            return 'run'
        return 'idle'

    def _can_attack(self) -> bool:
        """Check if the character can attack based on cooldown."""
        return (pygame.time.get_ticks() - self._last_attack_time) >= ATTACK_COOLDOWN
    