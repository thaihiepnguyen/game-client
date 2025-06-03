from core.animation.animation import Animation
from core.character.character_animation import CharacterAnimation
from typing import override
from core.animation.sprite import Sprite

class WarriorAnimation(CharacterAnimation):
    @override
    def _load_run_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/warrior/Sprites/Run.png",
            w=162,
            h=162,
            count=8,
            scale=4
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_jump_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/warrior/Sprites/Jump.png",
            w=162,
            h=162,
            count=3,
            scale=4
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_idle_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/warrior/Sprites/Idle.png",
            w=162,
            h=162,
            count=10,
            scale=4
        )
        return Animation(sprite=sprite, frame_duration=0.05)

    @override
    def _load_attack_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/warrior/Sprites/Attack1.png",
            w=162,
            h=162,
            count=7,
            scale=4
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_hit_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/warrior/Sprites/Take-hit.png",
            w=162,
            h=162,
            count=3,
            scale=4
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_death_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/warrior/Sprites/Death.png",
            w=162,
            h=162,
            count=7,
            scale=4
        )
        return Animation(sprite=sprite, frame_duration=0.1)