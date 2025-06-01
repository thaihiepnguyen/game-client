import pygame
from abc import ABC, abstractmethod
from core.const import GRAVITY, LOCK_FPS
from enum import Enum
from typing import Dict

CHARACTER_RECT_WIDTH = 80
CHARACTER_RECT_HEIGHT = 180

class ActionType(Enum):
    IDLE = "idle"
    JUMP = "jump"
    RUN = "run"
    ATK = "atk"


class Character(ABC):
    def __init__(self, x: float, y: float, speed: float, weight: float, jump_velocity: float, atk: float):
        # private
        self.__max_hp = 100
        self.__hp = self.__max_hp
        self.__atk = atk
        self.__attack_cooldown = 300
        self.__last_attack_time = 0
        self.__animation_cooldown = 50
        self.__last_update_time = 0
        self.__sprite_dir = self._set_sprite_dir()
        self.__action_index_map = self._set_action_index_map()
        self.__animation_steps = self._set_animation_steps()
        self.__frame_index = 0
        self.__action_index = self.__action_index_map[ActionType.IDLE]
        self.__animation_list = self.__load_sprites()

        # protected
        self._rect = pygame.Rect((x, y, CHARACTER_RECT_WIDTH, CHARACTER_RECT_HEIGHT))
        self._flip = False
        self._velocity_y = 0
        self._moving = False
        self._attacking = False
        self._speed = speed
        self._weight = weight # (e.g, 1.0 for normal, 2.0 for heavy)
        self._jump_velocity = jump_velocity


    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the character on the current screen surface.
        :param screen: The screen surface to draw on.
        """

        pygame.draw.rect(screen, (255, 0, 0), self._rect)
        image = self.__animation_list[self.__action_index][self.__frame_index]

        flip_img = pygame.transform.flip(image, self._flip, False)
        screen.blit(flip_img, (self._rect.x - (72 * 4), self._rect.y - (56 * 4)))

    @abstractmethod
    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        """
        Update the scene with the given delta time.
        :param screen: The screen surface.
        :param delta_time: The delta time.
        """

        if not self.__can_update_animation():
            return

        if self._attacking:
            self.__update_action(ActionType.ATK)
        elif self._velocity_y != 0:
            self.__update_action(ActionType.JUMP)
        elif self._moving:
            self.__update_action(ActionType.RUN)
        else:
            self.__update_action(ActionType.IDLE)

        if self.__frame_index == len(self.__animation_list[self.__action_index]) - 1:
            if self.__action_index == self.__action_index_map[ActionType.ATK]:
                self._attacking = False
            self.__frame_index = 0
        else:
            self.__frame_index += 1
        
        self.__last_update_time = pygame.time.get_ticks()

    @abstractmethod
    def _set_sprite_dir(self) -> str:
        pass

    @abstractmethod
    def _set_action_index_map(self) -> Dict[ActionType, int]:
        return {
            ActionType.IDLE: 0,
            ActionType.RUN: 1,
            ActionType.JUMP: 2,
            ActionType.ATK: 3
        }

    @abstractmethod
    def _set_animation_steps(self) -> list:
        pass

    def __load_sprites(self) -> list:
        size = 162
        sprite_sheet = pygame.image.load(self.__sprite_dir).convert_alpha()
        animation_list = []
        for y, animation in enumerate(self.__animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * size, y * size, size, size)
                temp_img_list.append(pygame.transform.scale(temp_img, (size * 4, size * 4)))
            animation_list.append(temp_img_list)

        return animation_list

    def __can_update_animation(self) -> bool:
        return (pygame.time.get_ticks() - self.__last_update_time) > self.__animation_cooldown

    def __can_attack(self) -> bool:
        """
        Check if this character is able to attack or not at the monent (current frame)
        :return: true / false
        """
        return (pygame.time.get_ticks() - self.__last_attack_time) >= self.__attack_cooldown

    def __update_action(self, new_action_type: ActionType):
        new_action_index = self.__action_index_map[new_action_type]
        if self.__action_index == new_action_index:
            return
        
        self.__action_index = new_action_index
        self.__frame_index = 0
        self.__last_update_time = pygame.time.get_ticks()

    def is_dead(self):
        return self.__hp == 0

    def get_hp(self):
        return self.__hp

    def get_max_hp(self):
        return self.__max_hp

    def get_atk(self):
        return self.__atk

    def get_speed(self):
        return self._speed

    def take_damage(self, oppenent: "Character"):
        self.__hp -= min(self.__hp, oppenent.get_atk())

    def apply_gravity(self, ground_y: float, delta_time: float):
        self._velocity_y += GRAVITY * self._weight * delta_time
        self._rect.y += self._velocity_y * delta_time

        if self._rect.bottom >= ground_y:
            self._rect.bottom = ground_y
            self._velocity_y = 0

    def look_at(self, opponent: "Character"):
        self._flip = self._rect.centerx > opponent._rect.centerx
    
    def attack(self, screen: pygame.Surface, opponent: "Character"):
        if not self.__can_attack():
            return
        self._attacking = True
        attacking_rect = pygame.Rect(self._rect.centerx - (1.5 * self._rect.width * self._flip), self._rect.y, 1.5 * self._rect.width, self._rect.height)
        if attacking_rect.colliderect(opponent._rect):
            if opponent.get_hp() > 0:
                opponent.take_damage(self)
        pygame.draw.rect(screen, (0, 255, 0), attacking_rect)
        self.__last_attack_time = pygame.time.get_ticks()

    def move(self, screen: pygame.Surface, dx: float) -> None:
        """
        Move the character by dx, ensuring it stays within the screen bounds.
        :param screen: pygame.Surface
        :param dx: pixel to move in the x direction
        :return:
        """
        if self._attacking == True:
            return

        self._moving = True
        self._rect.x += dx
        # Ensure the character stays within the screen bounds
        self._rect.x = max(0, min(self._rect.x, screen.get_width() - self._rect.width))
    
    def jump(self) -> None:
        if not self._velocity_y:
            self._velocity_y = -self._jump_velocity * LOCK_FPS

    def idle(self):
        self._moving = False