import pygame
from abc import ABC, abstractmethod
from core.const import GRAVITY, LOCK_FPS

CHARACTER_RECT_WIDTH = 80
CHARACTER_RECT_HEIGHT = 180

class Character(ABC):
    def __init__(self, x: float, y: float, speed: float, weight: float, jump_velocity):
        self._rect = pygame.Rect((x, y, CHARACTER_RECT_WIDTH, CHARACTER_RECT_HEIGHT))
        self._velocity_y = 0
        self._speed = speed
        self._weight = weight # (e.g, 1.0 for normal, 2.0 for heavy)
        self._jump_velocity = jump_velocity
        self._is_on_ground = False

    def apply_gravity(self, ground_y: float, delta_time: float):
        self._velocity_y += GRAVITY * self._weight * delta_time
        self._rect.y += self._velocity_y * delta_time

        if self._rect.bottom >= ground_y:
            self._rect.bottom = ground_y
            self._velocity_y = 0
            self._is_on_ground = True
        else:
            self._is_on_ground = False

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the character on the current screen surface.
        :param screen: The screen surface to draw on.
        """
        pass

    def move(self, screen: pygame.Surface, dx: float) -> None:
        """
        Move the character by dx, ensuring it stays within the screen bounds.
        :param screen: pygame.Surface
        :param dx: pixel to move in the x direction
        :return:
        """
        self._rect.x += dx
        # Ensure the character stays within the screen bounds
        self._rect.x = max(0, min(self._rect.x, screen.get_width() - self._rect.width))
    
    def jump(self) -> None:
        if self._is_on_ground:
            self._velocity_y = -self._jump_velocity * LOCK_FPS
            self._is_on_ground = False

    def get_speed(self):
        return self._speed