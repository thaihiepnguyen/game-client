from core.animation.animation import Animation
from core.animation.sprite import Sprite
from core.background.background_animation import BackgroundAnimation
from typing import override


class StreetAnimation(BackgroundAnimation):
    @override
    def _load_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/background/street/bg.png",
            w=640,
            h=324,
            count=8,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

