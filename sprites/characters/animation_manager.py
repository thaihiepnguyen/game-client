import pygame

from typing import List, Dict
from enum import Enum

from core.const import ANIMATION_COOLDOWN

class ActionType(Enum):
    IDLE = "idle"
    JUMP = "jump"
    RUN = "run"
    ATK = "atk"

class AnimationManager:
    def __init__(self, sprite_dir: str, animation_steps: List[int], sprite_size: float, sprite_scale: float, action_index_map: Dict[ActionType, int]):
        self._sprite_dir = sprite_dir
        self._animation_steps = animation_steps
        self._sprite_size = sprite_size
        self._sprite_scale = sprite_scale
        self._action_index_map = action_index_map
        self._animations = self._load_sprites()
        self._current_action = 'idle'
        self._current_frame = 0
        self._last_update_time = 0
        self._cooldown = ANIMATION_COOLDOWN

    def _load_sprites(self) -> List[List[pygame.Surface]]:
        """Load and scale sprites from a sprite sheet."""
        try:
            sprite_sheet = pygame.image.load(self._sprite_dir).convert_alpha()
        except pygame.error as e:
            raise ValueError(f"Failed to load sprite sheet {self._sprite_dir}: {e}")

        animations = []
        for y, steps in enumerate(self._animation_steps):
            frames = []
            for x in range(steps):
                frame = sprite_sheet.subsurface(x * self._sprite_size, y * self._sprite_size, self._sprite_size, self._sprite_size)
                scaled_frame = pygame.transform.scale(frame, (self._sprite_size * self._sprite_scale, self._sprite_size * self._sprite_scale))
                frames.append(scaled_frame)
            animations.append(frames)
        return animations

    def update(self, action_type: str) -> None:
        """Update the current animation frame based on action type."""
        if not self._can_update():
            return

        action_index = self._action_index_map.get(action_type, 0)
        if action_index != self._action_index_map[self._current_action]:
            self._current_action = action_type
            self.reset_frame()

        frames = self._animations[action_index]
        self._current_frame = (self._current_frame + 1) % len(frames)
        self._last_update_time = pygame.time.get_ticks()

    def get_current_frame(self, flip: bool = False) -> pygame.Surface:
        """Get the current animation frame, optionally flipped."""
        frame = self._animations[self._action_index_map[self._current_action]][self._current_frame]
        return pygame.transform.flip(frame, flip, False) if flip else frame

    def reset_frame(self) -> None:
        """Reset the frame index to 0."""
        self._current_frame = 0

    def is_animation_complete(self) -> bool:
        """Check if the current animation has completed."""
        return self._current_frame == len(self._animations[self._action_index_map[self._current_action]]) - 1

    def _can_update(self) -> bool:
        """Check if enough time has passed to update the animation."""
        return (pygame.time.get_ticks() - self._last_update_time) >= self._cooldown
    
    def sprite_size(self) -> float:
        return self._sprite_size
    
    def sprite_scale(self) -> float:
        return self._sprite_scale