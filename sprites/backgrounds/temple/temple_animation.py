from core.animation.animation import Animation
from core.animation.sprite import Sprite
from core.background.background_animation import BackgroundAnimation
from typing import override


class TempleAnimation(BackgroundAnimation):
    @override
    def _load_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/backgrounds/temple/bg.png",
            w=768,
            h=368,
            count=8,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _set_ground_y_ratio(self):
        return 4.7 / 5