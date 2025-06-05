import pygame
from abc import ABC, abstractmethod
from core.const import ATTACK_COOLDOWN, GRAVITY, LOCK_FPS
from core.character.character_animation import CharacterAnimation

class Character(ABC):
    def __init__(self, x: float, y: float, character_animation: CharacterAnimation, speed: float, weight: float, jump_velocity: float, atk: float):
        if speed < 0 or weight <= 0 or jump_velocity < 0 or atk < 0:
            raise ValueError("Speed, weight, jump_velocity, and atk must be non-negative.")

        # Health attributes
        self._max_hp = 100
        self._current_hp = self._max_hp
        self._atk = atk

        # Attack cooldown
        self._last_attack_time = 0

        # Movement attributes
        self._rect = pygame.Rect(x, y, 0, 0)
        self._velocity_y = 0.0
        self._speed = speed
        self._weight = weight
        self._jump_velocity = jump_velocity
        self._moving = False
        self._attacking = False
        self._flipped = False
        self._taking_damage = False

        # Animation setup
        self._character_animation = character_animation


    @abstractmethod
    def draw(self, screen: pygame.Surface, debug: bool = False) -> None:
        """
        Draw the character on the current screen surface.
        :param screen: The screen surface to draw on.
        :param debug:
        """
        
        rect_h = screen.get_height() * 1 / 3
        rect_w = rect_h * 1.3 / 3
        self._rect.height = rect_h
        self._rect.width = rect_w

        if self._velocity_y == 0.0:
            shadow_rect = pygame.Rect(self._rect.centerx - 30, self._rect.bottom - 10, 90, 20)
            pygame.draw.ellipse(screen, (0, 0, 0, 80), shadow_rect)

    @abstractmethod
    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        """
        Update the scene with the given delta time.
        :param screen: The screen surface.
        :param delta_time: The delta time.
        """

        action_type = self._determine_action()

        self._character_animation.update(action_type, delta_time)

        if self._character_animation.get_current_animation().is_complete():
            if action_type == 'atk':
                self._attacking = False
            if action_type == 'hit':
                self._taking_damage = False
            if action_type == 'death':
                self._character_animation.stop_update()


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

        attack_width = 2 * self._rect.width
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
        self._taking_damage = True
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
        if self._current_hp == 0:
            return 'death'
        if self._taking_damage:
            return 'hit'
        if self._velocity_y != 0.0:
            return 'jump'
        if self._attacking:
            return 'atk'
        if self._moving:
            return 'walk'
        return 'idle'

    def _can_attack(self) -> bool:
        """Check if the character can attack based on cooldown."""
        return (pygame.time.get_ticks() - self._last_attack_time) >= ATTACK_COOLDOWN
    