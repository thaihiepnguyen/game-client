import pygame
from abc import ABC

from pygame import Rect

from core.const import CHARACTER_HEIGHT, CHARACTER_WIDTH, Colors, GRAVITY, LOCK_FPS, SHADOW_HEIGHT, SHADOW_WIDTH, WINDOW_WIDTH
from core.character.character_animation import CharacterAnimation

class Character(ABC):
    def __init__(self, character_animation: CharacterAnimation):
        # --- Stats ---
        self.__max_hp = 100
        self.__current_hp: int = self.__max_hp

        # --- Movement / Physics ---
        self.__speed = self._set_speed()

        # --- State Flags ---
        self._state = 'idle'
        self.__stop_update = False
        self._flipped = False
        self._is_moving_left = False
        self._is_moving_right = False

        # --- Graphics & Hitboxes ---
        self._rect = pygame.Rect(0, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self._shadow_rect = pygame.Rect(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
        self._character_animation = character_animation

        # --- Sanity Check ---
        if self.__speed < 0:
            raise ValueError('Speed, weight, jump_velocity must be non-negative.')

    def _set_speed(self) -> float:
        """Set the speed of the character, affecting movement speed."""
        return 200

    # --- Public Getters ---
    def get_rect(self) -> Rect: return self._rect
    def get_hp(self) -> int: return self.__current_hp
    def get_max_hp(self) -> float: return self.__max_hp
    def get_speed(self) -> float: return self.__speed
    def is_dead(self) -> bool: return self.__current_hp <= 0
    def is_defend(self) -> bool: return self._state == 'def'

    # --- Public Setters ---
    def set_x(self, x: int) -> None:
        self._rect.x = max(0, min(x, WINDOW_WIDTH - self._rect.width))
    
    def set_y(self, y: int) -> None:
        self._rect.y = max(0, y)
    
    def set_hp(self, hp: int) -> None:
        self.__current_hp = max(0, min(hp, self.__max_hp))

    def set_flipped(self, flipped: bool) -> None:
        """Set the flipped state of the character, affecting direction."""
        self._flipped = flipped

    def set_state(self, state: str) -> None:
        """Set the current state of the character."""
        valid_states = ['idle', 'walk', 'jump', 'atk_z', 'atk_x', 'atk_c', 'def', 'hit', 'death']
        if state in valid_states:
            if state != self._state:
                self._state = state
        else:
            raise ValueError(f"Invalid state: {state}. Valid states are: {valid_states}")

    # --- Core Actions ---
    def attack_z(self) -> None:
        self._state = 'atk_z'

    def attack_x(self) -> None:
        self._state = 'atk_x'

    def attack_c(self) -> None:
        self._state = 'atk_c'

    def _prevent_move_actions(self):
        return ['atk_z', 'atk_x', 'atk_c', 'def', 'hit', 'death']

    def walk_left(self) -> None:
        if self.is_dead(): return

        if self._state in self._prevent_move_actions():
            return

        self._is_moving_left = True

        if self._state != 'jump' and self._state != 'walk':
            self._state = 'walk'

    def walk_right(self) -> None:
        if self.is_dead(): return

        if self._state in self._prevent_move_actions():
            return

        self._is_moving_right = True

        if self._state != 'jump' and self._state != 'walk':
            self._state = 'walk'

    def stop_movement(self):
        if self.is_dead(): return

        self._is_moving_left = False
        self._is_moving_right = False
        
        self._state = 'idle'

    def jump(self) -> None:
        if self.is_dead(): return

        if self._state in self._prevent_move_actions():
            return

        self._state = 'jump'

    def defend(self) -> None:
        if self.is_dead(): return

        self._state = 'def'

    def undefend(self) -> None:
        if self.is_dead(): return

        self._state = 'idle'

    def hit(self) -> None:
        if self.is_dead() or self._state == 'hit': return

        self._state = 'hit'

    def look_at(self, opponent: "Character") -> None:
        if not self.is_dead():
            self._flipped = self._rect.centerx > opponent._rect.centerx

    def update(self, _: pygame.Surface, delta_time: float) -> None:
        if self.__stop_update:
            return

        if self.__current_hp == 0:
            self._state = 'death'

        if self._is_moving_left:
            dx = -self.__speed * 0.02

            x = max(0, min(int(self._rect.x + dx), WINDOW_WIDTH - self._rect.width))
            self._rect.x = x

        if self._is_moving_right:
            dx = self.__speed * 0.02

            x = max(0, min(int(self._rect.x + dx), WINDOW_WIDTH - self._rect.width))
            self._rect.x = x

        if self._character_animation.get_current_animation().is_complete():
            if self._state == 'death':
                self.__stop_update = True

        self._character_animation.update(self._state, delta_time)

    def draw(self, ground_y: float, screen: pygame.Surface, debug: bool = False) -> None:
        if debug:
            pygame.draw.rect(screen, Colors.RED.value, self._rect)

        image = self._character_animation.get_current_frame(self._flipped)

        offset_x = self._rect.centerx - image.get_width() / 2
        offset_y = self._rect.bottom - image.get_height()

        if abs(self._rect.bottom - int(ground_y)) < 2:
            self._shadow_rect.centerx = self._rect.centerx
            self._shadow_rect.y = self._rect.bottom - 10
            pygame.draw.ellipse(screen, Colors.BLACK.value, self._shadow_rect)

        screen.blit(image, (offset_x, offset_y))
