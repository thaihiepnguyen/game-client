from core.character.character_animation import CharacterAnimation
from typing import override
from core.animation.animation import Animation
from core.animation.sprite import Sprite


class SamuraiAnimation(CharacterAnimation):
    @override
    def _load_run_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Walk.png",
            w=128,
            h=128,
            count=8,
            scale=2.2
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_jump_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Jump.png",
            w=128,
            h=128,
            count=12,
            scale=2.2
        )
        return Animation(sprite=sprite, frame_duration=0.04)

    @override
    def _load_idle_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Idle.png",
            w=128,
            h=128,
            count=6,
            scale=2.2
        )
        return Animation(sprite=sprite, frame_duration=0.05)

    @override
    def _load_attack_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Attack_1.png",
            w=128,
            h=128,
            count=6,
            scale=2.2
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_hit_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Hurt.png",
            w=128,
            h=128,
            count=2,
            scale=2.2
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_death_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Dead.png",
            w=128,
            h=128,
            count=3,
            scale=2.2
        )
        return Animation(sprite=sprite, frame_duration=0.1)