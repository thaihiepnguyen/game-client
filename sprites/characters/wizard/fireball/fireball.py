
import pygame

from core.animation.animation import Animation
from core.const import Colors, WINDOW_WIDTH
from core.animation.sprite import Sprite

class Fireball:
    def __init__(self, x, y, is_flipped: bool, speed: int = 1000):
        self.__rect = pygame.Rect(x, y, 90, 30)
        self.__is_flipped = is_flipped
        sprite = Sprite(
            dir="assets/images/characters/wizard/Sprites/Charge_1.png",
            w=64,
            h=128,
            count=9,
        )
        self.__animation = Animation(sprite=sprite, frame_duration=0.06)
        self.__animation.set_scale(2.0)
        self.__speed = speed

    def get_rect(self):
        return self.__rect

    def update(self, delta_time) -> bool:
        dx = (-1 if self.__is_flipped else 1) * self.__speed * delta_time
        self.__rect.x += dx

        if self.__rect.x <= 0 or self.__rect.x >= WINDOW_WIDTH:
            return False

        self.__animation.update(delta_time)
        return True

    def draw(self, screen, debug=False):
        if debug:
            pygame.draw.rect(screen, Colors.RED.value, self.__rect)

        image = self.__animation.get_current_frame(self.__is_flipped)

        screen.blit(image, (self.__rect.x, self.__rect.centery - image.get_height() / 2))