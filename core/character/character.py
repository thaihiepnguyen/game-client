import pygame
from abc import ABC, abstractmethod
from core.const import ATTACK_COOLDOWN, GRAVITY, LOCK_FPS, WINDOW_HEIGHT
from core.character.character_animation import CharacterAnimation

class Character(ABC):
    def __init__(self, x: float, y: float, character_animation: CharacterAnimation):
        # Health attributes
        self._max_hp = 100
        self._current_hp = self._max_hp
        self._atk = self._set_atk()
        self._armor = self._set_armor()

        # Attack cooldown
        self._last_attack_time = 0

        # Movement attributes
        self._rect = pygame.Rect(x, y, 0, 0)
        self._shadow_rect = pygame.Rect(x, y, 0, 0)
        self._velocity_y = 0.0
        self._speed = self._set_speed()
        self._weight = self._set_weight()
        self._jump_velocity = self._set_jump_velocity()
        self._moving = False
        self._attacking = False
        self._flipped = False
        self._taking_damage = False
        self._scale = 1

        # Animation setup
        self._character_animation = character_animation

        if self._speed < 0 or self._weight <= 0 or self._jump_velocity < 0 or self._atk < 0:
            raise ValueError("Speed, weight, jump_velocity, and atk must be non-negative.")

    def set_speed(self, speed):
        self._speed = speed

    def set_weight(self, weight):
        self._weight = weight

    def set_jump_velocity(self, jump_velocity):
        self._jump_velocity = jump_velocity

    def get_speed(self) -> float:
        return self._speed

    def get_weight(self) -> float:
        return self._weight

    def get_jump_velocity(self) -> float:
        return self._jump_velocity

    @abstractmethod
    def _set_speed(self) -> float:
        pass

    @abstractmethod
    def _set_weight(self) -> float:
        pass

    @abstractmethod
    def _set_jump_velocity(self) -> float:
        pass

    @abstractmethod
    def _set_atk(self) -> float:
        pass

    @abstractmethod
    def _set_armor(self) -> float:
        pass

    def draw(self, screen: pygame.Surface, debug: bool = False) -> None:
        """
        Draw the character on the current screen surface.
        :param screen: The screen surface to draw on.
        :param debug:
        """
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self._rect)

        image = self._character_animation.get_current_frame(self._flipped)

        self._character_animation.get_current_animation().set_scale(self._scale)

        offset_x = self._rect.centerx - image.get_width() / 2
        offset_y = self._rect.bottom - image.get_height()
        
        rect_h = screen.get_height() * 1 / 3
        rect_w = rect_h * 1.3 / 3
        self._rect.height = rect_h
        self._rect.width = rect_w

        screen.blit(image, (offset_x, offset_y))
        if self._velocity_y == 0.0:
            self._shadow_rect.x = self._rect.x
            self._shadow_rect.y = self._rect.bottom - 10
            self._shadow_rect.width = self._rect.width * 1.2
            self._shadow_rect.height = self._rect.height * 0.1

            pygame.draw.ellipse(screen, (0, 0, 0, 80), self._shadow_rect)

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
        # ensure character is always in screen
        self._rect.clamp_ip(screen.get_rect())

    def jump(self) -> None:
        """Make the character jump if on the ground."""
        if self._velocity_y == 0.0:  # Only jump if on ground
            self._velocity_y = -self._jump_velocity * LOCK_FPS

    def attack(self, screen: pygame.Surface, opponent: "Character", debug: bool = True) -> None:
        """Attack an opponent if cooldown allows."""
        if not self._can_attack():
            return

        self._attacking = True
        self._last_attack_time = pygame.time.get_ticks()

        attack_width = 1.8 * self._rect.width
        attack_height = 0.3 * self._rect.height
        attack_x = self._rect.centerx - attack_width if self._flipped else self._rect.centerx
        attacking_rect = pygame.Rect(attack_x, self._rect.y + 20, attack_width, attack_height)

        if attacking_rect.colliderect(opponent._rect) and opponent.get_hp() > 0:
            intersection = attacking_rect.clip(opponent._rect)
            ratio = intersection.width / opponent._rect.width
            opponent.take_damage(self, ratio)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), attacking_rect)

    def look_at(self, opponent: "Character") -> None:
        if self.is_dead():
            return
        """Flip the character to face the opponent."""
        self._flipped = self._rect.centerx > opponent._rect.centerx

    def take_damage(self, opponent: "Character", ratio: float = 1) -> None:
        """Reduce HP based on opponent's attack."""
        self._taking_damage = True
        self._current_hp = max(0, self._current_hp - (opponent.get_atk() - self._armor) * ratio)

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

    def _determine_action(self) -> str:
        """Determine the current action based on state."""
        if self._current_hp == 0:
            return 'death'
        if self._taking_damage:
            return 'hit'
        if self._attacking:
            return 'atk'
        if self._velocity_y != 0.0:
            return 'jump'
        if self._moving:
            return 'walk'
        return 'idle'

    def _can_attack(self) -> bool:
        """Check if the character can attack based on cooldown."""
        return (pygame.time.get_ticks() - self._last_attack_time) >= ATTACK_COOLDOWN
    