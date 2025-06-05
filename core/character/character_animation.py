import pygame
from abc import ABC, abstractmethod
from core.animation.animation import Animation
from typing import Dict

class CharacterAnimation(ABC):
    def __init__(self):
        self.__animations: Dict[str, Animation] = self._load_animations()
        self.__current_action: str = "idle"
        self.__stop_update: bool = False

    def update(self, action_type: str, delta_time: float) -> None:
        """
        Update the current animation frame based on the action type and delta time.
        :param action_type: The type of action (e.g., 'run', 'jump').
        :param delta_time: The time elapsed since the last update.
        """
        if self.__stop_update:
            return
        if action_type in self.__animations:
            if self.__current_action != action_type:
                self.__animations[self.__current_action].reset()
                self.__current_action = action_type
            self.__animations[self.__current_action].update(delta_time)
        else:
            raise ValueError(f"Action type '{action_type}' not found in animations.")

    def stop_update(self):
        """
        Stop the update of the current animation.
        :return:
        """
        self.__stop_update = True

    def get_current_frame(self, flip: bool = False) -> pygame.Surface:
        """
        Get the current animation frame for the current action.
        :param flip: Whether to flip the frame horizontally.
        :return: The current frame as a pygame.Surface.
        """
        if self.__current_action in self.__animations:
            return self.__animations[self.__current_action].get_current_frame(flip)
        else:
            raise ValueError(f"Current action '{self.__current_action}' not found in animations.")

    def get_current_animation(self) -> Animation:
        """
        Get the current animation object for the current action.
        :return: The current Animation object.
        """
        if self.__current_action in self.__animations:
            return self.__animations[self.__current_action]
        else:
            raise ValueError(f"Current action '{self.__current_action}' not found in animations.")

    def _load_animations(self) -> Dict[str, Animation]:
        """
        Load all animations for the character.
        This method should be implemented by subclasses to load specific animations.
        """
        return {
            "walk": self._load_walk_animation(),
            "jump": self._load_jump_animation(),
            "idle": self._load_idle_animation(),
            "atk": self._load_attack_animation(),
            "hit": self._load_hit_animation(),
            "death": self._load_death_animation()
        }
    
    @abstractmethod
    def _load_walk_animation(self) -> Animation:
        """
        Load the walk animation frames.
        :return: An Animation object for the walk action.
        """
        pass

    @abstractmethod
    def _load_jump_animation(self) -> Animation:
        """
        Load the jump animation frames.
        :return: An Animation object for the jump action.
        """
        pass

    @abstractmethod
    def _load_idle_animation(self) -> Animation:
        """
        Load the idle animation frames.
        :return: An Animation object for the idle action.
        """
        pass

    @abstractmethod
    def _load_attack_animation(self) -> Animation:
        """
        Load the attack animation frames.
        :return: An Animation object for the attack action.
        """
        pass

    @abstractmethod
    def _load_hit_animation(self) -> Animation:
        """
        Load the damage animation frames.
        :return: An Animation object for the damage action.
        """
        pass

    @abstractmethod
    def _load_death_animation(self) -> Animation:
        """
        Load the death animation frames.
        :return: An Animation object for the death action.
        """
        pass