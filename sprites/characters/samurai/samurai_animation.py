from core.character.character_animation import CharacterAnimation
from typing import override
from core.animation.animation import Animation
from core.animation.sprite import Sprite


class SamuraiAnimation(CharacterAnimation):
    @override
    def _load_walk_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Walk.png",
            w=128,
            h=128,
            count=9,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_jump_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Jump.png",
            w=128,
            h=128,
            count=7,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_idle_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Idle.png",
            w=128,
            h=128,
            count=5,
        )
        return Animation(sprite=sprite, frame_duration=0.05)

    @override
    def _load_attack_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Attack_1.png",
            w=128,
            h=128,
            count=4,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_hit_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Hurt.png",
            w=128,
            h=128,
            count=2,
        )
        return Animation(sprite=sprite, frame_duration=0.5)

    @override
    def _load_death_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/samurai/Sprites/Dead.png",
            w=128,
            h=128,
            count=6,
        )
        return Animation(sprite=sprite, frame_duration=0.1)